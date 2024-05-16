# Complete your game here
import pygame as pg
from pygame import Vector2
from random import randint
import math


class GameObject:
    """Base class for objects including position, a hitbox and draw function"""

    def __init__(self, graphic: str, pos: Vector2, size: int = 100, height: int = 100) -> None:
        self.graphic = pg.image.load(graphic)
        self.pos = pos.copy()
        self.hitbox = pg.Rect(0, 0, size, height)
        self.hitbox.center = self.pos
        self.heading = Vector2(0, -1)  # pointing upwards by default
        self.is_destroyed = False

    def draw(self, window: pg.Surface):
        """draws the graphic at the object center"""
        offset = pg.math.Vector2(self.graphic.get_rect().center)
        window.blit(self.graphic, self.pos - offset)

    def destroy(self):
        """Marks the object ready for destruction. Called by other Objects."""
        self.is_destroyed = True


class Door(GameObject):
    """The exit door of each level"""
    def __init__(self, graphic: str, pos: Vector2, size: int = 100, height: int = 100) -> None:
        super().__init__(graphic, pos, size, height)


class Coin(GameObject):
    """The Coins that need to be collected"""
    def __init__(self, graphic: str, pos: Vector2, size: int = 40, height: int = 40) -> None:
        super().__init__(graphic, pos, size, height)


class DynamicObject(GameObject):
    """Object with movement and direction."""

    def __init__(self, graphic: str, pos: Vector2, size: int = 100, height: int = 100) -> None:
        super().__init__(graphic, pos, size, height)
        self.vel = 0
        self.max_vel = 5
        self.agility = 3

    def move(self):
        """locomotion for the object"""
        self.pos = self.pos + self.heading.normalize() * self.vel
        self.hitbox.center = self.pos

    def draw(self, window: pg.Surface):
        """rotates and draws graphic centered on pos"""
        direction = Vector2(0, -1).angle_to(self.heading)
        body = pg.transform.rotate(self.graphic, - direction),
        offset = pg.math.Vector2(body[0].get_rect().center)
        window.blit(body[0], self.pos - offset)


class Robot(DynamicObject):
    """Main Character. Can be controlled by the player."""

    def __init__(self, graphic: str, pos: Vector2, size: int = 50, height: int = 50) -> None:
        super().__init__(graphic, pos, size, height)
        self.dir = [0, 0]
        self.coins_collected = 0
        self.won = False
        self.acceleration = 0.4

    def update(self):
        """updates the player state"""
        self.drive()
        self.move()

    def drive(self):
        """acceleratets, brakes and steers the player based on the input direction"""

        # accelerating
        if self.dir[1] != 0:
            self.vel += self.dir[1] * self.acceleration
        # decelerating
        elif self.vel < -self.acceleration * 2:
            self.vel += self.acceleration * 2
        elif self.vel > self.acceleration * 2:
            self.vel -= self.acceleration * 2
        else:
            self.vel = 0

        if self.vel > self.max_vel:
            self.vel = self.max_vel
        if self.vel < -self.max_vel:
            self.vel = -self.max_vel

        # steering
        self.heading.rotate_ip(self.dir[0] * self.agility)
        self.heading.rotate_ip(self.dir[0] * self.agility)

    def control(self, event):
        """gets the key inputs and determines the direction"""
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                self.dir[0] -= 1
            if event.key == pg.K_RIGHT:
                self.dir[0] += 1
            if event.key == pg.K_UP:
                self.dir[1] += 1
            if event.key == pg.K_DOWN:
                self.dir[1] -= 1

        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                self.dir[0] += 1
            if event.key == pg.K_RIGHT:
                self.dir[0] -= 1
            if event.key == pg.K_UP:
                self.dir[1] -= 1
            if event.key == pg.K_DOWN:
                self.dir[1] += 1

    def collide_with(self, objects: list) -> int:
        """Detects and handles all collisions. Objects is a list of GameObjects.Returns coins collected on pickup. Return -1: Door Return -2: game over."""
        for o in objects:
            if self.hitbox.colliderect(o.hitbox):
                # robot is colliding with object o
                if isinstance(o, Coin):
                    o.destroy()
                    self.coins_collected += 1
                    return self.coins_collected
                elif isinstance(o, Door):
                    return -1
                elif isinstance(o, Ghost):
                    return -2
        return 0


class Ghost(DynamicObject):
    """Enemy Character. Spawns and flys towards Robot. Has a target."""

    def __init__(self, graphic: str, pos: Vector2, target: GameObject, size: int = 50, height: int = 50) -> None:
        super().__init__(graphic, pos, size, height)
        self.target = target
        self.vel = 4
        self.agility = 1.5
        self.heading = self.heading.rotate(randint(0, 359))

    def update(self):
        """Updates the Ghost by turning it into a homing missile"""
        # find target
        target_direction = self.target.pos - self.pos
        angle_to_target = self.angle_between_vectors(
            self.heading, target_direction)

        # steer rocket
        if angle_to_target > self.agility:
            self.heading = self.heading.rotate(self.agility)
        elif angle_to_target < -self.agility:
            self.heading = self.heading.rotate(-self.agility)
        else:
            self.heading = target_direction.normalize()

        self.move()

    def angle_between_vectors(self, v1, v2):
        """returns the angle in between v1 and v2 from 180° to -180° - thanks chatgpt for this one!"""
        dot_product = v1[0] * v2[0] + v1[1] * v2[1]
        magnitude_v1 = math.sqrt(v1[0]**2 + v1[1]**2)
        magnitude_v2 = math.sqrt(v2[0]**2 + v2[1]**2)
        cos_theta = dot_product / (magnitude_v1 * magnitude_v2)

        if cos_theta > 1:
            cos_theta = 1
        elif cos_theta < -1:
            cos_theta = -1

        angle_radians = math.acos(cos_theta)
        angle_degrees = math.degrees(angle_radians)

        # Determine the sign of the angle using the cross product
        cross_product = v1[0] * v2[1] - v1[1] * v2[0]
        if cross_product < 0:
            angle_degrees = -angle_degrees

        return angle_degrees


class Level:
    """Contains all objects for a game session"""

    def __init__(self, window: pg.Surface, clock: pg.time.Clock, goal: int = 3, ghosts: int = 1) -> None:
        self.window = window
        self.clock = clock
        self.score = 0
        self.goal = goal
        self.ghosts = ghosts
        self.door = Door("door.png", Vector2(self.random_location()))
        self.player = Robot("robot.png", Vector2(
            20, pg.display.get_surface().get_height() - 100))
        self.coins_list = []
        self.spawn_coins(self.goal)
        self.ghost_list = []
        self.spawn_ghosts(self.ghosts)

    def run(self) -> str:
        """main loop of the game session"""
        while True:
            self.events()

            self.player.update()
            for g in self.ghost_list:
                g.update()

            result = self.player.collide_with(
                self.coins_list + self.ghost_list + [self.door])

            if result > 0:
                self.score = result
            elif result == -1:
                if self.score == self.goal:
                    return "won"
            elif result == -2:
                return "lost"

            self.destroy_coins()

            self.render()
            self.clock.tick(60)

    def events(self):
        """gets user input"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.KEYDOWN or event.type == pg.KEYUP:
                self.player.control(event)

    def render(self):
        """Draw all content to the window"""
        self.window.fill((200, 200, 200))

        self.door.draw(self.window)

        for c in self.coins_list:
            c.draw(self.window)
        for g in self.ghost_list:
            g.draw(self.window)

        self.player.draw(self.window)

        font = pg.font.Font(None, 32)
        score_str = f"Score: {self.score} / {self.goal}"
        scroe_srf = font.render(score_str, True,  (10, 10, 10))

        self.window.blit(scroe_srf, (20, 20))

        pg.display.flip()

    def random_location(self, margin: int = 50) -> tuple:
        """returns a random location (tuple) with a safety margin"""
        space_x = (margin, pg.display.get_surface().get_width() - margin)
        space_y = (margin, pg.display.get_surface().get_height() - margin)
        return (randint(space_x[0], space_x[1]), randint(space_y[0], space_y[1]))

    def spawn_coins(self, amount: int = 3):
        """Creates coins in random places"""
        for i in range(amount):
            self.coins_list.append(
                Coin("coin.png", Vector2(self.random_location())))

    def spawn_ghosts(self, amount: int = 1):
        """Creates coins in random places"""
        for i in range(amount):
            self.ghost_list.append(
                Ghost("monster.png", Vector2(self.random_location(200)), self.player))

    def destroy_coins(self):
        destroy_list = []
        for c in self.coins_list:
            if c.is_destroyed:
                destroy_list.append(c)

        for c in destroy_list:
            if c in self.coins_list:
                self.coins_list.remove(c)


class Button:
    def __init__(self, text: str, pos_y: int) -> bool:
        self.text = text
        self.hover = False
        self.shape = pg.Rect(0, 0, 300, 60)
        self.shape.center = (
            pg.display.get_surface().get_width()//2, pos_y)
        self.pressed = False

    def draw(self, window: pg.Surface):
        color = (10, 10, 10)
        font = pg.font.Font(None, 36)
        text = font.render(self.text, True, color)
        offset = pg.math.Vector2(text.get_rect().center)

        if self.hover:
            pg.draw.rect(window, (100, 100, 100), self.shape)
        pg.draw.rect(window, color, self.shape, width=2)
        window.blit(text, self.shape.center - offset)

    def update(self):
        if self.shape.collidepoint(pg.mouse.get_pos()):
            self.hover = True
        else:
            self.hover = False

        if self.pressed:
            self.pressed = False
            return True

        return False

    def click(self):
        if self.shape.collidepoint(pg.mouse.get_pos()):
            self.pressed = True


class Application:
    """Main Application Class"""

    # level (coins to collect, ghosts to avoid)
    levels = {
        1: (3, 1),
        2: (5, 1),
        3: (3, 2),
        4: (5, 2),
        5: (200, 2),
        6: (1, 3),
        7: (1, 8),
        8: (100, 100)
    }

    def __init__(self) -> None:
        pg.init()
        self.clock = pg.time.Clock()
        self.window = pg.display.set_mode((800, 600))
        self.level = 1
        self.state = "default"
        self.buttons = {
            "play": Button("Play Game", pos_y=420),
            "exit": Button("Exit", pos_y=500)
        }

    def run(self):
        while True:
            self.events()
            if self.buttons["play"].update():
                g = Level(self.window, self.clock,
                          goal=Application.levels[self.level][0], ghosts=Application.levels[self.level][1])
                self.state = g.run()
                if self.state == "won":
                    self.level += 1
                    self.buttons["play"].text = "Next Level"
                    if self.level not in Application.levels:
                        self.state = "finished"
                        self.level = 1
                        self.buttons["play"].text = "Play Again"
                if self.state == "lost":
                    self.buttons["play"].text = "Try Again"

            if self.buttons["exit"].update():
                exit()

            self.render()
            self.clock.tick(60)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                for i, b in self.buttons.items():
                    b.click()

    def render(self):
        self.window.fill((200, 200, 200))
        string = "Collect all coins and exit whitout getting caught!"
        string2 = "Arrow Keys: Move Player"

        color = (10, 10, 10)
        font = pg.font.Font(None, 36)

        text = font.render(string, True, color)
        offset = pg.math.Vector2(text.get_rect().center)
        self.window.blit(text, (400, 150) - offset)

        text = font.render(string2, True, color)
        offset = pg.math.Vector2(text.get_rect().center)
        self.window.blit(text, (400, 200) - offset)

        if self.state == "won":
            string = f"You won Level {self.level-1}! Congrats!"
            text = font.render(string, True, color)
            offset = pg.math.Vector2(text.get_rect().center)
            self.window.blit(text, (400, 300) - offset)
        elif self.state == "lost":
            string = f"You lost Level {self.level}! Better luck next time"
            text = font.render(string, True, color)
            offset = pg.math.Vector2(text.get_rect().center)
            self.window.blit(text, (400, 300) - offset)
        elif self.state == "finished":
            string = f"You beat the game. You're a true master of gaming!"
            text = font.render(string, True, color)
            offset = pg.math.Vector2(text.get_rect().center)
            self.window.blit(text, (400, 300) - offset)

        for i, b in self.buttons.items():
            b.draw(self.window)

        pg.display.flip()


app = Application()
app.run()

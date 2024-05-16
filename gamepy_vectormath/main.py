import pygame
from projectiles import Projectile, Rocket, ProjectileCollection
from items import ItemCollection
from tank import Tank, TankController
from enemies import RocketPod


class GameSession:
    def __init__(self, window: pygame.Surface, clock: pygame.time.Clock) -> bool:
        self.window = window
        self.clock = clock
        self.arena = pygame.image.load("arena.png")
        self.player = TankController(Tank())
        self.projectiles = ProjectileCollection()
        self.enemy = RocketPod(pygame.math.Vector2(
            400, 300), self.projectiles, self.player.tank)
        self.crates = ItemCollection()

    def run(self):
        while True:
            self.events()

            self.player.update()
            self.crates.upate()
            self.player.pickup_items(self.crates.items)
            self.player.get_hit(self.projectiles.alive_projectiles)
            self.enemy.get_hit(self.projectiles.alive_projectiles)
            self.enemy.update()
            self.projectiles.update()

            self.render()

            if self.player.health <= 0:
                return False
            if self.enemy.health <= 0:
                self.game_won()
                return True

            self.clock.tick(60)

    def game_over(self):
        pass

    def game_won(self):
        pass

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                self.player.steer_body(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.player.shoot(self.projectiles)

    def render(self):
        self.window.fill((200, 200, 200))
        self.window.blit(self.arena, (0,0))

        self.enemy.draw(self.window)
        self.crates.draw(self.window)
        self.projectiles.draw(self.window)
        self.player.draw(self.window)

        self.player.draw_ui(self.window)
        self.enemy.draw_ui(self.window)

        # pygame.draw.circle(self.window, (0, 0, 255), pygame.mouse.get_pos(), 5)
        pygame.display.flip()


class Button:
    def __init__(self, text: str, pos_y: int) -> bool:
        self.text = text
        self.hover = False
        self.shape = pygame.Rect(0, 0, 300, 60)
        self.shape.center = (
            pygame.display.get_surface().get_width()//2, pos_y)
        self.pressed = False

    def draw(self, window: pygame.Surface):
        color = (10, 10, 10)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, color)
        offset = pygame.math.Vector2(text.get_rect().center)

        if self.hover:
            pygame.draw.rect(window, (100, 100, 100), self.shape)
        pygame.draw.rect(window, color, self.shape, width=2)
        window.blit(text, self.shape.center - offset)

    def update(self):
        if self.shape.collidepoint(pygame.mouse.get_pos()):
            self.hover = True
        else:
            self.hover = False

        if self.pressed:
            self.pressed = False
            return True

        return False

    def click(self):
        if self.shape.collidepoint(pygame.mouse.get_pos()):
            self.pressed = True


class Application:
    def __init__(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((800, 600))
        self.bg = pygame.image.load("menu.png")
        self.buttons = {
            "play": Button("Play Game", pos_y=420),
            "exit": Button("Exit", pos_y=500)
        }

    def run(self):
        while True:
            self.events()
            if self.buttons["play"].update():
                g = GameSession(self.window, self.clock)
                g.run()
                pass
            if self.buttons["exit"].update():
                exit()

            self.render()
            self.clock.tick(60)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, b in self.buttons.items():
                    b.click()

    def render(self):
        self.window.fill((200, 200, 200))
        self.window.blit(self.bg, (0,0))

        for i, b in self.buttons.items():
            b.draw(self.window)

        pygame.display.flip()


app = Application()
app.run()

import pygame
import math


class Projectile:
    def __init__(self, pos: pygame.math.Vector2, heading: pygame.math.Vector2, vel: float = 10) -> None:
        self.pos = pos.copy()
        self.heading = heading.copy()
        self.vel = vel
        self.age = 0

    def update(self):
        self.pos = self.pos + self.heading.normalize() * self.vel
        self.age += 1

    def draw(self, window: pygame.Surface):
        pygame.draw.circle(window, (0, 0, 0), (self.pos[0], self.pos[1]), 5)


class ProjectileCollection:
    def __init__(self) -> None:
        self.alive_projectiles = []
        self.destruct_projectiles = []
        self.max_age = 120

    def update(self):
        for p in self.alive_projectiles:
            p.update()
            if p.age > self.max_age:
                self.destruct_projectiles.append(p)

        self.destroy_projectiles()

    def destroy_projectiles(self):
        for p in self.destruct_projectiles:
            self.alive_projectiles.remove(p)
        self.destruct_projectiles = []

    def draw(self, window: pygame.Surface):
        for p in self.alive_projectiles:
            p.draw(window)


class Tank:
    def __init__(self) -> None:
        self.body = pygame.image.load("body.png")
        self.tower = pygame.image.load("tower.png")
        self.pos = pygame.math.Vector2(200, 200)
        self.heading_body = 0
        self.heading_tower = pygame.math.Vector2(0, 0)
        self.vel = 0
        self.max_vel = 3
        self.rot_vel = 0
        self.max_rot_vel = 5

    def drive(self):

        heading_vector = pygame.math.Vector2(
            math.cos(math.radians(self.heading_body)), math.sin(math.radians(self.heading_body)))
        self.pos = self.pos + heading_vector.normalize() * self.vel

    def draw(self, window: pygame.Surface):
        # body
        body = pygame.transform.rotate(self.body, -self.heading_body - 90),
        offset_b = pygame.math.Vector2(body[0].get_rect().center)
        window.blit(body[0], self.pos - offset_b)

        # tower
        direction = pygame.math.Vector2(
            0, -1).angle_to(self.heading_tower)
        tower = pygame.transform.rotate(self.tower, - direction)
        offset_b = pygame.math.Vector2(tower.get_rect().center)
        window.blit(tower, self.pos - offset_b)


class TankController:
    def __init__(self, tank: Tank) -> None:
        self.tank = tank
        self.dir = [0, 0]

    def steer_body(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.dir[0] -= 1
            if event.key == pygame.K_RIGHT:
                self.dir[0] += 1
            if event.key == pygame.K_UP:
                self.dir[1] += 1
            if event.key == pygame.K_DOWN:
                self.dir[1] -= 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.dir[0] += 1
            if event.key == pygame.K_RIGHT:
                self.dir[0] -= 1
            if event.key == pygame.K_UP:
                self.dir[1] -= 1
            if event.key == pygame.K_DOWN:
                self.dir[1] += 1

    def steer_tower(self):
        # self.tank.heading_tower.update(pygame.mouse.get_pos())
        heading = pygame.math.Vector2(pygame.mouse.get_pos()) - self.tank.pos
        self.tank.heading_tower = heading.normalize()

    def shoot(self, projectiles: ProjectileCollection):
        projectiles.alive_projectiles.append(
            Projectile(self.tank.pos, self.tank.heading_tower))

    def update(self):
        # driving
        # accelerating
        vel_accel = 0.1
        if self.dir[1] != 0:
            self.tank.vel += self.dir[1] * vel_accel
        # decelerating
        elif self.tank.vel < -vel_accel * 2:
            self.tank.vel += vel_accel * 2
        elif self.tank.vel > vel_accel * 2:
            self.tank.vel -= vel_accel*2
        else:
            self.tank.vel = 0

        if self.tank.vel > self.tank.max_vel:
            self.tank.vel = self.tank.max_vel
        if self.tank.vel < -self.tank.max_vel:
            self.tank.vel = -self.tank.max_vel

        rot_accel = 2
        if self.tank.vel < 0:
            rot_accel *= -1
        self.tank.heading_body += self.dir[0] * rot_accel

        self.tank.drive()

    def draw(self, window):
        self.tank.draw(window)


class TankApp:
    def __init__(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((800, 600))
        self.tank = TankController(Tank())
        self.projectiles = ProjectileCollection()

    def run(self):
        while True:
            self.events()

            self.tank.update()
            self.projectiles.update()

            self.render()
            self.clock.tick(60)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                self.tank.steer_body(event)
            if event.type == pygame.MOUSEMOTION:
                self.tank.steer_tower()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.tank.shoot(self.projectiles)

    def render(self):
        self.window.fill((200, 200, 200))
        self.projectiles.draw(self.window)
        self.tank.draw(self.window)
        pygame.draw.circle(self.window, (0, 0, 255), pygame.mouse.get_pos(), 5)
        pygame.display.flip()


app = TankApp()
app.run()

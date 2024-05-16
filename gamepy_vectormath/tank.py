import pygame
from projectiles import Projectile, Rocket, ProjectileCollection


class Tank:
    """The tank model of the game."""

    def __init__(self) -> None:
        self.body = pygame.image.load("body.png")
        self.tower = pygame.image.load("tower.png")
        self.pos = pygame.math.Vector2(200, 200)
        self.heading_body = pygame.math.Vector2(
            1, 0)  # tank spawns in direction X+
        self.heading_tower = pygame.math.Vector2(0, 0)
        self.vel = 0
        self.max_vel = 3
        self.rot_vel = 0
        self.max_rot_vel = 5
        self.hitbox = pygame.Rect(0, 0, 100, 100)
        self.hitbox.center = self.pos

    def drive(self):
        self.pos = self.pos + self.heading_body.normalize() * self.vel
        self.hitbox.center = self.pos

    def draw(self, window: pygame.Surface):
        # body
        # get the angle relative to Y- (direction of sprite drawn)
        direction_body = pygame.math.Vector2(0, -1).angle_to(self.heading_body)
        body = pygame.transform.rotate(self.body, - direction_body),
        offset_b = pygame.math.Vector2(body[0].get_rect().center)
        window.blit(body[0], self.pos - offset_b)

        # tower
        # get the angle relative to Y- (direction of sprite drawn)
        direction_tower = pygame.math.Vector2(
            0, -1).angle_to(self.heading_tower)
        tower = pygame.transform.rotate(self.tower, - direction_tower)
        offset_b = pygame.math.Vector2(tower.get_rect().center)
        window.blit(tower, self.pos - offset_b)


class TankController:
    """The Class controlling the tank through key and mouse input."""

    def __init__(self, tank: Tank) -> None:
        self.tank = tank
        self.dir = [0, 0]
        self.ammo = 20

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

        # yaw rotation
        rot_accel = 2
        self.tank.heading_body.rotate_ip(self.dir[0] * rot_accel)

        self.tank.drive()

    def pickup_item(self, item: object):
        if self.tank.hitbox.colliderect(item.hitbox):
            print("item collected!")

    def draw(self, window):
        self.tank.draw(window)

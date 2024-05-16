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
        self.max_ammo = 20
        self.ammo = 20
        self.health = 100
        self.boost_timer = 0

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
        if self.ammo > 0:
            projectiles.alive_projectiles.append(
                Projectile(self.tank.pos, self.tank.heading_tower))
            self.ammo -= 1

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

        # boost
        max_vel = self.tank.max_vel
        if self.boost_timer > 0:
            max_vel += 2
            self.boost_timer -= 1

        if self.tank.vel > max_vel:
            self.tank.vel = max_vel
        if self.tank.vel < -max_vel:
            self.tank.vel = -max_vel

        # yaw rotation
        rot_accel = 2
        self.tank.heading_body.rotate_ip(self.dir[0] * rot_accel)

        self.tank.drive()

    def pickup_items(self, items: list):
        for i in items:
            if self.tank.hitbox.colliderect(i.hitbox):
                print(f"collected: {type(i)}")
                i.collect()
                if i.type == "ammo":
                    self.fill_ammo()
                if i.type == "health":
                    self.health = 100
                if i.type == "boost":
                    self.boost_timer = 300



    def fill_ammo(self):
        self.ammo += 5
        if self.ammo > self.max_ammo:
            self.ammo = self.max_ammo

    def draw(self, window):
        self.tank.draw(window)

    def draw_ui(self, window):
        font = pygame.font.Font(None, 24)
        ammo_str = f"Ammo: {self.ammo}"
        ammo = font.render(ammo_str, True,  (10, 10, 10))
        health_str = f"Health: {self.health}"
        health = font.render(health_str, True,  (10, 10, 10))
        window.blit(ammo, (10, 10))
        window.blit(health, (10, 30))

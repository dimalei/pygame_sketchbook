# class defing projectiles and projectile environments (collections)
import pygame
import math
from helpers import angle_between_vectors

import pygame.locals


class Projectile:
    """Base projectile that the tank can shoot."""

    def __init__(self, pos: pygame.math.Vector2, heading: pygame.math.Vector2, vel: float = 10, size: int = 10) -> None:
        self.pos = pos.copy()
        self.heading = heading.copy()
        self.vel = vel
        self.age = 0
        self.size = size
        self.hitbox = pygame.Rect(0, 0, self.size, self.size)
        self.hitbox.center = self.pos
        self.__destroy = False

    def update(self):
        # update position and hitbox
        self.pos = self.pos + self.heading.normalize() * self.vel
        self.hitbox.center = self.pos
        self.age += 1

    def draw(self, window: pygame.Surface):
        pygame.draw.circle(window, (0, 0, 0), self.pos, self.size // 2)

    def hit_something(self, hitted_object: "Projectile"):
        # Destroy the hitted object and iself.
        self.destroy()
        hitted_object.destroy()

    # destroy setter
    def destroy(self):
        self.__destroy = True

    # destroy getter
    def get_destroy(self) -> bool:
        return self.__destroy

    def __str__(self) -> str:
        return f"projectile flying at {self.pos}"


class TankRound(Projectile):
    def __init__(self, pos: pygame.Vector2, heading: pygame.Vector2, vel: float = 10, size: int = 10) -> None:
        super().__init__(pos, heading, vel, size)


class Rocket(Projectile):
    """Advanced Projectile that homes onto a target."""

    def __init__(self, pos: pygame.Vector2, heading: pygame.Vector2, target: object, vel: float = 3, size: int = 20, agility: float = 1.0) -> None:
        super().__init__(pos, heading, vel, size)
        self.target = target
        self.agility = agility  # can rotate X degrees per frame
        self.rocket = pygame.image.load("rocket.png")
        self.smoke_trail = [self.pos.copy() for i in range(20)]

    def update(self):
        # update position and hitbox
        self.pos = self.pos + self.heading.normalize() * self.vel
        self.hitbox.center = self.pos

        # age
        self.age += 5

        # smoke trail
        if self.age % 4 == 0:
            for i, s in enumerate(self.smoke_trail):
                if i + 1 == len(self.smoke_trail):
                    self.smoke_trail[i] = self.pos
                else:
                    self.smoke_trail[i] = self.smoke_trail[i+1]

        # home target
        target_direction = self.target.pos - self.pos
        angle_CCW = angle_between_vectors(
            self.heading, target_direction)

        # steer rocket
        if angle_CCW > 2:
            self.heading = self.heading.rotate(self.agility)
        if angle_CCW < -2:
            self.heading = self.heading.rotate(-self.agility)

    def draw(self, window: pygame.Surface):
        # smoke trail
        color = (230, 230, 230)
        width = 1
        for i, s in enumerate(self.smoke_trail):
            if i == len(self.smoke_trail) - 1:
                pygame.draw.line(window, color,
                                 s, self.pos, width)
            else:
                pygame.draw.line(window, color, s,
                                 self.smoke_trail[i+1], width)
            width += 1

        # rocket
        angle = pygame.math.Vector2(0, -1).angle_to(self.heading)
        rotated = pygame.transform.rotate(self.rocket, - angle)
        offset = pygame.math.Vector2(rotated.get_rect().center)
        window.blit(rotated, self.pos - offset)

    def __str__(self) -> str:
        return f"rocket flying at {self.pos} heading {self.heading}"


class ProjectileCollection:
    """Projectile environment. All Projectiles must live within the same projectile collection."""

    def __init__(self) -> None:
        self.alive_projectiles = []
        self.destruct_projectiles = []
        self.max_age = 3200

    def update(self):
        for p in self.alive_projectiles:
            p.update()
            if p.age > self.max_age:
                self.destruct_projectiles.append(p)

            # check for collisions with other projectiles
            collides_with = p.hitbox.collidelistall(
                [i.hitbox for i in self.alive_projectiles])

            for c in collides_with:
                # avoid self collison
                if p != self.alive_projectiles[c]:
                    p.hit_something(self.alive_projectiles[c])

            # destroy projectile if hit
            if p.get_destroy():
                self.destruct_projectiles.append(p)

        self.destroy_projectiles()

    def destroy_projectiles(self):
        for p in self.destruct_projectiles:
            if p in self.alive_projectiles:
                self.alive_projectiles.remove(p)
        self.destruct_projectiles = []

    def draw(self, window: pygame.Surface):
        for p in self.alive_projectiles:
            p.draw(window)

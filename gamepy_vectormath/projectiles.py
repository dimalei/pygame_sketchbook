# class defing projectiles and projectile environments (collections)
import pygame
import math

import pygame.locals


class Projectile:
    """Base projectile that the tank can shoot."""

    def __init__(self, pos: pygame.math.Vector2, heading: pygame.math.Vector2, vel: float = 10) -> None:
        self.pos = pos.copy()
        self.heading = heading.copy()
        self.vel = vel
        self.age = 0

    def update(self):
        self.pos = self.pos + self.heading.normalize() * self.vel
        self.age += 1

    def draw(self, window: pygame.Surface):
        pygame.draw.circle(window, (0, 0, 0), self.pos, 5)

    def __str__(self) -> str:
        return f"projectile flying at {self.pos}"


class Rocket(Projectile):
    """Advanced Projectile that homes onto a target."""

    def __init__(self, pos: pygame.Vector2, heading: pygame.Vector2, target: object, vel: float = 3) -> None:
        super().__init__(pos, heading, vel)
        self.target = target
        self.agility = 0.6  # can rotate X degrees per frame
        self.target_direction = pygame.math.Vector2(1, 0)
        self.rocket = pygame.image.load("rocket.png")
        self.smoke_trail = [self.pos.copy() for i in range(20)]

    def update(self):
        # fly
        self.pos = self.pos + self.heading.normalize() * self.vel

        # smoke trail
        if self.age % 4 == 0:
            for i, s in enumerate(self.smoke_trail):
                if i + 1 == len(self.smoke_trail):
                    self.smoke_trail[i] = self.pos
                else:
                    self.smoke_trail[i] = self.smoke_trail[i+1]

        # age
        self.age += 5

        # home target
        self.target_direction = self.target.pos - self.pos
        angle_CCW = self.angle_between_vectors(
            self.heading, self.target_direction)

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

    def angle_between_vectors(self, v1, v2):
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


class ProjectileCollection:
    """Projectile environment. All Projectiles must live within the same projectile collection."""

    def __init__(self) -> None:
        self.alive_projectiles = []
        self.destruct_projectiles = []
        self.max_age = 3600

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

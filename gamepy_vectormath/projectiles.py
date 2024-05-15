# class defing projectiles and projectile environments (collections)
import pygame
import math

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
    def __init__(self, pos: pygame.Vector2, heading: pygame.Vector2, target: object, vel: float = 1) -> None:
        super().__init__(pos, heading, vel)
        self.target = target
        self.agility = 1 # can rotate X degrees per frame
        self.target_direction = pygame.math.Vector2(1,0)
    
    def update(self):
        self.pos = self.pos + self.heading.normalize() * self.vel
        self.age += 5

        self.target_direction = self.target.pos - self.pos
        # self.target_direction = self.target_direction.rotate(5)
        
        ################################
        # this part does not work!
        ################################
        angle_CCW = pygame.math.Vector2(-1,0).angle_to(self.heading) - pygame.math.Vector2(-1,0).angle_to(self.target_direction)

        # steer rocket
        if angle_CCW > 2 and angle_CCW:
            self.heading = self.heading.rotate(-self.agility)
        if angle_CCW < -2 and angle_CCW:
            self.heading = self.heading.rotate(+self.agility)

    def draw(self, window: pygame.Surface):
        pygame.draw.circle(window, (0, 0, 255), (self.pos[0], self.pos[1]), 10)
        pygame.draw.line(window, (0,0,0), self.pos, self.pos + self.heading * 50, 5)
        pygame.draw.line(window, (0,255,0), self.pos, self.pos + self.target_direction * 5, 2)

    def __str__(self) -> str:
        return f"rocket flying at {self.pos} heading {self.heading}"


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

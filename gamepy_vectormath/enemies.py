import pygame
from projectiles import Rocket, ProjectileCollection, TankRound
import math
from helpers import angle_between_vectors


class RocketPod:
    """The enemy of the game"""

    def __init__(self, pos: pygame.math.Vector2, collection: ProjectileCollection, target: object) -> None:
        self.pos = pos
        self.base = pygame.image.load("rocket_pod_base.png")
        self.tower = pygame.image.load("rocket_pod_tower.png")
        self.heading = pygame.math.Vector2(0, 1)
        self.timer = 90
        self.collection = collection
        self.target = target
        self.health = 100
        self.agility = 0.5
        self.hitbox = pygame.Rect(0, 0, 100, 100)
        self.hitbox.center = self.pos

    def update(self):
        """launches rockets every X seconds and turns itself into the players direction"""

        if self.timer > 0:
            self.timer -= 1
        else:
            self.launch_rocket()
            self.timer = 120

        target_direction = self.target.pos - self.pos
        angle_CCW = angle_between_vectors(
            self.heading, target_direction)

        # steer rocket
        if angle_CCW > self.agility:
            self.heading = self.heading.rotate(self.agility)
        elif angle_CCW < -self.agility:
            self.heading = self.heading.rotate(-self.agility)
        else:
            self.heading = target_direction.normalize()

    def launch_rocket(self):
        self.collection.alive_projectiles.append(
            Rocket(self.pos, self.heading, self.target, vel=3.5, agility=2))

    def get_hit(self, items: list):
        for i in items:
            if self.hitbox.colliderect(i.hitbox):
                # only count hits form the rocket class.
                if isinstance(i, TankRound):
                    print(f"got a hit from: {type(i)}")
                    i.destroy()
                    self.health -= 5

    def draw(self, window: pygame.Surface):
        offset_b = pygame.math.Vector2(self.base.get_rect().center)
        window.blit(self.base, self.pos - offset_b)

        direction_tower = pygame.math.Vector2(0, -1).angle_to(self.heading)
        tower = pygame.transform.rotate(self.tower, - direction_tower),
        offset_t = pygame.math.Vector2(tower[0].get_rect().center)
        window.blit(tower[0], self.pos - offset_t)

    def draw_ui(self, window: pygame.Surface):
        font = pygame.font.Font(None, 24)
        health_str = f"Enemy Health: {self.health}"
        health = font.render(health_str, True,  (10, 10, 10))
        x_offset = pygame.display.get_surface().get_size()[
            0] - health.get_rect()[2] - 10
        window.blit(health, (x_offset, 10))

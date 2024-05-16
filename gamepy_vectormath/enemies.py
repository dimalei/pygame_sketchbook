import pygame
from projectiles import Rocket, ProjectileCollection
import math


class RocketPod:
    """The enemy of the game"""

    def __init__(self, pos: pygame.math.Vector2, collection: ProjectileCollection, target: object) -> None:
        self.pos = pos
        self.base = pygame.image.load("rocket_pod_base.png")
        self.tower = pygame.image.load("rocket_pod_tower.png")
        self.heading = pygame.math.Vector2(0, 1)
        self.timer = 0
        self.collection = collection
        self.target = target
        self.health = 100
        self.agility = 0.5
        self.hitbox = pygame.Rect(0, 0, 100, 100)
        self.hitbox.center = self.pos

    def update(self):
        """launches rockets every X seconds and turns itself into the players direction"""

        self.timer += 1
        if self.timer > 300:
            self.launch_rocket()
            self.timer = 0

        target_direction = self.target.pos - self.pos
        angle_CCW = self.angle_between_vectors(
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
            Rocket(self.pos, self.heading, self.target))

    def angle_between_vectors(self, v1, v2):
        """returns the angle in between v1 and v2 from 180° to -180°"""

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

import pygame
from random import randint

## to do
# hearts, speed power ups

class Item:
    def __init__(self, pos: pygame.math.Vector2) -> None:
        self.pos = pos
        self.size = 50
        self.hitbox = pygame.Rect(0, 0, self.size, self.size)
        self.hitbox.center = self.pos
        self.sprite = pygame.image.load("crate.png")
        self.collected = False

    def draw(self, window: pygame.Surface):
        offset = pygame.math.Vector2(self.sprite.get_rect().center)
        window.blit(self.sprite, self.pos - offset)

    def collect(self):
        self.collected = True

class AmmoCrate(Item):
    def __init__(self, pos: pygame.Vector2) -> None:
        super().__init__(pos)
        self.sprite = pygame.image.load("crate.png")
        self.type = "ammo"

class HealthCrate(Item):
    def __init__(self, pos: pygame.Vector2) -> None:
        super().__init__(pos)
        self.sprite = pygame.image.load("health.png")
        self.type = "health"

class BoostCrate(Item):
    def __init__(self, pos: pygame.Vector2) -> None:
        super().__init__(pos)
        self.sprite = pygame.image.load("no2.png")
        self.type = "boost"

class ItemCollection:
    def __init__(self, max_items: int = 2) -> None:
        self.items = []
        self.destruct_items = []
        self.max_items = max_items
        self.timer = 0
        self.boundries = pygame.display.get_surface().get_size()

    def upate(self):
        # spawn new items
        self.timer += 1
        if self.timer > 300 and len(self.items) < self.max_items:
            self.spawn_item()
            self.timer = 0
        
        # destroy collected
        for c in self.items:
            if c.collected:
                self.destruct_items.append(c)
        
        self.destroy_crates()

    def spawn_item(self):
        rand = randint(0,8)
        if rand == 1:
            new_crate = HealthCrate(pygame.math.Vector2(
                randint(0, self.boundries[0]), randint(0, self.boundries[1])))
            self.items.append(new_crate)
        elif rand == 2:
            new_crate = BoostCrate(pygame.math.Vector2(
                randint(0, self.boundries[0]), randint(0, self.boundries[1])))
            self.items.append(new_crate)
        else:
            new_crate = AmmoCrate(pygame.math.Vector2(
                randint(0, self.boundries[0]), randint(0, self.boundries[1])))
            self.items.append(new_crate)


    def destroy_crates(self):
        for c in self.destruct_items:
            if c in self.items:
                self.items.remove(c)
        self.destruct_items = []

    def draw(self, window: pygame.Surface):
        for c in self.items:
            c.draw(window)
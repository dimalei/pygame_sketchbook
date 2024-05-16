import pygame
from projectiles import Projectile, Rocket, ProjectileCollection
from items import ItemCollection
from tank import Tank, TankController


class RocketPod:
    def __init__(self, collection: ProjectileCollection, target: object) -> None:
        self.pos = pygame.math.Vector2(400, 100)
        self.timer = 0
        self.collection = collection
        self.target = target

    def update(self):
        self.timer += 1
        if self.timer > 300:
            self.launch_rocket()
            self.timer = 0

    def launch_rocket(self):
        self.collection.alive_projectiles.append(
            Rocket(self.pos, pygame.math.Vector2(0, 1), self.target))

    def draw(self, window: pygame.Surface):
        pygame.draw.circle(window, (255, 0, 0), self.pos, 10)


class TankApp:
    def __init__(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((800, 600))
        self.player = TankController(Tank())
        self.projectiles = ProjectileCollection()
        self.enemy = RocketPod(self.projectiles, self.player.tank)
        self.crates = ItemCollection()

    def run(self):
        while True:
            self.events()

            self.player.update()
            self.crates.upate()
            self.player.pickup_items(self.crates.items)
            self.enemy.update()
            self.projectiles.update()

            self.render()
            self.clock.tick(60)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                self.player.steer_body(event)
            if event.type == pygame.MOUSEMOTION:
                self.player.steer_tower()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.player.shoot(self.projectiles)

    def render(self):
        self.window.fill((200, 200, 200))

        self.crates.draw(self.window)
        self.projectiles.draw(self.window)
        self.player.draw(self.window)
        self.enemy.draw(self.window)
        self.player.draw_ui(self.window)

        # pygame.draw.circle(self.window, (0, 0, 255), pygame.mouse.get_pos(), 5)
        pygame.display.flip()


app = TankApp()
app.run()

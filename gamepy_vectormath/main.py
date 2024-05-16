import pygame
from projectiles import Projectile, Rocket, ProjectileCollection
from items import ItemCollection
from tank import Tank, TankController
from enemies import RocketPod

class TankApp:
    def __init__(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((800, 600))
        self.player = TankController(Tank())
        self.projectiles = ProjectileCollection()
        self.enemy = RocketPod(pygame.math.Vector2(
            400, 300), self.projectiles, self.player.tank)
        self.crates = ItemCollection()

    def run(self):
        while True:
            self.events()

            self.player.update()
            self.crates.upate()
            self.player.pickup_items(self.crates.items)
            self.player.get_hit(self.projectiles.alive_projectiles)
            self.enemy.get_hit(self.projectiles.alive_projectiles)
            self.enemy.update()
            self.projectiles.update()

            self.render()

            if self.player.health <= 0:
                self.game_over()
                break
            if self.enemy.health <= 0:
                self.game_won()
                break

            self.clock.tick(60)

    def game_over(self):
        pass

    def game_won(self):
        pass

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                self.player.steer_body(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.player.shoot(self.projectiles)

    def render(self):
        self.window.fill((200, 200, 200))

        self.enemy.draw(self.window)
        self.crates.draw(self.window)
        self.projectiles.draw(self.window)
        self.player.draw(self.window)

        self.player.draw_ui(self.window)
        self.enemy.draw_ui(self.window)

        # pygame.draw.circle(self.window, (0, 0, 255), pygame.mouse.get_pos(), 5)
        pygame.display.flip()


app = TankApp()
app.run()

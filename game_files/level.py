from dependencies import *

class Level():
    def __init__(self) -> None:
        self.tiles = pygame.sprite.Group()
        self.gun_spawners = pygame.sprite.Group()
        self.player_spawners = pygame.sprite.Group()


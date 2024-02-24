from dependencies import *

class Level():
    """structure for holding all of the sprites in a level
    """
    def __init__(self) -> None:
        self.tiles = pygame.sprite.Group()
        self.gun_spawners = pygame.sprite.Group()
        self.player_spawners = pygame.sprite.Group()


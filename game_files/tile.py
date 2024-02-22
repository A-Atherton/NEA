from dependencies import *

class Tile(pygame.sprite.Sprite):
    """structure for holding all of the variables of a tile

    Args:
        pygame (_type_): _description_
    """
    def __init__(self, position, size: int, collision: bool, asset_path: str) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.abspath("assets/tile/" + asset_path))
        #self.image = pygame.Surface((size, size))
        #tile_image = pygame.image.load(os.path.abspath("assets/tile/" + asset_path))
        #self.image.blit(tile_image, (0,0))
        self.rect = self.image.get_rect(topleft = position)
        self.collision = collision
        self.health = 5
        
    def damage(self, damage_amount):
        self.health -= damage_amount
        if self.health <= 0:
            self.kill()

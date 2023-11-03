from constants import *
from dependencies import *

class Weapon(pygame.sprite.Sprite):
    def __init__( self, name: str, shoot: bool, ammo: int, firerate: float, asset_path: str, bullet_speed: int, position:pygame.Vector2) -> None:
        super().__init__()
        position += OFFSET_OF_GUN_FROM_PLAYER
        self.asset_path = asset_path
        self.name = name
        self.shoot = shoot #does the weapon shoot
        self.ammo_in_weapon = ammo #ammount of ammo left in the weapon
        self.firerate = firerate
        self.bullet_speed = bullet_speed
        self.image = pygame.image.load(os.path.abspath("assets/weapons/" + self.asset_path))
        self.rect = self.image.get_rect(topleft= position)
    
    def update(self, position):
        position += OFFSET_OF_GUN_FROM_PLAYER
        self.rect.x = position.x
        self.rect.y = position.y
        
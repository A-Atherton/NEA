from tile import Tile
from dependencies import *
from weapons import *

class Gun_Spawner(Tile):
    """structure for holding all of the variables of a gun_spawner

    Args:
        Tile (_type_): _description_
    """
    def __init__(self, position, size: int, collision: bool, asset_path: str, game:object) -> None:
        super().__init__(position, size, collision, asset_path)
        self.time_of_last_spawn = 0
        self.game = game
        
    def update(self):
        if pygame.time.get_ticks() - self.time_of_last_spawn >= 10_000 and len(self.game.weapons) < WEAPON_CAP_AMOUNT:
            self.spawn_gun()
        
    def spawn_gun(self):
        self.game.weapons.add(Ak47(pygame.Vector2(self.rect.x, self.rect.y)))
        self.time_of_last_spawn = pygame.time.get_ticks()


class Player_Spawner(Tile):
    """structure for holding all of the variables of a player spawner

    Args:
        Tile (_type_): _description_
    """
    def __init__(self, position, size: int, collision: bool, asset_path: str) -> None:
        super().__init__(position, size, collision, asset_path)
        self.used = False
        
from constants import *
from dependencies import *
from weapon import Weapon
    
#weapons
class Ak47(Weapon):
    def __init__(self, position: pygame.Vector2) -> None:
        super().__init__("ak47", True, 30, 0.2, "ak47.png", 30, position)

class Smg(Weapon): #Needs assets
    def __init__(self, position) -> None:
        super().__init__("smg", True, 25, 0.07, None, 30, position)

class Sword(Weapon): #Needs assets
    def __init(self, position) -> None:
        super().__init__("sword", False, 0, 0, None, 0, position)

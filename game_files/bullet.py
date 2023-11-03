from dependencies import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position: tuple, velocity: tuple) -> None:
        super().__init__()
        self.image = pygame.surface.Surface((6,6))
        self.image.fill((255, 187, 92))
        self.rect = self.image.get_rect(topleft = position)
        self.velocity = velocity
        self.lifetime = 10000
        self.birth_time = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        
        current_time = pygame.time.get_ticks()
        if self.birth_time - current_time > self.lifetime: # kills the bullet after 10 seconds which avoids
            self.kill()                                     
        
      
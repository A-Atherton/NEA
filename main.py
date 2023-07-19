import pygame
import numpy as np
import pygame_widgets
from pygame_widgets.button import Button

class RidgidBody():
    def __init__(self, position: list, mass: int) -> None: #takes in a position as a vector and mass as a scalar
        self.position = np.array(position)
        self.velocity = np.array([0,0])
        self.acceleration = np.array([0,0])
        self.mass = np.array(mass)
    
    def add_force(self, force:list): 
        self.acceleration += np.array(force) // self.mass

    def update(self):
        self.velocity += self.acceleration
        self.position += self.velocity
        if self.position <= 720:
            self.velocity *= -1
        #friction
        

ball = RidgidBody([100,300], 2)

class Player(RidgidBody):
    def __init__(self, position: list, mass: int) -> None:
        super().__init__(position, mass)
        
class Level():
    def __init__(self, layout, level_ID):
        self.layout = layout
        self.level_ID = level_ID
        self.tile_size = 64 

    def display(self):
        for row_index, row in enumerate(self.layout):
            for col_index, cell in enumerate(row):
                x = col_index * self.tile_size
                y = row_index * self.tile_size

class Tile(pygame.sprite.Sprite):
    def __init__(self, position, size) -> None:
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill("grey")
        self.rect = self.image.get_rect(topleft = position)

#Pygame Setup

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

#Main loop

while running:

    #Events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    pygame_widgets.update(events)
    
    #Render
    screen.fill('white')
    
    pygame.display.flip()

    clock.tick(60)

pygame.quit()

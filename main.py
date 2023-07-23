import pygame
import pygame_widgets
from pygame_widgets.button import Button
import os
import numpy as np

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

class Player(pygame.sprite.Sprite):
    def __init__(self,) -> None:
        super().__init__()
    
    def move(direction):
        if direction == 'up':
            pass
        
class Level():
    def __init__(self, layout, surface) -> None:
        self.layout = layout
        self.tile_size = 64
        self.display_surface = surface
        self.level_setup()

    def level_setup(self) -> None:
        self.tiles = pygame.sprite.Group()
        for row_index, row in enumerate(self.layout):
            for col_index, cell in enumerate(row):
                x = col_index * self.tile_size
                y = row_index * self.tile_size
                if cell == "X":
                    self.tiles.add(Tile((x,y),self.tile_size))

    def display(self) -> None:
        self.tiles.draw(self.display_surface)

class Tile(pygame.sprite.Sprite):
    def __init__(self, position, size) -> None:
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill('black')
        self.rect = self.image.get_rect(topleft = position)

levels_list = []

def load_levels(surface):
    with os.scandir('levels/') as entries:
        for entry in entries:
            level_layout = []
            with open(entry, 'r') as level:
                for line in level:
                    level_layout.append(line.rstrip("\n"))                    
            levels_list.append(Level(level_layout, surface))

#CONSTANTS
GRAVITY = 0.1
FRAMERATE = 60

#Pygame Setup
pygame.init()
screen = pygame.display.set_mode((1024,576))
clock = pygame.time.Clock()
running = True

load_levels(screen)

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
    levels_list[0].display()
    pygame.display.flip()

    #Clock
    clock.tick(FRAMERATE)

pygame.quit()

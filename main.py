import pygame
import pygame_widgets
from pygame_widgets.button import Button
import os
import numpy as np

#CONSTANTS
FRAMERATE = 60

"""
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
"""

class Player(pygame.sprite.Sprite):
    def __init__(self,position) -> None:
        super().__init__()
        self.image = pygame.Surface((20,32))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft = position)
        self.direction = pygame.Vector2(0,0)

        self.speed = 8
        self.gravity = .8
        self.jump_speed = -16
        self.jump_counter = 1
    
    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.direction.x = self.speed
        elif keys[pygame.K_a]:
            self.direction.x = -self.speed
        else:
            self.direction.x = 0
        if keys[pygame.K_w] and self.jump_counter > 0:
            self.jump()

    def apply_gravity(self):
        self.direction.y += self.gravity

    def jump(self):
        self.direction.y = self.jump_speed
        self.jump_counter -= 1
        

    def update(self):
        self.get_input()
        self.apply_gravity()


        
class Level():
    def __init__(self, layout, surface) -> None:
        self.layout = layout
        self.tile_size = 64
        self.display_surface = surface
        self.level_setup()

    def level_setup(self) -> None:
        self.tiles = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        for row_index, row in enumerate(self.layout):
            for col_index, cell in enumerate(row):
                x = col_index * self.tile_size
                y = row_index * self.tile_size
                if cell == "X":
                    self.tiles.add(Tile((x,y),self.tile_size))
                if cell == "P":
                    self.players.add(Player((x,y)))

    def collision_check(self):
        for player in self.players.sprites():

            #horizontal check
            player.rect.x += player.direction.x
            for tile in self.tiles.sprites():
                if tile.rect.colliderect(player.rect):
                    if player.direction.x > 0:
                        player.rect.right = tile.rect.left
                    elif player.direction.x < 0:
                        player.rect.left = tile.rect.right
            
            #verticle check
            player.rect.y += player.direction.y
            for tile in self.tiles.sprites():
                if tile.rect.colliderect(player.rect):
                    if player.direction.y < 0:
                        player.rect.top = tile.rect.bottom
                        player.direction.y = 0
                    elif player.direction.y > 0:
                        player.rect.bottom = tile.rect.top
                        player.jump_counter = 1
                        player.direction.y = 0


    def run(self) -> None:
        for player in self.players:
            player.update()
        self.collision_check()
        self.tiles.draw(self.display_surface)
        self.players.draw(self.display_surface)
        

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
    levels_list[0].run()
    pygame.display.flip()


    #Clock
    clock.tick(FRAMERATE)

pygame.quit()

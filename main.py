import pygame
import pygame_widgets
from pygame_widgets.button import Button
import os
import numpy as np

from pygame_widgets.textbox import TextBox


#CONSTANTS
FRAMERATE = 60
AIM_INDICATOR_DISTANCE_FROM_PLAYER = 50


class Weapon(pygame.sprite.Sprite):
    def __init__(self, name: str, shoot: bool, ammo: int, firerate: float, asset_path:str, bullet_speed: int) -> None:
        super().__init__()
        self.asset_path = asset_path
        self.name = name
        self.shoot = shoot #does the weapon shoot
        self.ammo_in_weapon = ammo #ammount of ammo left in the weapon
        self.firerate = firerate
        self.bullet_speed = bullet_speed

class Ak47(Weapon):
    def __init__(self, position) -> None:
        super().__init__("ak47", True, 30, 0.2, "ak47.png", 30)
        self.image = pygame.image.load(os.path.abspath("assets/weapons/" + self.asset_path))
        self.rect = self.image.get_rect(topleft= position)
    
    def update(self, position):
        self.rect.x = position.x
        self.rect.y = position.y


class Bullet(pygame.sprite.Sprite):
    def __init__(self, position: tuple, velocity: tuple) -> None:
        super().__init__()
        self.image = pygame.surface.Surface((6,6))
        self.image.fill((255, 187, 92))
        self.rect = self.image.get_rect(topleft = position)
        self.velocity = velocity
        self.lifetime = 20
        self.birth_time = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if self.lifetime > self.birth_time:
            self.kill()
        

class Player(pygame.sprite.Sprite):
    def __init__(self,position,joystick_id) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.abspath("assets/player/player.png"))
        self.rect = self.image.get_rect(topleft = position)
        self.direction = pygame.Vector2(0,0)
        self.controller = pygame.joystick.Joystick(joystick_id)
        self.aim_direction = pygame.Vector2(0,0)
        self.time_of_last_shot = 0

        #movement
        self.speed = 6
        self.gravity = .8
        self.jump_speed = -16
        self.jump_counter = 1

        #combat
        self.health = 100
        self.holding = None
    
    def get_input(self):
        """
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_d]:
            self.direction.x = self.speed
        elif keys[pygame.K_a]:
            self.direction.x = -self.speed
        else:
            self.direction.x = 0
        if keys[pygame.K_w] and self.jump_counter > 0:
            self.jump()
        """

        #controller
        if self.controller.get_button(0) and self.jump_counter > 0: #A
            self.jump()
        if self.controller.get_button(1): #B
            pass
        if self.controller.get_button(2): #X
            pass
        if self.controller.get_button(3): #Y
            pass

        if self.controller.get_axis(0) > 0.2 or self.controller.get_axis(0) < -0.2: #x +ve
            self.direction.x = self.speed * self.controller.get_axis(0)
        else:
            self.direction.x = 0

        #shooting

        time_since_last_shot = pygame.time.get_ticks()- self.time_of_last_shot 

        if self.controller.get_axis(5) > -0.5 and self.holding != None and self.holding.shoot == True and self.holding.ammo_in_weapon > 0 and time_since_last_shot > self.holding.firerate * 1000:
            self.shoot(self.holding.bullet_speed)
            self.holding.ammo_in_weapon -= 0
            self.time_of_last_shot = pygame.time.get_ticks()
        
    def apply_gravity(self):
        self.direction.y += self.gravity

    def jump(self):
        self.direction.y = self.jump_speed
        self.jump_counter -= 1
    
    def update(self):
        self.get_input()
        self.apply_gravity()
        if self.holding != None:
            self.holding.update(pygame.Vector2(self.rect.x, self.rect.y))

    def get_aim_direction(self): #draws the direction that the player is aiming
        x_offset = self.controller.get_axis(2)
        y_offset = self.controller.get_axis(3)
        
        self.aim_direction = pygame.Vector2(x_offset, y_offset)

        aim_cursor_position = (self.rect.x + self.aim_direction.x * AIM_INDICATOR_DISTANCE_FROM_PLAYER + 10,
                               self.rect.y + self.aim_direction.y * AIM_INDICATOR_DISTANCE_FROM_PLAYER + 16)
        pygame.draw.circle(screen, "white", aim_cursor_position, 4)
    
    def shoot(self, bullet_speed):
        
        current_level.bullets.add(Bullet((self.rect.x + 10,self.rect.y + 16),
                                          (self.aim_direction.x * bullet_speed, self.aim_direction.y * bullet_speed)))
    
    def pick_up(self):
        self.holding = Ak47((self.rect.x, self.rect.y))
        current_level.weapons.add(self.holding)
        

        
        

        
class Level():
    def __init__(self, layout, surface) -> None:
        self.layout = layout
        self.tile_size = 32
        self.display_surface = surface
        self.number_of_players = pygame.joystick.get_count()
        self.level_setup()


    def level_setup(self) -> None:
        self.tiles = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.weapons = pygame.sprite.Group()
        joystick_id = 0
        for row_index, row in enumerate(self.layout):
            for col_index, cell in enumerate(row):
                x = col_index * self.tile_size
                y = row_index * self.tile_size
                if cell == "X":
                    self.tiles.add(Tile((x,y),self.tile_size, True, "standard_tile.png"))
                if cell == "P" and self.number_of_players > 0:
                    self.players.add(Player((x,y), joystick_id))
                    self.number_of_players -= 1
                    joystick_id += 1
                if cell == "S":
                    self.tiles.add(Tile((x,y),self.tile_size, False, "gun_spawn.png"))
                    

    def player_collision_check(self) -> None:
        for player in self.players.sprites():

            #horizontal check
            player.rect.x += player.direction.x
            for tile in self.tiles.sprites():
                if tile.rect.colliderect(player.rect) and tile.collision == True:
                    if player.direction.x > 0:
                        player.rect.right = tile.rect.left
                    elif player.direction.x < 0:
                        player.rect.left = tile.rect.right
            
            #verticle check
            player.rect.y += player.direction.y
            for tile in self.tiles.sprites():
                if tile.rect.colliderect(player.rect) and tile.collision == True:
                    if player.direction.y < 0:
                        player.rect.top = tile.rect.bottom
                        player.direction.y = 0
                    elif player.direction.y > 0:
                        player.rect.bottom = tile.rect.top
                        player.jump_counter = 1
                        player.direction.y = 0
    
    def bullet_collision_check(self) -> None: #kills the bullet if it hits a solid tile
        for bullet in self.bullets.sprites():
            for tile in self.tiles.sprites():
                if tile.rect.colliderect(bullet.rect) and tile.collision == True:
                    bullet.kill()




    def run(self) -> None:

        self.players.update()
        self.bullets.update()
        self.player_collision_check()
        self.bullet_collision_check()
        self.tiles.draw(self.display_surface)
        for player in self.players:
            player.get_aim_direction()
        self.players.draw(self.display_surface)
        self.bullets.draw(self.display_surface)
        self.weapons.draw(self.display_surface)
        

class Tile(pygame.sprite.Sprite):
    def __init__(self, position, size: int, collision: bool, asset_path: str) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.abspath("assets/tile/" + asset_path))
        #self.image = pygame.Surface((size, size))
        #tile_image = pygame.image.load(os.path.abspath("assets/tile/" + asset_path))
        #self.image.blit(tile_image, (0,0))
        self.rect = self.image.get_rect(topleft = position)
        self.collision = collision

class Gun_Spawner(Tile):
    def __init__(self, position, size: int, collision: bool, asset_path: str) -> None:
        super().__init__(position, size, collision, asset_path)
    

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

background = pygame.image.load(os.path.abspath("assets/background/Background.png"))

load_levels(screen)

current_level_counter = 0

#Main loop
while running:

    #Events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                current_level_counter += 1
            if event.key == pygame.K_0:
                for player in current_level.players:
                    player.pick_up()

    pygame_widgets.update(events)

    #Render
    screen.blit(background, (0,0))

    current_level = levels_list[current_level_counter % len(levels_list)]
    current_level.run()
    
    pygame.display.flip()

    #Clock
    clock.tick(FRAMERATE)

pygame.quit()

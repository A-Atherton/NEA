import pygame
import pygame_widgets
from pygame_widgets.button import Button
import os
import math
import random
from pygame_widgets.textbox import TextBox


#CONSTANTS
FRAMERATE = 60
AIM_INDICATOR_DISTANCE_FROM_PLAYER = 50
OFFSET_OF_GUN_FROM_PLAYER = pygame.Vector2(0,0)
WEAPON_CAP_AMOUNT = 6
WEAPON_SPAWN_RATE_IN_MILLIS = 10_000
PLAYER_ACCELERATION_RATE = 0.38
PLAYER_FRICTION = 0.1
PLAYER_MAX_VELOCITY = 5

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
        """
        if self.birth_time > self.lifetime:
            self.kill()
        """

class Player(pygame.sprite.Sprite):
    def __init__( self, position, controller_player, joystick=None ) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.abspath("assets/player/player.png"))
        self.rect = self.image.get_rect(topleft = position)
        self.velocity = pygame.Vector2(0,0)
        self.acceleration = pygame.Vector2(0,0)
        self.controller_player = controller_player
        if controller_player:
            self.controller = joystick

        self.aim_velocity = pygame.Vector2(0,0)
        self.time_of_last_shot = 0 
        self.flip = False
        self.spawned = False
        self.dead = False

        #movement
        self.speed = 6
        self.gravity = .8
        self.jump_speed = -16
        self.jump_counter = 1

        #combat
        self.health = 100
        self.holding = None
    
    def get_input(self):
        
        time_since_last_shot = pygame.time.get_ticks()- self.time_of_last_shot
        
        #controller
        if self.controller_player:
            if self.controller.get_button(0) and self.jump_counter > 0: #A
                self.jump()
            if self.controller.get_button(1): #B
                pass
            if self.controller.get_button(2): #X
                pass
            if self.controller.get_button(3): #Y
                self.holding = None

            if self.controller.get_axis(0) > 0.2 or self.controller.get_axis(0) < -0.2:
                 #x movement
                self.acceleration.x = PLAYER_ACCELERATION_RATE * self.controller.get_axis(0)
            
            else:
                self.velocity.x = 0

            #shooting 
            if self.controller.get_axis(5) > -0.5 and self.holding != None and self.holding.shoot == True and self.holding.ammo_in_weapon > 0 and time_since_last_shot > self.holding.firerate * 1000:
                self.shoot(self.holding.bullet_speed)
                self.holding.ammo_in_weapon -= 1
                self.time_of_last_shot = pygame.time.get_ticks()
        
        #keyboard player
        else:       
            keys = pygame.key.get_pressed()
            clicks = pygame.mouse.get_pressed(num_buttons=3)
            if keys[pygame.K_d]: #move right
                self.acceleration.x = PLAYER_ACCELERATION_RATE
            elif keys[pygame.K_a]: #move left
                self.acceleration.x = -PLAYER_ACCELERATION_RATE
            else:
                self.velocity.x = 0
            if keys[pygame.K_w] and self.jump_counter > 0: #jump
                self.jump()
            if keys[pygame.K_f]: #drop weapon 
                self.holding = None
            #shooting
            if clicks[0] and self.holding != None and self.holding.shoot == True and self.holding.ammo_in_weapon > 0 and time_since_last_shot > self.holding.firerate * 1000:
                self.shoot(self.holding.bullet_speed)
                self.holding.ammo_in_weapon -= 1
                self.time_of_last_shot = pygame.time.get_ticks()
        
    def apply_gravity(self):
        self.velocity.y += self.gravity

    def jump(self):
        self.velocity.y = self.jump_speed
        self.jump_counter -= 1

    def update(self):
        self.get_input()
        self.apply_gravity()
        if self.holding != None:
            self.holding.update(pygame.Vector2(self.rect.x, self.rect.y))
            if self.holding.ammo_in_weapon <= 0:
                self.holding.kill()
                self.holding = None
        if self.health <= 0:
            self.dead = True
        
        self.facing()

    def get_aim_direction(self): #draws the direction that the player is aiming
        if self.controller_player: #controller player
            right_x_offset = self.controller.get_axis(2)
            right_y_offset = self.controller.get_axis(3)
            
            right_distance = math.sqrt(right_x_offset ** 2 + right_y_offset ** 2)

            if right_distance > 0.1:
                self.aim_direction = pygame.Vector2(right_x_offset / right_distance, right_y_offset/ right_distance)

            else:
                
                left_x_offset = self.controller.get_axis(0)
                left_y_offset = self.controller.get_axis(1)
                left_distance = math.sqrt(left_x_offset ** 2 + left_y_offset ** 2)

                if left_distance > 0.1:
                    self.aim_direction = pygame.Vector2(left_x_offset / left_distance, left_y_offset/ left_distance)

                    
                else:
                    random_x_offset = (2 * random.random()) - 1
                    random_y_offset = (2 * random.random()) - 1
                    
                    random_distance = math.sqrt(random_x_offset ** 2 + random_y_offset ** 2)
                    self.aim_direction = pygame.Vector2(random_x_offset / random_distance, random_y_offset/ random_distance)

            aim_cursor_position = (self.rect.x + right_x_offset * AIM_INDICATOR_DISTANCE_FROM_PLAYER + 10,
                                self.rect.y + right_y_offset * AIM_INDICATOR_DISTANCE_FROM_PLAYER + 16)
            pygame.draw.circle(screen, "white", aim_cursor_position, 4)
            
        else: #keyboard player
            mouse_pos = pygame.mouse.get_pos()
            
            mouse_offset_from_player = (mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y)
            
            mouse_distance_from_player = math.sqrt(mouse_offset_from_player[0] ** 2 + mouse_offset_from_player[1] ** 2)
            
            if mouse_distance_from_player > 0:
                self.aim_direction = pygame.Vector2(mouse_offset_from_player[0] / mouse_distance_from_player, mouse_offset_from_player[1]/ mouse_distance_from_player)
            if mouse_distance_from_player > AIM_INDICATOR_DISTANCE_FROM_PLAYER:
                aim_cursor_position = (self.rect.x + self.aim_direction.x * AIM_INDICATOR_DISTANCE_FROM_PLAYER + 10,
                                    self.rect.y + self.aim_direction.y * AIM_INDICATOR_DISTANCE_FROM_PLAYER + 16)
            else: 
                aim_cursor_position = (self.rect.x + mouse_offset_from_player[0] + 10,
                                    self.rect.y + mouse_offset_from_player[1] + 16)
            pygame.draw.circle(screen, "white", aim_cursor_position, 4)        
        
    def shoot(self, bullet_speed):
        game.bullets.add(Bullet((self.rect.x + 10,self.rect.y + 16),
                                          (self.aim_direction.x * bullet_speed, self.aim_direction.y * bullet_speed)))
    
    def pick_up(self, weapon):
        self.holding = weapon
        game.weapons.add(self.holding)
        
    def do_damage(self, damage_amount: int):
        self.health -= damage_amount

    def facing(self):
        if self.velocity.x > 0:
            True
        else:
            self.flip = False
        self.image = pygame.transform.flip(pygame.image.load(os.path.abspath("assets/player/player.png")), self.flip, False)



class Game():
    def __init__(self, layouts, surface) -> None:
        self.tile_size = 32
        self.display_surface = surface
        self.number_of_players = pygame.joystick.get_count()
        self.levels = []
        self.level_setup(layouts)
        self.current_level_counter = 0
        self.current_level = self.levels[self.current_level_counter]
        self.keyboard_player_spawned = False
        
    def level_setup(self, layouts) -> None:
        #self.player_que = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.weapons = pygame.sprite.Group()
        joystick_id = 0
        
        for layout in layouts:
            temp = Level()
            self.levels.append(temp)
            for row_index, row in enumerate(layout):
                for col_index, cell in enumerate(row):
                    x = col_index * self.tile_size
                    y = row_index * self.tile_size
                    if cell == "X":
                        temp.tiles.add(Tile((x,y),self.tile_size, True, "standard_tile.png"))
                    if cell == "P":
                        temp.player_spawners.add(Player_Spawner((x,y),self.tile_size, False, "gun_spawn.png"))
                    if cell == "S":
                        temp.gun_spawners.add(Gun_Spawner((x,y),self.tile_size, False, "gun_spawn.png"))
                    if cell == " ":
                        pass
                        #self.tile.add(Tile((x,y), self.tile_size, False, ))
                   
    def player_collision_check(self,dt) -> None:
        for player in self.players.sprites():

            #horizontal check
            player.acceleration.x += player.velocity.x * PLAYER_FRICTION
            player.velocity.x += player.acceleration.x * dt
            print(player.velocity)
            player.velocity.x = max(-PLAYER_MAX_VELOCITY, min(player.velocity.x, PLAYER_ACCELERATION_RATE))
            print(player.velocity)
            if abs(player.velocity.x) < .01: player.velocity.x = 0
            player.rect.x += player.velocity.x * dt + (player.acceleration.x * .5) * (dt * dt)
            
            for tile in self.current_level.tiles.sprites():
                if tile.rect.colliderect(player.rect):
                    if tile.collision == True:
                        if player.velocity.x > 0:
                            player.rect.right = tile.rect.left
                        elif player.velocity.x < 0:
                            player.rect.left = tile.rect.right

            #verticle check
            player.rect.y += player.velocity.y
            for tile in self.current_level.tiles.sprites():
                if tile.rect.colliderect(player.rect):
                    if player.velocity.y < 0:
                        player.rect.top = tile.rect.bottom
                        player.velocity.y = 0
                        
                    elif player.velocity.y > 0:
                        player.rect.bottom = tile.rect.top
                        player.jump_counter = 1
                        player.velocity.y = 0
                        #player.jump_counter = 1
                else:
                        pass #player.jump_counter = 0

            #bullet check
            for bullet in self.bullets:
                if bullet.rect.colliderect(player.rect):
                    player.do_damage(15)
                    bullet.kill()
            #weapon check
            for weapon in self.weapons:
                if player.holding == None:
                    if weapon.rect.colliderect(player.rect):
                        player.holding = weapon

    def bullet_collision_check(self,dt) -> None: #kills the bullet if it hits a solid tile
        for bullet in self.bullets.sprites():
            for tile in self.current_level.tiles.sprites():
                if tile.rect.colliderect(bullet.rect) and tile.collision == True:
                    bullet.kill()
        
    def weapon_collision_check(self) -> None:
        
        for tile in self.current_level.tiles:
            pass
           
    def run(self) -> None:
        dt = clock.tick(60)*0.001*FRAMERATE
        self.players.update()
        self.bullets.update()
        self.current_level.gun_spawners.update()
        self.player_collision_check(dt)
        self.bullet_collision_check(dt)
        self.current_level.tiles.draw(self.display_surface)
        for player in self.players:
            player.get_aim_direction()
        self.weapons.draw(self.display_surface)
        self.players.draw(self.display_surface)
        self.bullets.draw(self.display_surface)
        self.current_level.gun_spawners.draw(self.display_surface)
        self.check_for_players()

    def check_for_players(self) -> None: #function to check for a new controller, add a new player and spawn them in the next level
        """
        for joy_itr in joysticks:
            if joy_itr.joystick.get_button(0):
                print("button pressed")
        """
        
        if pygame.key.get_pressed()[pygame.K_e] and not self.keyboard_player_spawned:
            self.players.add(Player((100,100), False))
            self.keyboard_player_spawned = True
            print("Keyboard player added")
        
    def next_level(self):
        self.current_level_counter += 1
        self.current_level = game.levels[game.current_level_counter % len(game.levels)]
        for weapon in self.weapons.sprites():
            weapon.kill()
        for bullet in self.bullets.sprites():
            bullet.kill()
        #self.players.hide()
        for player in self.players:
            player.spawned = False
            player.holding = None
        for spawner in self.current_level.player_spawners:
            spawner.used = False
        self.spawn_players()

    def spawn_players(self):
        for i, player in enumerate(self.players.sprites()):
            if not player.spawned:

                for spawner in self.current_level.player_spawners.sprites():

                    if not spawner.used:
                        player.rect.topleft = spawner.rect.topleft

                        spawner.used = True
                        break
                        
                
        
class Level():
    def __init__(self) -> None:
        self.tiles = pygame.sprite.Group()
        self.gun_spawners = pygame.sprite.Group()
        self.player_spawners = pygame.sprite.Group()


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
        self.time_of_last_spawn = 0
        
    def update(self):
        if pygame.time.get_ticks() - self.time_of_last_spawn >= 10_000 and len(game.weapons) < WEAPON_CAP_AMOUNT:
            self.spawn_gun()
        
    def spawn_gun(self):
        game.weapons.add(Ak47(pygame.Vector2(self.rect.x, self.rect.y)))
        self.time_of_last_spawn = pygame.time.get_ticks()


class Player_Spawner(Tile):
    def __init__(self, position, size: int, collision: bool, asset_path: str) -> None:
        super().__init__(position, size, collision, asset_path)
        self.used = False
        

class Joystick_Class():
    def __init__(self, joystick) -> None:
        self.joystick = joysticks
        self.spawned = False


def load_levels(surface):
    levels_list = []
    with os.scandir('levels/') as entries:
        for entry in entries:
            level_layout = []
            with open(entry, 'r') as level:
                for line in level:
                    level_layout.append(line.rstrip("\n"))                    
            levels_list.append(level_layout)
    
    global game
    game = Game(levels_list, screen)


#Pygame Setup
pygame.init()
screen = pygame.display.set_mode((1024,576), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True
pygame.mouse.set_visible(True)
background = pygame.image.load(os.path.abspath("assets/background/Background.png"))
load_levels(screen)
joysticks = []

#Main loop
while running:
    #Events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                game.next_level()
        
        if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks.append(Joystick_Class(joy))
                print("Joystick connected")
                game.players.add(Player((100,100), True, joystick=joy))
                

    
    pygame_widgets.update(events)

    #Render
    screen.blit(background, (0,0))
    game.run()
    
    pygame.display.flip()

    #Clock
    clock.tick(FRAMERATE)

pygame.quit()

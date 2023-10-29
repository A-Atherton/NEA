from dependencies import *
from constants import *
from level import Level
from player import Player
from tile import Tile
from spawners import Gun_Spawner, Player_Spawner

class Game():
    def __init__(self, layouts, surface, clock) -> None:
        self.tile_size = 32
        self.display_surface = surface
        self.clock = clock
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
            dt = 1
            #horizontal check
            player.acceleration.x += player.velocity.x * PLAYER_FRICTION
            player.velocity.x += player.acceleration.x * dt
            player.velocity.x = max(-PLAYER_MAX_VELOCITY, min(player.velocity.x, PLAYER_ACCELERATION_RATE))
            if abs(player.velocity.x) < .01: player.velocity.x = 0
            print(player.velocity.x * dt + (player.acceleration.x * .5) * (dt * dt))
            
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
        dt = self.clock.tick(60)*0.001*FRAMERATE
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
        self.current_level = self.levels[self.current_level_counter % len(self.levels)]
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
             
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
        """takes in the level layouts from the levels
        file and creates a level object for each layout

        Args:
            layouts (Array): 2D array of strings. Each array of strings represents the level layout of one layout
        """
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
                        temp.gun_spawners.add(Gun_Spawner((x,y),self.tile_size, False, "gun_spawn.png", self))
                    if cell == " ":
                        pass
                        #self.tile.add(Tile((x,y), self.tile_size, False, ))
                   
    def player_collision_check(self,dt) -> None:
        """checks for collisions between players and tiles, players and bullets, and players and weapons

        Args:
            dt (float): the time between now and the last frame (not currently being used)
        """
        for player in self.players.sprites():
            dt = 1
            #horizontal check
            player.rect.x += player.velocity.x
            
            for tile in self.current_level.tiles.sprites():
                if tile.rect.colliderect(player.rect):
                    if tile.collision == True:
                        if player.velocity.x > 0:
                            player.rect.right = tile.rect.left
                        elif player.velocity.x < 0:
                            player.rect.left = tile.rect.right

            #verticle check
            player.rect.y += player.velocity.y
            player.on_ground = False
            for tile in self.current_level.tiles.sprites():
                if tile.rect.colliderect(player.rect):
                    if player.velocity.y < 0:
                        player.rect.top = tile.rect.bottom
                        player.velocity.y = 0
                        
                    elif player.velocity.y > 0:
                        player.rect.bottom = tile.rect.top
                        player.jump_counter = 1
                        player.velocity.y = 0
                        player.on_ground = True
                        
            print(player.on_ground)
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

    def bullet_collision_check(self,dt) -> None:
        """checks for collisions between bullets and tiles

        Args:
            dt (float): the time between now and the last frame (not currently being used)
        """
        for bullet in self.bullets.sprites():
            for tile in self.current_level.tiles.sprites():
                if tile.rect.colliderect(bullet.rect) and tile.collision == True:
                    bullet.kill()
                    tile.kill()
        
    def weapon_collision_check(self, dt) -> None:
        """Checks for collision between weapons and tiles and stops the 
        weapon from moving if it collides with a tile (not currently being used)

        Args:
            dt (float): the time between now and the last frame (not currently being used)
        """
        
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
        self.check_for_new_players()
        if self.check_for_winner():
            print("someone won the round")
            self.next_level()
        

    def check_for_new_players(self) -> None: 
        """
        check for a new keyboard player (and controller in the future), add a new player and spawn them in the next level
        """
        
        if pygame.key.get_pressed()[pygame.K_e] and not self.keyboard_player_spawned:
            self.players.add(Player((100,100), False, self, self.display_surface))
            self.keyboard_player_spawned = True
            print("Keyboard player added")
        
    def next_level(self):
        """loads the next level and resets the players and weapons
        """
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
        """spawns the players in the level
        """
        for i, player in enumerate(self.players.sprites()):
            if not player.spawned:

                for spawner in self.current_level.player_spawners.sprites():

                    if not spawner.used:
                        player.rect.topleft = spawner.rect.topleft
                        player.health = 100
                        player.living = True
                        spawner.used = True
                        break
    def check_for_winner(self):
        """checks for a winner

        Returns:
            bool: winner or not
        """
        living_players = []
        for player in self.players:
            if player.living: living_players.append(player)
        print(living_players)
        
        if len(living_players) == 1 and len(self.players) > 1:
            return True
        
        elif len(self.players) == 1 and len(living_players) <= 0:
            return True
        
        elif len(living_players) == 0:
            return False
        
        else:
            return False
        
             
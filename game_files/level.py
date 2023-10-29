from dependencies import *

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
        self.spawners = pygame.sprite.Group()
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
                    self.spawners.add(Gun_Spawner((x,y),self.tile_size, False, "gun_spawn.png"))
                if cell == " ":
                    pass
                    #self.tile.add(Tile((x,y), self.tile_size, False, ))
                    
    def player_collision_check(self) -> None:
        for player in self.players.sprites():

            #horizontal check
            player.rect.x += player.direction.x
            for tile in self.tiles.sprites():
                if tile.rect.colliderect(player.rect):
                    if tile.collision == True:    
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

    def bullet_collision_check(self) -> None: #kills the bullet if it hits a solid tile
        for bullet in self.bullets.sprites():
            for tile in self.tiles.sprites():
                if tile.rect.colliderect(bullet.rect) and tile.collision == True:
                    bullet.kill()
        
    def weapon_collision_check(self) -> None:
        
        for tile in self.tiles:
            pass
           
    def run(self) -> None:
        self.players.update()
        self.bullets.update()
        self.spawners.update()
        self.player_collision_check()
        self.bullet_collision_check()
        self.tiles.draw(self.display_surface)
        for player in self.players:
            player.get_aim_direction()
        self.weapons.draw(self.display_surface)
        self.players.draw(self.display_surface)
        self.bullets.draw(self.display_surface)
        self.spawners.draw(self.display_surface)
        

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
        if pygame.time.get_ticks() - self.time_of_last_spawn >= 10_000 and len(current_level.weapons) < WEAPON_CAP_AMOUNT:
            self.spawn_gun()
        

    def spawn_gun(self):
        current_level.weapons.add(Ak47(pygame.Vector2(self.rect.x, self.rect.y)))
        self.time_of_last_spawn = pygame.time.get_ticks()

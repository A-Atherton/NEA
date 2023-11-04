from dependencies import *
from constants import *
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__( self, position, controller_player, game, display_surface, joystick=None ) -> None:
        super().__init__()
        
        temp = pygame.image.load(os.path.abspath("assets/player/player.png"))
        self.character_images = [ pygame.transform.flip(temp, True, False), temp]
        self.image = self.character_images[0]
        self.game_frame_counter = 0
        self.character_frame_counter = 0
        self.facing_left = True
        self.assign_image_arrays()
        
        self.rect = self.image.get_rect(topleft = position)
        self.game = game
        self.display_surface = display_surface
        self.controller_player = controller_player
        if controller_player: self.controller = joystick
        self.spawned = False
        self.dead = False
        

        #movement
        self.speed = 6
        self.gravity = .8
        self.jump_speed = -16
        self.jump_counter = 1
        self.velocity = pygame.Vector2(0,0)
        self.acceleration = pygame.Vector2(0,0)

        #combat
        self.health = 100
        self.holding = None
        self.time_of_last_shot = 0 
    
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
                self.acceleration.x = 0
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
        
        self.find_direction_facing()
        self.update_frame()

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
            pygame.draw.circle(self.display_surface, "white", aim_cursor_position, 4)
            
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
            pygame.draw.circle(self.display_surface, "white", aim_cursor_position, 4)        
        
    def shoot(self, bullet_speed):
        self.game.bullets.add(Bullet((self.rect.x + 10,self.rect.y + 16),
                                          (self.aim_direction.x * bullet_speed, self.aim_direction.y * bullet_speed)))
    
    def pick_up(self, weapon):
        self.holding = weapon
        self.game.weapons.add(self.holding)
        
    def do_damage(self, damage_amount: int):
        self.health -= damage_amount

    def find_direction_facing(self):
        if self.velocity.x > 0: self.facing_left = True
        else: self.facing_left = False
    
    def update_frame(self):
        self.game_frame_counter += 1

        if self.game_frame_counter % 2 == 0:
            self.character_frame_counter += 1
            self.image = self.idle_image_list[int(self.facing_left)][self.character_frame_counter % len(self.idle_image_list[0])]
            temp = self.rect.topleft
            self.rect = self.image.get_rect(topleft = temp)
        

    def load_sprites(self, path):
        """loads creates a list of images and a list of the flipped images when given the location of the folder

        Args:
            path (string): path of folder to extract images from

        Returns:
            _type_: _description_
        """
        frames_right = []
        frames_left = []
        with os.scandir(path) as entries:
            for entry in sorted(entries, key=lambda entry: entry.name):
                print(entry)
                temp = pygame.transform.scale_by(pygame.image.load(entry), 2)
                frames_right.append(temp)
                frames_left.append(pygame.transform.flip(temp, True, False))
            return (frames_left, frames_right)
    
    def assign_image_arrays(self):
        self.idle_image_list = self.load_sprites("assets/player/character_idle")
        self.run_image_list = self.load_sprites("assets/player/character_run")
    
    def move(self, position: pygame.Vector2):
        """moves the player to a specified position and sets their movement variables to 0

        Args:
            position (pygame.Vector2): position to move the player to
        """
        self.velocity = pygame.Vector2(0,0)
        self.acceleration = pygame.Vector2(0,0)
        self.rect.topleft = position
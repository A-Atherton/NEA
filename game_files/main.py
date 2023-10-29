from dependencies import *
from constants import *
from game import Game
from joystick_class import Joystick_Class
from player import Player
#CONSTANTS

def load_levels(surface):
    """takes all levels from the levels folder and converts the text files into a
    a list of strings (pretty much a 2D array). It adds these arrays into another
    array which is passed as an parameter

    Args:
        surface (a pygame surface): _description_
    """
    
    levels_list = []
    with os.scandir('levels/') as entries:
        for entry in entries:
            level_layout = []
            with open(entry, 'r') as level:
                for line in level:
                    level_layout.append(line.rstrip("\n"))                    
            levels_list.append(level_layout)
    
    global game
    game = Game(levels_list, surface)

#Pygame Setup
pygame.init()
screen = pygame.display.set_mode((1024,576))
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
    for event in events: #loops through all events in that have recently happened
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                game.next_level()
        
        if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every joystick that is added
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks.append(Joystick_Class(joy)) 
                print("Joystick connected")
                game.players.add(Player((100,100), True, joystick=joy))
                
    pygame_widgets.update(events)
    screen.blit(background, (0,0)) #render background before other components
    game.run()                     #run game components
    pygame.display.flip()          #flip display
    clock.tick(FRAMERATE)

pygame.quit()

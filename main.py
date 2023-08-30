import pygame
import numpy as np
import pygame_widgets
from pygame_widgets.button import Button

class RidgidBody():
    def __init__(self, position: list, mass: float) -> None: #takes in a position as a vector and mass as a scalar
        self.position = np.array(position, float)
        self.velocity = np.array([0,0], float)
        self.acceleration = np.array([0,0], float)
        self.mass = np.array(mass, float)
    
    def add_force(self, force:list) -> None: 
        self.acceleration += np.array(force, float) / self.mass

    def update(self) -> None:
        self.velocity += self.acceleration
        self.position += self.velocity

    def gravity(self) -> None:
       self.add_force([0, 9.81 * self.mass])


ball = RidgidBody([100,300], 2)


#Pygame Setup

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

#button setup

button = Button(screen,100,100,
                     60,20,
                         text="gravity",
                           onClick=lambda: ball.gravity())


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
    
    button.draw()

    pygame.draw.circle(screen, "black", ball.position, 5)

    #Flip

    pygame.display.flip()

    ball.update()

    clock.tick(60)

pygame.quit()

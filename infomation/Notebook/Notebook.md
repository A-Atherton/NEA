# Notebook

## Analysis

Researched different python modules to use for game development: [here](https://geekflare.com/python-game-development-libraries-frameworks/)

Best options were:

* Pygame
  * lots of other people using it
  * fast

* Python Arcade
  * Works well with PyInstaller to make executables

## Exploritory work

Created a class for a basic rigid body which has attributes as numpy arrays which work like vectors (the maths vectors). 2 methods which add a force to the object and one to update the attributed of the object.

![Alt text](<Screenshot from 2023-07-11 13-29-30.png>)

Created a basic python game loop:

![Alt text](<Screenshot from 2023-07-11 13-31-41.png>)

made an object with a mass and a position:

![Alt text](<Screenshot from 2023-07-11 13-32-29.png>)

Here you can see that the object called ball is being drawn to the screen:

![Alt text](<Screenshot from 2023-07-11 13-32-11.png>)

It does not move as no forces are acting on it.

I created a class called player which I will use later

![Alt text](<Screenshot 2023-07-19 at 18.03.21.png>)

thinking of doing levels with a level map string after looking at a [video](https://www.youtube.com/watch?v=YWN8GcmJ-jA)

![Alt text](<Screenshot 2023-07-19 at 18.13.54.png>)



``` python

class Level():
  def __init__(self, level, level_ID):
    self.level = level
    self.level_ID = level_ID

level1 = Level([
      "      ",
      "XX  XX",
      "XXXXXX"
    ], 23)
```

will run a function that gets all levels from a file that comes with the game. This can be added or removed from.

when a level is being played the level can be changed by destroying tiles. this will not effect the levels that are stored in the file.

created a class for the level and for the tiles both from the above tutorial video

![Alt text](<Screenshot 2023-07-19 at 19.03.49.png>)

I created a test tile and drew it

![Alt text](<Screenshot 2023-07-19 at 19.12.02.png>)
![Alt text](<Screenshot 2023-07-19 at 19.12.10.png>)

here is the result

![Alt text](<Screenshot 2023-07-19 at 19.11.44.png>)


created a method that runs when the object is created

![Alt text](<Screenshot 2023-07-21 at 10.20.31.png>)

It adds a tile to a group of sprites if there is an "X" in the level layout in that position. 

![Alt text](<Screenshot 2023-07-21 at 10.20.43.png>)

Error that amkes no sense - Error was boring missed a parenthesis

![Alt text](<Screenshot 2023-07-21 at 10.20.07.png>)

After some slow debugging I finally got the map to display properly to make this. wow.

![Alt text](<Screenshot 2023-07-23 at 14.31.35.png>)

created a levels folder which has some txt files in it storing some simple levels. Also made a test python file which goes through the files in this folder and gets the laevel layouts from each and creates a python list to sort which will be used to create a Level object.

![Alt text](<Screenshot 2023-07-23 at 15.32.22.png>)

result:

![Alt text](<Screenshot 2023-07-23 at 15.33.59.png>)

I implemented the same code as a function with a small change where it appends a Level object to the levels list

![Alt text](<Screenshot 2023-07-23 at 15.52.14.png>)

made some collision logic and now I have a player that can walk on the tiles, jump and interact with the world

![Alt text](<Screenshot 2023-07-24 at 11.59.34.png>)

![Alt text](<Screenshot 2023-07-24 at 12.19.59.png>)

movement is currently very fast and unnatural but that will be changed in later versions by using acceleration and decceleration by friction which will make the movement feel more natural. Also movement currently uses the "wasd" keys which is not my favourite method as I would like to use controllers as it is a better method for local multiplayer. I also need to guns and deaths and multiplayer.

![Alt text](<Screenshot 2023-07-24 at 13.08.50.png>) added a weapon parent class for use later.

![Alt text](<Screenshot 2023-07-27 at 10.50.47.png>)

![Alt text](<Screenshot 2023-07-27 at 14.56.26.png>)

Added controllers which will be the primary method of playing the game.

![Alt text](<Screenshot 2023-07-27 at 15.02.48.png>)

Added circles to show where the players are aiming with the right joystick of a controller

Here is the code that does that.
![Alt text](<Screenshot 2023-07-27 at 14.57.43.png>)

this code uses the top left of the player as the centre of the aiming circle which doesnt look right
Used pygame_widgets to do some tests

![Alt text](<Screenshot from 2023-07-11 16-06-40.png>)

and created a new method to add gravity

![Alt text](<Screenshot from 2023-07-11 16-07-02.png>)
![Alt text](<Screenshot 2023-07-27 at 15.09.45.png>) 

I fixed this by adding half the width and half the hight of the player onto the position of the circle. 

I changed the system used for aiming:
![Alt text](<Screen Shot 2023-09-07 at 15.00.52.png>)


I changed the system i was using so that all levels are stored in the game class.

This means that the game class stores the players so the players are the same objects for all levels. This is a better method than before

to do this I changed the layout of the method in the game class (formerly the level class). The level layouts are passed into the game class and these are turned into a group of tiles stored in the gun_spawners, players_spawners and tiles groups in the Level class

![Alt text](<Screen Shot 2023-09-14 at 14.52.20.png>)

![Alt text](<Screen Shot 2023-09-14 at 14.52.32.png>)

After restructuring I found that the levels were not displaying properly

![Alt text](<Screen Shot 2023-09-15 at 11.46.22.png>)

to investigate further and for later testing i added a key which increases a counter which decides what level will be displayed

![Alt text](<Screen Shot 2023-09-15 at 11.45.20.png>)

this did not work so i printed the layouts that were being passed to the game object on intialization which showed that only one level was being passed to the game object. On inspection of the function to pass the level to the game i noticed that only the wrong variable was being passed and only one level was stored in that variable. This resulted in a broken looking game.

![Alt text](<Screen Shot 2023-09-15 at 11.46.44.png>)

i fixed this by changing the variable being passed to the correct 2D array of strings instead of the 1D array of strings that was being passed in before.

![Alt text](<Screen Shot 2023-09-15 at 11.45.39.png>)

after some debugging of some simple bugs I got the game working as it was before. I also removed the print to keep the console clean. 

![Alt text](<Screen Shot 2023-09-15 at 11.59.11.png>)

Next i needed to add a new method of spawning players as before they were spawned on initialization of the level. This time a new method will be needed because each player object is not stored in each level

The new method will run at the initialization of the game object and will check the amount of controllers connected and...

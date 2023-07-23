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
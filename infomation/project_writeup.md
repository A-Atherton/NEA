# Project Write up

## **Problem Specification**

Some friends want to play a game which has the following features.

A 2d platformer / shooter which should have two game modes:

* Vs - two or more players play against each other in a deathmatch game
* Single Player / Coop - one or more players fight against waves of npc enemies

It should use local multiplayer and platforms should be destructible breaking into pieces when shot using an algorithm to determine the fragmentation pattern of the platform. The NPCs should use path finding algorithms to find the way over rubble from broken platforms to the player(s).

## **Analysis**

### **Stakeholders**

#### **Users**

The main group to benefit from the game are going to be the players. Players will be a diverse group of users. They will likely already have some experience of how games work. This means an in depth tutorial on how to use a controller is not necessary, however controls for the game should be similar to other games the users have played as this will avoid a long learning curve for the player which maximises the time they have enjoying the final product. A screen should be shown when the player first opens the game which describes what the controls are briefly. Controls should be easy to change and sensitivity should be easy to change.

#### **Accessability for Different Users**

The game should be usable with many types of controllers including those for people with disabilities. It may be worth considering adding support for mouse and keyboard as not all players will have access to a controller however this may give some players an advantage against others. options to change colours to make use of the game for colour blind users should be implemented and differences between colours should not be the only signifier for a differences in two items e.g. different guns should have different shapes and different colours.

Users who do not speak english should be considered so easy methods of chosing language should be implemented even if different languages are not added at the time. This will make further improvements to the game easier in the future.

#### **Other Stakeholders**

My teacher is also a stakeholder. They need the game to be completed within a time frame and to have a large amount of algorithmic complexity.

### **Research and Identificatiom of Solutions to the problem**

#### **Platforms for designs**

There are two options for languages that i have considered:

1. C++
2. Python

The benefits of c++ are that it is compiled, fast and a standard for game development however my knowledge of c++ is not as good as in python and getting help is harder as the language is not taught in my college. Python is slower but it is the language that my college uses which means help is easier to find. Also i have more experience in python. For these reasons I decided on using python for the game.

I did some research on [python game libraries](https://geekflare.com/python-game-development-libraries-frameworks/)

I decided on using pygame for my game as it will make the development process far quicker since I do not need to spend time handling displays and events. Pygame is the best option as there are good docs on the python module and lots of insomation on youtube and the web. It is also a fast option compared to other python modules for game development.

#### **Looking at other solutions**

I looked at other solutions...

Stick fight:

+ Fast paced
+ Easy local multiplayer
+ Some platform destruction

- Not open source
- Costs money
- Online multiplayer can be buggy

frog smashers:
+ Also fast paced
+ 

### **Essential Features**

* Player versus player (pvp) combat is an essensial feature. It is important as users want to play against each other.

### **Limitations**

* The proposed system will only use local multiplayer 

### **Objectives**

* Fragmentation of platforms
* Collisions between entities in the game
* Collisions between players and objects
* The game should run with FPS over 60 for smooth game play
* 

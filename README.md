# Aim simulator

This project demonstrates the aim of the robot using deep learning technology. 

Detecting enemy forces, Aim at them and execute the gun shoot.

This project implemented on a video game - counter-strike: global offensive.
            
The trained new deep learning model detects new classes on the pre-trained model inception.
            
Tested on a video game - counter-strike: global offensive

The project contains three steps -

1. detect and classify players
2. aim towards them
3. shoot when the cross on them

[![](http://img.youtube.com/vi/UJqy6Rj7Nzg/0.jpg)](http://www.youtube.com/watch?v=UJqy6Rj7Nzg "Aimbot simulator")
## Classification and Localization

To classify and localize the game characters, the model trained by a set of new pictures and classes.

This project uses the inception model.

The new classes are:
* Counter-Terrorist
* Terrorist
* Counter-Terrorist Dead
* Terrorist Dead

First two classes were added to detect whether a game character is an enemy or teammate.

The last two classes were added to determine whether the character is dead or alive, meaning shoot or ignore.

## Aiming

In the first-person-shooting game, the mouse located in the center of the screen.

and any detection requires movement from center to the place.

and since this is a video game, any new movement changes the unique position of the enemy.

therefore This project managed to calculate the right way to move the mouse towards the enemy.

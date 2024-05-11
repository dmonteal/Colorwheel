# Colorwheel
1 and 2 player game to fill board with colors. 

To get the project working you will need:
-a few packages: Pysimplegui, traceback, pathlib, pylab (you can replace this with numpy I believe)
-download the python and config files in "main" branch
-make a folder called 'icons' in the downloaded folder. Then download all the images in "icon" branch into that folder

The rules are a bit different for 1 and 2 players, but the idea of both is colors can only be adjacent to adjacent colors on the colors wheel.

1P: you start with an nxn empty board and a hand of m colors. Once you press one of the positions the timer starts.
You get points based on how many positions are filled, bonus for being fast and combo a position slot. Colors are updated randomly.
n is default 4, m is default 3

2P: you start with an nxn board with x positions filled, each of you start with m colors. You go back and forth until someone can't place a piece down. Colors go clockwise on the wheel.
n is default 5, m is default 3, x is default 4

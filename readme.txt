Project description:

The current project undertakes to build a computer version of the popular smartphone game 'Cut the rope';
with rope’s cutting and other behaviour triggered by a right-click of the mousse.

The game is organized in levels and has three levels.

No installation is required to run this project, but to have the 
folder kept in the structure provided and opening the project.py 
file and run it.


My project was done in Python 3 - and thus requires to have
a version 3 of Python installed.

And and external module was used: Pygame. Thus it also requires the Pygame
module to be installed before running the project.

Guidelines on how to install Pygame for Python 3:
Reference: https://www.youtube.com/watch?v=MdGoAnFP-mU

1. Go to https://www.pygame.org/news.html
2. Click on Downloads on the left
3. Scroll down to Windows and go to the link:
http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame
under the statement 'There are some pre release binaries for 64 bit ...

4.Download the .whl that matches the installed Python Version and Windows bit version
5. Once downloaded, rename the file by adding '.zip' to it
7. Extract the file 
8. And open C:\PythonXX\include and create a folder called 'pygame'

9. Open the zip file and click on pygame.1-9-2a0.data and open the headers folder

10. Copy all the header files (.h) and paste them into the pygame
folder created in step 8

11. Open C:\PythonXX\Lib\site-packages

12. From the zip folder, copy the pygame and pygame-1.9.2a0.dist-info folder
directly into the site-packages folder from the previous step

13. Open Python IDLE or Sublime and type in 'import pygame'
 which should be imported successfully.


 
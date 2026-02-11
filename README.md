Hey there!!
This is the source code to My Game "Mob_Mecha"
In order to run this game on your PC/LAPTOP You need;
PIP
Python
Pygame 
Python can be installed from the Browser
 
STEPS TO RUN THE GAME;

Install PIP
python -m ensurepip --upgrade
python -m pip install --upgrade pip

Install Pygame
python -m pip --version
python -m pip install pygame

-Open Terminal in the Mob_Mecha folder where all the files are visible 
I repeat all the files -
Mob_Mecha.py
Rider.PY
...py
...py
etc
-inside the terminal
pyinstaller --onefile --windowed --add-data "Elements;Elements" --add-data "BackgroundMusic;BackgroundMusic" Mob_Mecha.py

once done the Game is ready to open 
Go to DIST/
double click// MOB_MECHA

ENJOY!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

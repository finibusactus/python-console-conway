# Conway's game of life in the console

## -Features
  * Allows for an arbitary grid size - it only stores the coordinates of cells that are alive
  * Memory efficent for the above reason
  * Can save and load files


## File structure
  main.py - access point for the program  
  conway_cli.py - command line wrapper around main.py  
  /saves (or make another folder) - folder for saving files  
  util.py - utility functions used in the script  
  game.py - the main implementation of the game  

## How to play - keybindings
  Use WASD/wasd/arrow keys to move the cursor and screen  
  Use T/t to toggle if a cell is dead or alive  
  Use +/- to toggle the speed of the simulation  
  Use ' ' (space) to pause or unpause the simulation  
  Use F/f to iterate forward one generation  
 Control+C to terminate and save

## Need to know
  >In the top of the file 'main.py' change the variable declarations to save and load from a different file  
  The save file is a list of coordinates in csv format of all the cells that are alive 

  >The game is initailly paused when data is loaded from a file 


## Opening the game  
  Run the file `python3 main.py` and/or change the save and load files at the top of the file

  Run the file `python3 conway_cli.py` or use `python3 conway_cli.py help`


## Dependency Graph using Mermaid

  ```mermaid
  graph LR;
  game.py-->main.py;
  util.py-->main.py;
  save_and_load_files-->main.py;
  main.py-->conway_cli.py;
  command_line_args-->conway_cli.py
  ```
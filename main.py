FILE_TO_SAVE_TO = 'saves/custom_save.csv' # Add an optional file path or use None
FILE_TO_LOAD_FROM = 'saves/glider_gun.csv' # Add an optional file path or use None


import subprocess
from os import get_terminal_size
from util import getkp, set_to_csv_data, csv_data_to_set
from game import Game


def start_game_loop(game, save_file):
    while True:
        string = getkp()
        if string == b'CONTROL+C':
            game.quit()
            if save_file:
                set_to_csv_data(save_file, game.squares_alive)
                print(f'The file has been succesfully saved in {save_file}')
            exit()
        game.handle_key_press(string)

def start_game(FILE_TO_LOAD_FROM, save_file):
    subprocess.run('', shell=True)  # Allows windows to process ANSI escape codes
    WIDTH, HEIGHT = get_terminal_size()
    game = Game(WIDTH, HEIGHT)
    data = None
    if FILE_TO_LOAD_FROM:
        data = csv_data_to_set(FILE_TO_LOAD_FROM)
    if data:
        game.load_cell_data(data, True)
    game.start_game_loop()
    if data:
        game.pause()
    print('Press any arrow keys or wasd to start')
    start_game_loop(game, save_file)

def main():
    global FILE_TO_SAVE_TO, FILE_TO_LOAD_FROM
    start_game(FILE_TO_LOAD_FROM, FILE_TO_SAVE_TO)


if __name__ == '__main__':
    main()
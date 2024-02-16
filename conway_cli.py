from main import start_game
import argparse

parser = argparse.ArgumentParser(description='Play Conway\'s game of life in the console')
parser.add_argument('-v', '--version' , action='version', version='%(prog)s 1.0')
parser.add_argument("-l", "--load", type=str, default=None, help="load csv data from this file")
parser.add_argument("-s", "--save", type=str, default=None, help="save the final grid in this file")

def main():
    args = parser.parse_args()
    start_game(args.load, args.save)

if __name__ == '__main__':
    main()
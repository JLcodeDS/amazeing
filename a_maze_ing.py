from src.config_parser import ConfigParser
from MazeGenerator import MazeGenerator
from sys import argv


def print_maze(maze_gen: MazeGenerator):
    for col in maze_gen.maze:
        for row in col:
            if row.visited:
                print("0", end="")
            else:
                print(" ", end="")
        print()


def main():
    if len(argv) != 2:
        print("Not enough parameters.")
        print("To use this program, run: python3 a_maze_ing.py <config file>")
    confparse = ConfigParser(argv[1])
    try:
        conf_dict = confparse.get_config()
    except Exception as e:
        raise Exception(f"Error in parsing config file: {e}")
    conf_dict = {k.lower(): v for (k, v) in conf_dict.items()}
    mazeGen = MazeGenerator(**conf_dict)
    mazeGen.initialize_maze()
    mazeGen.make_42_cells()
    print_maze(mazeGen)


if __name__ == "__main__":
    # try:
    #     main()
    # except Exception as e:
    #     print(e)
    main()

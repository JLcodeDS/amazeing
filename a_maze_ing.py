from src.config_parser import ConfigParser
from maze_generator import MazeGenerator
from sys import argv


def print_maze(maze_gen: MazeGenerator):
    r = [1] * (maze_gen.width * 2 + 1)
    printable = [r]
    for row in maze_gen.maze:
        r_path = [1]
        r_below = [1]
        for c in row:
            r_path.append(0)
            r_path.append(c.walls["E"])
            r_below.append(c.walls["S"])
            r_below.append(1)
        printable.append(r_path)
        printable.append(r_below)

    for row in printable:
        for c in row:
            if c:
                print("\033[37m██\033[0m", end="")
            else:
                print("  ", end="")
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
    mazeGen.generate_maze()
    print_maze(mazeGen)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
    # main()

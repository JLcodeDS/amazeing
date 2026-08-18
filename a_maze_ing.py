from config_parser import ConfigParser
from mazegen.maze_generator import MazeGenerator
from maze_display import MazeDisplay
from sys import argv


def main():
    """Execute the maze generation and display pipeline.

    Parses the configuration file path provided via command-line arguments,
    initializes the configuration settings, and launches the maze application interface.

    Raises:
        Exception: If an error occurs while reading or parsing the configuration file.
    """
    if len(argv) != 2:
        print("Not enough parameters.")
        print("To use this program, run: python3 a_maze_ing.py <config file>")
        return
    confparse = ConfigParser(argv[1])
    try:
        conf_dict = confparse.get_config()
    except Exception as e:
        raise Exception(f"Error in parsing config file: {e}")
    conf_dict = {k.lower(): v for (k, v) in conf_dict.items()}
    display = MazeDisplay(conf_dict)
    display.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
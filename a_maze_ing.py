from config_parser import ConfigParser
from sys import argv


def main():
    if len(argv) != 2:
        print("Not enough parameters.")
        print("To use this program, run: python3 a_maze_ing.py <config file>")
    confparse = ConfigParser(argv[1])
    try:
        conf_dict = confparse.get_config()
    except Exception as e:
        raise Exception(f"Error in parsing config file: {e}")
    print(conf_dict)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)

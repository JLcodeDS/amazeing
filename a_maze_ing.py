from sys import argv
from typing import Callable


class ConfigParser:
    def __init__(self, filename: str) -> None:
        self._config_dict: dict[str, str | None] = {
            "WIDTH": None,
            "HEIGHT": None,
            "ENTRY": None,
            "EXIT": None,
            "OUTPUT_FILE": None,
            "PERFECT": None
        }
        self.config_type: dict[str, Callable] = {
            "WIDTH": int,
            "HEIGHT": int,
            "ENTRY": lambda x: tuple(int(num) for num in x.split(",")),
            "EXIT": lambda x: tuple(int(num) for num in x.split(",")),
            "OUTPUT_FILE": str,
            "PERFECT": bool
        }
        self.filename = filename

    def read_config(self) -> None:
        with open(self.filename) as file:
            for line in file.readlines():
                if line[0] != "#":
                    keyval = line.split("=")
                    try:
                        self._config_dict[keyval[0]] = self.config_type[
                            keyval[0]](keyval[1].replace("\n", ""))
                    except Exception:
                        raise Exception(
                            "Key Value pair " +
                            f"'{keyval[0]} : {keyval[1].replace('\n', '')}'" +
                            "is not allowed."
                            )

    def get_config(self):
        self.read_config()
        return self._config_dict


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

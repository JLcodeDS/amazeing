from typing import Callable, Any


class ConfigParser:
    def __init__(self, filename: str) -> None:
        self._config_dict: dict[str, Any] = {
            "WIDTH": None,
            "HEIGHT": None,
            "ENTRY": None,
            "EXIT": None,
            "OUTPUT_FILE": None,
            "PERFECT": None,
            "SEED": None
        }
        self.config_type: dict[str, Callable] = {
            "WIDTH": int,
            "HEIGHT": int,
            "ENTRY": lambda x: tuple(int(num) for num in x.split(",")),
            "EXIT": lambda x: tuple(int(num) for num in x.split(",")),
            "OUTPUT_FILE": str,
            "PERFECT": bool,
            "SEED": int
        }
        self.filename = filename

    def read_config(self) -> None:
        with open(self.filename) as file:
            for line in file.readlines():
                if line[0] != "#":
                    keyval = line.split("=")
                    try:
                        if keyval[0] != "PERFECT":
                            self._config_dict[keyval[0]] = self.config_type[
                                keyval[0]](keyval[1].replace("\n", ""))
                        else:
                            perfect = True if keyval[1] == "True" else False
                            self._config_dict[keyval[0]] = perfect
                    except Exception:
                        value_cln = keyval[1].replace('\n', '')
                        raise Exception(
                            "Key Value pair " +
                            f"'{keyval[0]} : {value_cln}'" +
                            "is not allowed.\nAllowed keys are: "
                            f"{list(self.config_type.keys())}"
                            )

    def validate_dims(self) -> None:
        conf = self._config_dict
        w = conf["WIDTH"]
        h = conf["HEIGHT"]
        en_dim = conf["ENTRY"]
        ex_dim = conf["EXIT"]
        if (w < 3 and h < 3) or (h < 3 or w < 3):
            raise Exception("Invalid dimensions for WIDTH or HEIGHT.")
        if (en_dim[0] < 0 or en_dim[0] > w) or (
                en_dim[1] < 0 or en_dim[1] > h):
            raise Exception(f"Invalid Entry coordinates: {en_dim}")
        if (ex_dim[0] < 0 or ex_dim[0] > w) or (
                ex_dim[1] < 0 or ex_dim[1] > h):
            raise Exception(f"Invalid Exit coordinates: {ex_dim}")

    def get_config(self):
        self.read_config()
        try:
            self.validate_dims()
        except Exception:
            raise
        return self._config_dict

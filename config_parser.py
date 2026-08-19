from typing import Callable, Any


class ConfigParser:
    """
    A parser for reading, type-casting, and validating
    configuration files.

    used for grid or maze generation settings.
    """

    def __init__(self, filename: str) -> None:
        """
        Initializes the ConfigParser with a target configuration file.

        Args:
            filename (str): The path to the configuration file to be parsed.
        """
        self._config_dict: dict[str, Any] = {
            "WIDTH": None,
            "HEIGHT": None,
            "ENTRY": None,
            "EXIT": None,
            "OUTPUT_FILE": None,
            "PERFECT": None,
            "SEED": None,
        }
        self.config_type: dict[
            str, Callable[[str], str | bool | int | tuple[int, ...]]] = {
            "WIDTH": int,
            "HEIGHT": int,
            "ENTRY": lambda x: tuple(int(num) for num in x.split(",")),
            "EXIT": lambda x: tuple(int(num) for num in x.split(",")),
            "OUTPUT_FILE": str,
            "PERFECT": bool,
            "SEED": int,
        }
        self.allowed_types: dict[str, str] = {
            "WIDTH": "int",
            "HEIGHT": "int",
            "ENTRY": "int,int ",
            "EXIT": "int,int ",
            "OUTPUT_FILE": "str",
            "PERFECT": "bool",
            "SEED": "int",
        }
        self.allowed_types_str = ", ".join(
            f"{k}={v}" for k, v in self.allowed_types.items()
        )
        self.required_params = list(self.allowed_types.keys())[:-1]
        self.filename = filename

    def read_config(self) -> None:
        """
        Reads the configuration file line by line, ignoring comments (#),

        parsing key-value pairs, casting them to their respective types, and
        storing them in the configuration dictionary.

        Raises:
            Exception: If an invalid key, unsupported format, or invalid
            value is encountered.
        """
        with open(self.filename) as file:
            for line in file.readlines():
                if line[0] != "#":
                    keyval = line.split("=")
                    try:
                        if keyval[0] != "PERFECT":
                            self._config_dict[keyval[0]] = self.config_type[
                                keyval[0]
                            ](keyval[1].replace("\n", ""))
                        else:
                            keyval[1] = keyval[1].replace("\n", "")
                            if keyval[1] not in ["True", "False"]:
                                raise Exception(
                                    f"Invalid value for PERFECT: '{keyval[1]}'"
                                )
                            perfect = (
                                True if keyval[1] == "True" else False
                            )
                            self._config_dict[keyval[0]] = perfect
                        if keyval[0] in ["EXIT", "ENTRY"] and (
                            len(self._config_dict[keyval[0]]) != 2
                        ):
                            raise
                    except Exception:
                        value_cln = keyval[1].replace("\n", "")
                        raise Exception(
                            "Key Value pair "
                            + f"'{keyval[0]}={value_cln}' "
                            + "is not allowed.\nAllowed keys and value formats are:\n"
                            + self.allowed_types_str
                        )

    def validate_dims(self) -> None:
        """
        Validates the dimensions, entry points, and exit points loaded in

        the configuration dictionary to ensure they meet constraints (e.g.,
        minimum size, valid bounds).

        Raises:
            Exception: If dimensions are too small, entry and exit are
            identical, or coordinates fall outside the grid bounds.
        """
        conf = self._config_dict
        if True in [conf[param] is None for param in self.required_params]:
            missing = [
                param for param in conf.keys() if conf[
                    param] is None and param != "SEED"]
            raise Exception(f"Missing config parameters: {missing}")
        w = conf["WIDTH"]
        h = conf["HEIGHT"]
        en_dim = conf["ENTRY"]
        ex_dim = conf["EXIT"]
        if en_dim == ex_dim:
            raise Exception("Entry and Exit must be different.")
        if (w < 3 and h < 3) or (h < 3 or w < 3):
            raise Exception("Invalid dimensions for WIDTH or HEIGHT.")
        if (en_dim[0] < 0 or en_dim[0] > w) or (
            en_dim[1] < 0 or en_dim[1] > h
        ):
            raise Exception(f"Invalid Entry coordinates: {en_dim}")
        if (ex_dim[0] < 0 or ex_dim[0] > w) or (
            ex_dim[1] < 0 or ex_dim[1] > h
        ):
            raise Exception(f"Invalid Exit coordinates: {ex_dim}")

    def get_config(self) -> dict[str, Any]:
        """
        Reads and validates the configuration file, then returns the

        fully populated configuration dictionary.

        Returns:
            dict[str, Any]: The dictionary containing all parsed and
            validated configuration settings.

        Raises:
            Exception: Propagates any parsing or validation errors
            encountered.
        """
        self.read_config()
        try:
            self.validate_dims()
        except Exception:
            raise
        return self._config_dict

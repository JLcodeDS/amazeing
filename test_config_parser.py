import pytest
from config_parser import ConfigParser

"""
A few tests to test capabilities of individual scripts.
"""


def test_config_parser_valid_file(tmp_path):
    """Test successful reading, type-casting, and validation of a
    valid config file."""
    config_file = tmp_path / "valid_config.txt"
    config_file.write_text(
        "# This is a comment line\n"
        "WIDTH=10\n"
        "HEIGHT=15\n"
        "ENTRY=0,0\n"
        "EXIT=9,14\n"
        "OUTPUT_FILE=maze.txt\n"
        "PERFECT=True\n"
        "SEED=42\n"
    )

    parser = ConfigParser(str(config_file))
    config = parser.get_config()

    assert config["WIDTH"] == 10
    assert config["HEIGHT"] == 15
    assert config["ENTRY"] == (0, 0)
    assert config["EXIT"] == (9, 14)
    assert config["OUTPUT_FILE"] == "maze.txt"
    assert config["PERFECT"] is True
    assert config["SEED"] == 42


@pytest.mark.parametrize(
    "file_content, expected_error_msg",
    [
        (
            "WIDTH=10\nHEIGHT=10\nENTRY=2,2\nEXIT=2,2\n"
            + "OUTPUT_FILE=out.txt\nPERFECT=True\nSEED=1\n",
            "Entry and Exit must be different.",
        ),
        (
            "WIDTH=2\nHEIGHT=10\nENTRY=0,0\nEXIT=1,9\n"
            + "OUTPUT_FILE=out.txt\nPERFECT=True\nSEED=1\n",
            "Min Values for WIDTH or HEIGHT are W=3 H=3",
        ),
        (
            "WIDTH=10\nHEIGHT=10\nENTRY=0,0\nEXIT=9,9\n"
            + "OUTPUT_FILE=out.txt\nPERFECT=InvalidBool\nSEED=1\n",
            "is not allowed.",
        ),
    ],
)
def test_config_parser_validation_failures(
    tmp_path, file_content, expected_error_msg
        ):
    """Test that invalid bounds, matching entry/exit, or malformed
    values raise exceptions."""
    config_file = tmp_path / "invalid_config.txt"
    config_file.write_text(file_content)

    parser = ConfigParser(str(config_file))

    with pytest.raises(Exception) as exc_info:
        parser.get_config()

    assert expected_error_msg in str(exc_info.value)

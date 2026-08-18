import pytest
from mazegen import MazeGenerator, Cell
import maze_analyzer


def test_cell_wall_manipulation_and_hex_conversion():
    """Test opening specific walls and verifying the
    resulting hexadecimal output."""
    cell = Cell(height=1, width=2, dest=(5, 5))

    # Initial state: all 4 walls closed
    # ("W-S-E-N" = 1111 binary = 15 = 'f' hex)
    assert cell.get_closed_walls() == ["W", "S", "E", "N"]
    assert cell.get_hexa() == "f"

    # Open single wall 'N'
    # ("W-S-E-N" = 1110 binary = 14 = 'e' hex)
    cell.open_wall("N")
    assert "N" in cell.get_open_walls()
    assert cell.get_hexa() == "e"

    # Open multiple walls 'W' and 'E'
    # ("W-S-E-N" = 0100 binary = 4 = '4' hex)
    cell.open_wall(["W", "E"])
    assert set(cell.get_open_walls()) == {"N", "W", "E"}
    assert cell.get_hexa() == "4"


def test_maze_generator_end_to_end_file_creation(tmp_path):
    """Test full generation, A* solving, and correct
    output file structure."""
    output_file = tmp_path / "maze_out.txt"
    gen = MazeGenerator(
        seed=10,
        entry=(0, 0),
        exit=(9, 9),
        perfect=True,
        width=10,
        height=10,
        output_file=str(output_file),
    )

    gen.generate_maze()

    # Verify output file was written and non-empty
    assert output_file.exists()
    content = output_file.read_text().splitlines()

    # Should contain: 10 grid rows + 1 empty line + entry + exit + path string
    assert len(content) == 14
    assert content[10] == ""
    assert content[11] == "0,0"
    assert content[12] == "9,9"
    # Ensure shortest path string consists only of
    # valid cardinal movement directions
    assert all(direction in "NSEW" for direction in content[13])
    # check maze analyzer
    maze = maze_analyzer.Maze.from_file(output_file)
    verdict = maze_analyzer.render(
            maze_analyzer.analyze(maze), 2, 2
        )
    assert (
        "Corners + centre : all reachable" in verdict)
    assert (
        "Wall coherence   : OK (all shared walls match)" in verdict)
    assert (
        "PERFECT=True (this is not a multi-route board for Pac-Man)."
        in verdict
        )


def test_maze_generator_raises_when_entry_in_42_pattern(tmp_path):
    """Test that placing the entry inside the embedded 42
    pattern raises an exception."""
    output_file = tmp_path / "maze_out.txt"
    # In a 10x10 maze, the 42 logo centers around row 2-6, col 1-7
    # (1, 2) falls directly on a Cell42 position
    gen = MazeGenerator(
        seed=42,
        entry=(1, 2),
        exit=(9, 9),
        perfect=True,
        width=10,
        height=10,
        output_file=str(output_file),
    )
    with pytest.raises(Exception) as exc_info:
        gen.generate_maze()
    assert "Error: Entry and Exit are in the 42 logo." in str(exc_info.value)

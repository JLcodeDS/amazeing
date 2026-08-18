*This project has been created as part of the 42 curriculum by arivet, jludolph*

# `mazegen` — Standalone 2D Maze Generator Module

`mazegen` is a lightweight, zero-dependency Python module that generates 2D grid mazes using procedural algorithms, embeds custom path constraints (such as the "42" pattern), and computes optimal solution paths via A* search.

---

## Installation

### From a Pre-Built Wheel (`.whl`)

You can install the pre-built package directly using `pip`:

```bash
pip install mazegen-1.0.0-py3-none-any.whl

```

### Building from Source

To build and install the `.whl` package directly from source:

1. Ensure `build` is installed:
```bash
pip install build

```


2. Build the package at the root of the project:
```bash
python3 -m build

```


3. Install the resulting `.whl` file located in `dist/`:
```bash
pip install dist/mazegen-1.0.0-py3-none-any.whl

```



---

## Quickstart & Basic Example

To generate a maze with default parameters and print its solution path:

```python
from mazegen import MazeGenerator

# 1. Instantiate the generator with a custom seed and grid size
maze = MazeGenerator(
    width=15,
    height=15,
    seed=42,
    entry=(0, 0),
    exit=(14, 14),
    perfect=True
)

# 2. Run the generation and pathfinding algorithms
maze.generate_maze()

# 3. Access the generated grid structure and solution path
print(f"Maze Dimensions: {maze.width}x{maze.height}")
print(f"Solution Path Length: {len(maze.shortest_path)} steps")
print(f"Coordinates in Solution Path: {maze.shortest_path}")

```

---

## Custom Parameters

When instantiating `MazeGenerator`, you can customize the generator's behavior using the following parameters:

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `width` | `int` | `15` | Total columns in the maze grid matrix. |
| `height` | `int` | `15` | Total rows in the maze grid matrix. |
| `seed` | `int` | `None` | PRNG seed for deterministic, reproducible generation. |
| `entry` | `tuple[int, int]` | `(0, 0)` | Starting coordinate formatted as `(x, y)`. |
| `exit` | `tuple[int, int]` | `(width-1, height-1)` | Destination coordinate formatted as `(x, y)`. |
| `perfect` | `bool` | `True` | Set `True` for a single-solution maze without loops; `False` for multiple paths and loops. |
| `output_file` | `str` | `"output.txt"` | Target destination path for serializing hex-encoded wall output. |

### Example with Custom Configuration:

```python
from mazegen import MazeGenerator

config = {
    "width": 25,
    "height": 20,
    "seed": 1337,
    "entry": (0, 0),
    "exit": (24, 19),
    "perfect": False,  # Imperfect maze (contains loops and dead-end openings)
    "output_file": "custom_maze.txt"
}

generator = MazeGenerator(**config)
generator.generate_maze()

```

---

## Accessing Maze Structure & Solutions

The `MazeGenerator` instance exposes internal data structures directly in memory without requiring you to read or parse the output file.

### 1. In-Memory Grid Structure (`maze.grid`)

The grid is stored as a 2D matrix of `Cell` objects accessible via `generator.grid[y][x]`.

```python
cell = generator.grid[0][0]  # Access top-left cell

print(cell.x, cell.y)        # Cell coordinates
print(cell.walls)           # Dictionary showing active walls, e.g., {'N': True, 'E': False, 'S': True, 'W': True}
print(cell.get_hexa())      # Hexadecimal bitmask representation of walls

```

### 2. Solution Path (`maze.shortest_path`)

The solution path is computed using the A* pathfinding algorithm and stored as an ordered list of `(x, y)` coordinate tuples from `entry` to `exit`.

```python
path = generator.shortest_path
# Output: [(0, 0), (0, 1), (1, 1), ..., (14, 14)]

for step, (x, y) in enumerate(path):
    print(f"Step {step}: ({x}, {y})")

```

---

## License

This module is licensed under the **MIT License**. The complete license terms permitting full reuse, modification, and redistribution are provided in the `LICENSE.md` file located at the root of the repository.
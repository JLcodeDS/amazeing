*This project has been created as part of the 42 curriculum by arivet, jludolph*

# A-Maze-ing

## Description

**A-Maze-ing** is a 2D maze generator, solver, and visualizer built in Python. The project generates customizable rectangular mazes using procedural algorithms, embeds a signature "42" pattern into the center layout, solves the resulting structure using pathfinding algorithms, and renders an interactive graphical user interface using MiniLibX (MLX).

### Core Features
- **Procedural Maze Generation**: Supports both "perfect" mazes (single solution, no loops) and "imperfect" mazes (multiple routes and loops).
- **Embedded 42 Design**: Custom algorithm logic automatically incorporates a predefined "42" pattern into the maze layout.
- **A* Pathfinding**: Built-in pathfinder that guarantees finding the shortest path from the entry to the exit point.
- **Interactive UI**: Real-time graphical visualization supporting maze regeneration, step-by-step path animation, color theme swapping, and file export.
- **Modular Packaging**: Core maze generation logic (`mazegen`) is fully packaged as an installable Python wheel (`.whl`).

---

## Instructions

### Prerequisites
- **Python 3.10+**
- **MiniLibX (MLX)** graphics library bindings installed.
- **Linux/macOS**: On Linux systems, `libbsd-dev` may be required.

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd <repository>
```

2. **(Optional) Install `mazegen` as a standalone Python package:**
```bash
pip install build
python3 -m build
pip install dist/mazegen-0.1.0-py3-none-any.whl
```



### Execution

Run the main application by providing a configuration file path as an argument:

```bash
python3 main.py config.json

```

### In-App Graphical Controls

| Key | Action |
| --- | --- |
| **`1`** | Regenerate maze with a new random seed |
| **`2`** | Toggle/Animate the shortest path solution |
| **`3`** | Cycle through available visual color themes |
| **`4` / `Esc`** | Exit the application |

---

## Configuration File Format

The program requires a configuration file passed as a command-line argument. Keys are case-insensitive.

### JSON Structure Example

```json
{
  "seed": 42,
  "entry": [0, 0],
  "exit": [10, 10],
  "perfect": true,
  "width": 15,
  "height": 15,
  "output_file": "maze.txt"
}

```

### Parameter Specification

* `seed` (*int*): Seed value for PRNG initialization to ensure deterministic generation.
* `entry` (*tuple/list of 2 ints*): Starting coordinates formatted as `[X, Y]`.
* `exit` (*tuple/list of 2 ints*): Ending coordinates formatted as `[X, Y]`.
* `perfect` (*bool*): `true` creates a perfect maze with no loops; `false` introduces dead-end breaks to form multiple paths.
* `width` (*int*): Number of columns in the grid matrix.
* `height` (*int*): Number of rows in the grid matrix.
* `output_file` (*str*): Path destination where the generated hexadecimal maze data will be written.

---

## Algorithms

### Maze Generation: Randomized Depth-First Search (Backtracker)

We selected **Randomized Depth-First Search (DFS) with Backtracking** for maze generation.

#### Why We Chose This Algorithm:

1. **High Tortuosity & Aesthetic**: DFS creates mazes with long, winding corridors and fewer short branches, offering a classic visual appearance and high difficulty.
2. **Implementation Simplicity**: Using a stack array to keep track of visited nodes allows straightforward recursive or iterative traversal.
3. **Control over Custom Patterns**: It allowed us to easily flag and isolate static pre-visited regions (like the central "42" pattern cells) so the generator naturally routes around them.

### Pathfinding: A* Search

The solver utilizes the **A\* Search algorithm** with Manhattan distance as its heuristic function ($h(n) = \vert{}\Delta x\vert{} + \vert{}\Delta y\vert{}$). A* guarantees finding the shortest path while exploring fewer total nodes than unguided search algorithms like Dijkstra or BFS.

---

## Reusability

The **`mazegen`** module was designed to be completely independent from the GUI rendering logic (`MazeDisplay`).

### Reusable Components:

* **`mazegen.Cell`**: Generic node class handling wall bitmasks, hex encoding (`get_hexa()`), directional movement calculations, and path costs.
* **`mazegen.MazeGenerator`**: Independent class capable of generating grid representations, solving paths via A*, and serializing the output without requiring any UI dependencies or graphics frameworks.

### How to Reuse:

Install the `.whl` package and import it directly into any Python program:

```python
from mazegen import MazeGenerator

config = {
    "seed": 12345, "entry": (0, 0), "exit": (9, 9),
    "perfect": True, "width": 10, "height": 10,
    "output_file": "output.txt"
}

generator = MazeGenerator(**config)
generator.generate_maze()
print(f"Shortest path coordinates: {generator.shortest_path}")

```

---

## Team & Project Management

### Roles & Responsibilities

The roles were fairly evenly distributed throughout the project, especially for the first steps such as the initial config parser and the maze generation algorithms (perfect and imperfect). Then slightly more divided to speed up completion:
* **arivet**: MiniLibX display integration (`MazeDisplay`), color palette design, interactive controls/event hooks, and path animation.
* **jludolph**: A star search algorithm implementation and incorporation into the final output file and as a class attribute.


### Initial Planning vs. Reality

* **Original Plan**: We wanted to start with writing the parser, then the generator and the mlx display to visualize and validate the algorithms, then the pathfinding and finally, refactor and polish the docstrings, documentation and packaging.
* **Evolution**: Core maze generation was completed ahead of schedule. However, handling edge cases—such as protecting entry/exit coordinates from overlapping with the embedded "42" logo and smoothing wall joints using circular primitives in MLX—required took a bit longer than expected.

### What Worked Well & What Could Be Improved

* **Worked Well**: Decoupling `mazegen` into an independent package from day one allowed parallel development on generation logic and UI rendering without merge conflicts.
* **Could Be Improved**: Automated test coverage for small/invalid maze dimensions could be expanded to catch edge configuration errors earlier.

### Tools Used

* **Git & GitHub**: Source control and code review branches.
* **Python `build` & `setuptools**`: Packaging `mazegen` into standard Python wheels.
* **VS Code**: IDE and local debugging.

---

## Resources

* **Vulkan / Graphics Reference**: [LunarG Vulkan SDK](https://vulkan.lunarg.com/) / [MoltenVK Repository](https://github.com/KhronosGroup/MoltenVK)
* **Maze Algorithms**: https://professor-l.github.io/mazes/ graphical visualization and explanations of different algorithms.
* **Pathfinding**: https://www.geeksforgeeks.org/dsa/a-search-algorithm/ A star search explanations and some youtube videos (such as https://www.youtube.com/watch?v=qigPctCgR_k) to see it in action for additional clarity.

### AI Usage Disclaimer

AI tools (specifically LLMs) were utilized during development for the following tasks:

1. **Documentation & Docstrings**: Generating standard Google-style docstrings across Python modules (`mazegen`, `maze_display`, `config_parser`).
2. **Packaging Guidance**: Assistance in configuring `pyproject.toml` to build `.whl` files under setuptools standards.
3. **Refactoring Assistance**: Optimizing line lengths and formatting to maintain compliance with 42 PEP8 style standards.
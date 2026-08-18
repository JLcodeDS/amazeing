import random


class Cell:
    """Represents an individual node/grid cell in the maze.

    Tracks wall states, visitation status, neighbor locations, and metadata
    used for pathfinding algorithms (e.g., A* search).

    Attributes:
        walls (dict[str, int]): Wall indicators ("N", "E", "S", "W")
            mapped to 1 (closed) or 0 (open).
        visited (bool): Flag indicating if the cell has been
            processed during generation.
        height (int): Row position (Y coordinate) in the maze.
        width (int): Column position (X coordinate) in the maze.
        coords (tuple[int, int]): Position in (height, width) / (row, column)
            format.
        move (dict[str, tuple[int, int]]): Target coordinates for moving
            in each cardinal direction.
        h_score (int): Estimated distance (Manhattan heuristic) from this
            cell to the destination.
        g_score (int): Cost of the path from the entry node to this cell.
        f_score (int): Total estimated path cost (g_score + h_score).
        parent (Cell | None): Reference to the preceding cell in the
            pathfinding tree.
    """

    def __init__(self, height: int, width: int, dest: tuple[int, int]):
        """Initializes a Cell instance at the given coordinates.

        Args:
            height (int): Row coordinate in the maze grid.
            width (int): Column coordinate in the maze grid.
            dest (tuple[int, int]): Exit coordinates in (height, width)
                format.
        """
        self.walls = {
            "W": 1,
            "S": 1,
            "E": 1,
            "N": 1
        }
        self.visited = False
        self.height = height
        self.width = width
        self.coords = (height, width)
        self.move = {
            "W": (height, width - 1),
            "S": (height + 1, width),
            "E": (height, width + 1),
            "N": (height - 1, width)
        }
        self.h_score = self.heuristic((height, width), dest)
        self.g_score: int
        self.f_score: int
        self.parent: Cell | None = None

    def get_hexa(self) -> str:
        """
        Converts the cell's wall configurations to a single
        hexadecimal character.

        Returns:
            str: Single hex digit representing binary walls
                string "W-S-E-N".
        """
        bin_str = "".join([str(x) for x in self.walls.values()])
        return format(int(bin_str, 2), "x")

    def open_wall(self, direction: str | list[str]) -> None:
        """Removes one or more walls from the cell.

        Args:
            direction (str | list[str]): A direction string
                ("N", "S", "E", "W") or a list of direction strings.
        """
        if isinstance(direction, str):
            self.walls[direction] = 0
        else:
            for dir in direction:
                self.walls[dir] = 0

    def get_open_walls(self) -> list[str]:
        """Retrieves directions where walls are open.

        Returns:
            list[str]: Cardinal direction codes with open walls (value 0).
        """
        return [wall for wall in self.walls.keys() if not self.walls[wall]]

    def get_closed_walls(self) -> list[str]:
        """Retrieves directions where walls remain intact.

        Returns:
            list[str]: Cardinal direction codes with intact walls (value 1).
        """
        return [wall for wall in self.walls.keys() if self.walls[wall]]

    def get_move_coords(self, direction: str) -> tuple[int, int]:
        """Calculates neighbor coordinates along a specified direction.

        Args:
            direction (str): Cardinal direction ("N", "S", "E", "W").

        Returns:
            tuple[int, int]: Coordinates (row, column) in the
                specified direction.
        """
        return self.move[direction]

    def get_allowed_moves(self) -> list[tuple[int, int]]:
        """Returns reachable neighbor cell coordinates through open walls.

        Returns:
            list[tuple[int, int]]: Coordinates of all adjacent accessible
                cells.
        """
        return [self.get_move_coords(dir) for dir in self.get_open_walls()]

    @staticmethod
    def heuristic(point1: tuple[int, int], point2: tuple[int, int]):
        """Calculates Manhattan distance between two coordinate tuples.

        Args:
            point1 (tuple[int, int]): Starting coordinate (row, column).
            point2 (tuple[int, int]): Ending coordinate (row, column).

        Returns:
            int: Calculated Manhattan distance between the points.
        """
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


class Cell42(Cell):
    """Specialized cell pre-marked as visited to form a
    centered decorative pattern."""

    def __init__(self, height: int, width: int, dest: tuple[int, int]):
        """Initializes a Cell42 instance with visited pre-set to True."""
        super().__init__(height, width, dest)
        self.visited = True


class MazeGenerator:
    """
    Handles randomized maze generation, custom structural layouts,
    pathfinding, and output.

    Attributes:
        seed (int): Seed value for PRNG initialization.
        entry (tuple): Entry coordinates formatted as (x, y).
        exit (tuple): Exit coordinates formatted as (x, y).
        width (int): Total column count of the maze grid.
        height (int): Total row count of the maze grid.
        perfect (bool): True to generate a perfect maze
            (single path, no loops); False for imperfect.
        output_file (str): Output text file destination path.
        wall_entry (dict[str, str]): Reverse lookup mapping opposite
            direction walls.
        maze_edges (dict[str, int]): Outer boundaries indexed by direction
            name.
        maze (list[list[Cell]]): 2D grid matrix holding `Cell` objects.
        shortest_path (list[tuple[int, int]]): Solved path coordinates from
            entry to exit.
    """

    def __init__(self, seed: int, entry: tuple, exit: tuple,
                 perfect: bool, width: int, height: int, output_file: str):
        """Initializes parameters and builds the initial cell grid."""
        self.seed = seed
        self.entry = entry
        self.exit = exit
        self.width = width
        self.height = height
        self.perfect = perfect
        self.output_file = output_file
        self.wall_entry = {
            "W": "E",
            "S": "N",
            "E": "W",
            "N": "S"
        }
        self.maze_edges = {
            "W": 0,
            "S": height - 1,
            "E": width - 1,
            "N": 0
        }

        self.maze = self.initialize_maze()

    def initialize_maze(self) -> list[list[Cell]]:
        """Populates the grid matrix with standard closed Cell instances.

        Returns:
            list[list[Cell]]: A 2D list of default `Cell` objects.
        """
        ex = (self.exit[1], self.exit[0])
        maze = [
            [Cell(h, w, ex) for w in range(self.width)
             ] for h in range(self.height)
            ]
        return maze

    def make_42_cells(self):
        """Embeds a custom '42' cell pattern at the center of the maze grid.

        Prints a warning if the current grid dimensions are too small to
        house the logo.
        """
        h_42 = 5
        w_42 = 7
        coords_42 = [
            (0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (2, 4),
            (4, 0), (4, 2), (4, 3), (4, 4), (5, 0), (5, 2), (5, 4),
            (6, 0), (6, 1), (6, 2), (6, 4)
        ]
        if (self.height < h_42 or self.width < w_42):
            print("WARNING: Maze dimensions do not allow for 42 pattern.")
        else:
            wh_42 = ((self.width - w_42) // 2,
                     (self.height - h_42) // 2)
            for w, h in coords_42:
                self.maze[wh_42[1] + h][wh_42[0] + w] = Cell42(
                    wh_42[1] + h, wh_42[0] + w, (self.exit[1], self.exit[0]))

    def get_cell(self, coords: tuple[int, int]) -> Cell:
        """Retrieves a cell instance from the grid matching specified
        coordinates.

        Args:
            coords (tuple[int, int]): Grid coordinate specified as
            (row, column).

        Returns:
            Cell: The target `Cell` instance.
        """
        return self.maze[coords[0]][coords[1]]

    def enter_maze(self) -> None:
        """Starts the initial cell traversal starting from the maze
        entry point."""
        current_cell = self.get_cell((self.entry[1], self.entry[0]))
        current_cell.visited = True
        path_stack = [current_cell]
        self.perfect_backtrack(path_stack)

    def perfect_backtrack(self, path_stack: list[Cell]) -> None:
        """Generates a perfect maze structure using randomized depth-first
        search.

        Args:
            path_stack (list[Cell]): Stack containing active cell path steps.
        """
        while len(path_stack) > 0:
            current = path_stack[-1]
            choices = self.find_viable_choices(current)
            if not len(choices):
                path_stack.pop()
            else:
                direction = random.choice(choices)
                current.open_wall(direction)
                move = current.get_move_coords(direction)
                next_cell = self.get_cell(move)
                next_cell.open_wall(self.wall_entry[direction])
                next_cell.visited = True
                path_stack.append(next_cell)

    def imperfect_maze(self) -> None:
        """Removes extra walls across dead-ends to create secondary
        routes and loops."""
        for y in range(self.height):
            for x in range(self.width):
                current = self.get_cell((y, x))
                closed_walls = current.get_closed_walls()
                if len(closed_walls) == 3 and not isinstance(current, Cell42):
                    can_break = []
                    for wall in closed_walls:
                        if (wall in ["N", "S"]) and (
                                current.height == self.maze_edges[wall]):
                            continue
                        if (wall in ["E", "W"]) and (
                                current.width == self.maze_edges[wall]):
                            continue
                        move = current.get_move_coords(wall)
                        next_cell = self.get_cell(move)
                        if isinstance(next_cell, Cell42):
                            continue
                        can_break.append(wall)
                    if can_break:
                        to_break = random.choice(can_break)
                        current.open_wall(to_break)
                        move = current.get_move_coords(to_break)
                        next_cell = self.get_cell(move)
                        opposite_wall = self.wall_entry[to_break]
                        next_cell.open_wall(opposite_wall)

    def find_viable_choices(self, current: Cell) -> list[str]:
        """Finds valid adjacent unvisited directions from a specific cell.

        Args:
            current (Cell): Cell being evaluated.

        Returns:
            list[str]: Unvisited wall directions within grid boundaries.
        """
        choices = current.get_closed_walls()
        viable_choices = choices.copy()
        for wall in choices:
            if (wall == "S" or wall == "N") and (
                    current.height == self.maze_edges[wall]):
                viable_choices.remove(wall)
                continue
            if (wall == "E" or wall == "W") and (
                    current.width == self.maze_edges[wall]):
                viable_choices.remove(wall)
                continue
            move = current.get_move_coords(wall)
            if self.maze[move[0]][move[1]].visited:
                viable_choices.remove(wall)
        return viable_choices

    def generate_maze(self) -> None:
        """Orchestrates full maze execution flow: seeds the random mod,
        creates geometry, solves via A*, and outputs results.

        Raises:
            Exception: If entry or exit coordinates overlap with the
            '42' pattern region.
        """
        random.seed(self.seed)
        self.initialize_maze()
        self.make_42_cells()
        entry = (self.entry[1], self.entry[0])
        exit = (self.exit[1], self.exit[0])
        if isinstance(self.get_cell(entry), Cell42) or (
            isinstance(self.get_cell(exit), Cell42)
        ):
            n_coord = [
                (
                    c.coords[1], c.coords[0]
                ) for r in self.maze for c in r if isinstance(c, Cell42)
                ]
            raise Exception(
                "Error: Entry and Exit are in the 42 logo.\n" +
                "Disallowed coords are:\n" +
                f"{n_coord}"
                )
        self.enter_maze()
        if not self.perfect:
            self.imperfect_maze()
        self.a_star_search()
        self.write_output()

    def write_output(self) -> None:
        """Writes encoded hex maze structure, metadata, and solution
        directions to file."""
        dir_map = {
            (0, -1): 'W',
            (1, 0): 'S',
            (-1, 0): 'N',
            (0, 1): 'E'
        }
        lines = []
        for row in self.maze:
            lines.append("".join([c.get_hexa() for c in row]) + "\n")
        lines.extend(["\n",
                     f"{self.entry[0]},{self.entry[1]}\n",
                      f"{self.exit[0]},{self.exit[1]}\n"])
        short_path = ""
        prev = self.shortest_path[0]
        for cell in self.shortest_path[1:]:
            short_path += dir_map[
                (cell[0] - prev[0], cell[1] - prev[1])
            ]
            prev = cell
        lines.append(short_path + "\n")
        with open(self.output_file, "w") as output:
            output.writelines(lines)

    def a_star_search(self):
        """Solves the maze using the A* search pathfinding algorithm.

        Computes the shortest path from entry to exit and stores the list
        of coordinates in `self.shortest_path`.
        """
        entry = (self.entry[1], self.entry[0])
        goal = (self.exit[1], self.exit[0])
        current = self.get_cell(entry)
        current.g_score = 0
        current.f_score = current.h_score
        closed_cells = set()
        open_cells = [current]
        while len(open_cells):
            current = self.get_best_move(open_cells)
            if current.coords == goal:
                break
            open_cells.remove(current)
            closed_cells.add(current)
            neighbours = [
                self.get_cell(x) for x in current.get_allowed_moves()]
            for cell in neighbours:
                if cell.coords in [x.coords for x in closed_cells]:
                    continue
                new_g = current.g_score + 1
                if cell.coords not in [x.coords for x in open_cells]:
                    open_cells.append(cell)
                elif new_g >= cell.g_score:
                    continue
                cell.g_score = new_g
                cell.f_score = cell.g_score + cell.h_score
                cell.parent = current
        shortest_path = [current.coords]
        while current.coords != entry:
            current = current.parent
            shortest_path.append(current.coords)
        shortest_path = shortest_path[::-1]
        self.shortest_path = shortest_path

    def get_best_move(self, allowed: list[Cell]):
        """Selects the candidate cell with the lowest estimated
        total cost (f_score).

        Args:
            allowed (list[Cell]): Candidate cells currently in the open set.

        Returns:
            Cell: Cell instance with the optimal f_score and h_score values.
        """
        min_f = min(allowed, key=lambda x: (x.f_score, x.h_score))
        return min_f

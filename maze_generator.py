import random


class Cell:
    def __init__(self, height: int, width: int):
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

    def get_hexa(self) -> str:
        bin_str = "".join([str(x) for x in self.walls.values()])
        return format(int(bin_str, 2), "x")

    def open_walls(self, direction: str | list[str]) -> None:
        if isinstance(direction, str):
            self.walls[direction] = 0
        else:
            for dir in direction:
                self.walls[dir] = 0

    def get_open_walls(self) -> list[str]:
        return [wall for wall in self.walls.keys() if not self.walls[wall]]

    def get_closed_walls(self) -> list[str]:
        return [wall for wall in self.walls.keys() if self.walls[wall]]

    def get_move_coords(self, direction: str) -> tuple[int, int]:
        return self.move[direction]


class Cell42(Cell):
    def __init__(self, height: int, width: int):
        super().__init__(height, width)
        self.visited = True


class MazeGenerator:
    def __init__(self, seed: int, entry: tuple, exit: tuple,
                 perfect: bool, width: int, height: int, output_file: str):
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
        maze = [
            [Cell(h, w) for w in range(self.width)
             ] for h in range(self.height)
            ]
        return maze

    def make_42_cells(self):
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
                    wh_42[1] + h, wh_42[0] + w)

    def get_cell(self, coords: tuple[int, int]) -> Cell:
        return self.maze[coords[0]][coords[1]]

    def enter_maze(self) -> None:
        current_cell = self.get_cell((self.entry[1], self.entry[0]))
        current_cell.visited = True
        path_stack = [current_cell]
        self.perfect_backtrack(path_stack)

    def perfect_backtrack(self, path_stack: list[Cell]) -> None:
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
        random.seed(self.seed)
        self.initialize_maze()
        self.make_42_cells()
        self.enter_maze()
        if not self.perfect:
            random.seed(self.seed + 157)
            self.imperfect_superposition()
        self.write_output()

    def write_output(self) -> None:
        lines = []
        for row in self.maze:
            lines.append("".join([c.get_hexa() for c in row]) + "\n")
        lines.extend(["\n",
                     f"{self.entry[0]},{self.entry[1]}\n",
                      f"{self.exit[0]},{self.exit[1]}\n"])
        with open(self.output_file, "w") as output:
            output.writelines(lines)

    def print_maze(self) -> None:
        # (Wall, path) combination
        MAZE_COLORS = [
            ("\033[96m██\033[0m", "\033[95m░░\033[0m"),
            ("\033[32m██\033[0m", "\033[92m▒▒\033[0m"),
            ("\033[93m██\033[0m", "\033[91m██\033[0m"),
            ("\033[37m██\033[0m", "\033[90m██\033[0m")
        ]
        chosen_palette = MAZE_COLORS[3]
        # chosen_palette = random.choice(MAZE_COLORS)
        r = [1] * (self.width * 2 + 1)
        printable = [r]
        for row in self.maze:
            r_path = [1]
            r_below = [1]
            for c in row:
                r_path.append(0)
                r_path.append(c.walls["E"])
                r_below.append(c.walls["S"])
                r_below.append(1)
            printable.append(r_path)
            printable.append(r_below)
        for print_row in printable:
            for cell in print_row:
                if cell:
                    print(f"{chosen_palette[0]}", end="")
                else:
                    print("  ", end="")
            print()

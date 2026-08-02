class MazeGenerator():
    def __init__(self, seed: str, entry: tuple, exit: tuple,
                 perfect: bool, width: int, height: int, output_file: str):
        self.seed = seed
        self.entry = entry
        self.exit = exit
        self.width = width
        self.height = height
        self.perfect = perfect

    def initialize_maze(self):
        self.maze = [
            [Cell() for _ in range(self.width)] for _ in range(self.height)
            ]

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
                self.maze[wh_42[1] + h][wh_42[0] + w].visited = True


class Cell:
    def __init__(self):
        self.walls = {
            "W": 1,
            "S": 1,
            "E": 1,
            "N": 1
        }
        self.visited = False

    def get_hexa(self) -> str:
        bin_str = "".join([str(x) for x in self.walls.values])
        return format(int(bin_str), "x")

    def open_wall(self, direction: str) -> None:
        self.walls[direction] = 0

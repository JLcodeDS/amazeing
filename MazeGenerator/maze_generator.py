class MazeGenerator():
    def __init__(self, seed: str, entry: tuple, exit: tuple,
                 perfect: bool, width: int, height: int):
        self.seed = seed
        self.entry = entry
        self.exit = exit
        self.width = width
        self.height = height
        self.perfect = perfect

    def initialize_maze(self):
        self.maze = [[Cell() * self.width] * self.height]

    def make_42_cells(self):
        h_42 = 5
        w_42 = 7
        if (self.height < h_42 or self.width < w_42):
            print("WARNING: Maze dimensions do not allow for 42 pattern.")
        else:
            

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


class Cell_42(Cell):
    def __init__(self):
        super().__init__()
        self.visited = True

from mlx import Mlx
from typing import Any
from maze_generator import Cell, Cell42


class MazeDisplay:
    def __init__(self, maze_gen: Any) -> None:
        self.maze_gen = maze_gen
        self.tile_size = 20

        self.win_width = self.maze_gen.width * self.tile_size
        self.win_height = self.maze_gen.height * self.tile_size

        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr, self.win_width, self.win_height, "A-Maze-ing")

        self.show_path = False
        self.color_palette_index = 0

    def get_cell_color(self, cell: Cell) -> int:
        entry_yx = (self.maze_gen.entry[1], self.maze_gen.entry[0])
        exit_yx = (self.maze_gen.exit[1], self.maze_gen.exit[0])
        if cell.coords == entry_yx:
            return 0xFFFF0000
        elif cell.coords == exit_yx:
            return 0xFF00FF84
        elif isinstance(cell, Cell42):
            return 0xFFFCD172
        else:
            return 0xFF332305

    def draw_rectangle(
        self, start_x: int, start_y: int, width: int, height: int, color: int
    ) -> None:
        for y in range(start_y, start_y + height):
            for x in range(start_x, start_x + width):
                self.mlx.mlx_pixel_put(self.mlx_ptr, self.win_ptr, x, y, color)

    def draw_maze(self) -> None:
        self.mlx.mlx_clear_window(self.mlx_ptr, self.win_ptr)

        wall_color = 0xFFFFB40F
        wall_thickness = 2
        for y in range(self.maze_gen.height):
            for x in range(self.maze_gen.width):
                cell = self.maze_gen.get_cell((y, x))
                px = x * self.tile_size
                py = y * self.tile_size
                bg_color = self.get_cell_color(cell)

                self.draw_rectangle(
                    px, py, self.tile_size, self.tile_size, bg_color)

                if cell.walls["N"] == 1:
                    self.draw_rectangle(
                        px, py, self.tile_size, wall_thickness, wall_color)
                if cell.walls["W"] == 1:
                    self.draw_rectangle(
                        px, py, wall_thickness, self.tile_size, wall_color)
                if cell.walls["S"] == 1:
                    self.draw_rectangle(
                        px, py + self.tile_size - wall_thickness,
                        self.tile_size, wall_thickness, wall_color)
                if cell.walls["E"] == 1:
                    self.draw_rectangle(
                        px + self.tile_size - wall_thickness, py,
                        wall_thickness, self.tile_size, wall_color)
        self.mlx.mlx_do_sync(self.mlx_ptr)

    def handle_input(self, keycode: int, param: Any = None) -> None:
        print(f"Touche détectée : {keycode}")
        if keycode == 49:
            self.maze_gen.generate_maze()
            self.draw_maze()

        elif keycode == 50:
            self.show_path = not self.show_path
            self.draw_maze()

        elif keycode == 51:
            self.color_palette_index += 1
            self.draw_maze()

        elif keycode == 21 or keycode == 53:
            self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
            self.mlx.mlx_loop_exit(self.mlx_ptr)

    def run(self):
        self.draw_maze()
        self.mlx.mlx_hook(self.win_ptr, 2, 1, self.handle_input, None)
        self.mlx.mlx_loop(self.mlx_ptr)

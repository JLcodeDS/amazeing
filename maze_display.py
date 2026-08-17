import sys
import ctypes
import time
import datetime
from mlx import Mlx
from typing import Any
from maze_generator import Cell, Cell42, MazeGenerator


class MazeDisplay:
    def __init__(self, maze_dict: Any) -> None:
        self.maze_dict = maze_dict
        self.maze_gen = MazeGenerator(**maze_dict)
        self.tile_size = 30
        self.ui_height = 40
        self.offset = 15

        self.win_width = (
            self.maze_gen.width * self.tile_size + (self.offset * 2))
        self.win_height = (
            (self.maze_gen.height * self.tile_size) + self.ui_height + (
                self.offset * 2))

        if sys.platform == "linux":
            ctypes.CDLL("libbsd.so.0", mode=ctypes.RTLD_GLOBAL)

        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        if not self.mlx_ptr:
            raise RuntimeError(
                "Error: Impossible to initialize graphic display (Verify "
                "the $DISPLAY variable or X11 connection).")
        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr, self.win_width, self.win_height, "A-Maze-ing")

        self.show_path = False
        self.color_palette_index = 0
        self.palettes = [
            {   # 0: Cyan / Pink
                "wall": 0xFFFF00E6, "bg": 0xFF140026, "path": 0xFF2BFF00,
                "entry": 0xFF00FFFF, "exit": 0xFFE6FF00, "42": 0xFFD400FF
            },
            {   # 1: Neon Green
                "wall": 0xFF00B53A, "bg": 0xFF050510, "path": 0xFFD583C2,
                "entry": 0xFF55FF55, "exit": 0xFFFF3333, "42": 0xFF2A7C3D
            },
            {   # 2: Orange / Brown
                "wall": 0xFFDFA03E, "bg": 0xFF1D110B, "path": 0xFF032E8D,
                "entry": 0xFFFF0000, "exit": 0xFF00FF84, "42": 0xFFEADBC3
            },
            {   # 3: Blue / White
                "wall": 0xFF72D1FC, "bg": 0xFF052333, "path": 0xFFF04B00,
                "entry": 0xFFFFFFFF, "exit": 0xFF84FF00, "42": 0xFF0FB4FF
            }
        ]

    def get_cell_color(self, cell: Cell) -> int:
        palette = self.palettes[self.color_palette_index % len(self.palettes)]
        entry_yx = (self.maze_gen.entry[1], self.maze_gen.entry[0])
        exit_yx = (self.maze_gen.exit[1], self.maze_gen.exit[0])
        if cell.coords == entry_yx:
            return palette["entry"]
        elif cell.coords == exit_yx:
            return palette["exit"]
        elif isinstance(cell, Cell42):
            return palette["42"]
        else:
            return palette["bg"]

    def draw_rectangle(
        self, start_x: int, start_y: int, width: int, height: int, color: int
    ) -> None:
        for y in range(start_y, start_y + height):
            for x in range(start_x, start_x + width):
                self.mlx.mlx_pixel_put(self.mlx_ptr, self.win_ptr, x, y, color)

    def draw_rounded_square(
        self, start_x: int, start_y: int, size: int, radius: int, color: int
    ) -> None:
        for y in range(size):
            for x in range(size):
                dx = max(0, radius - x, x - (size - radius - 1))
                dy = max(0, radius - y, y - (size - radius - 1))
                if dx * dx + dy * dy <= radius * radius:
                    self.mlx.mlx_pixel_put(
                        self.mlx_ptr, self.win_ptr, start_x + x, start_y + y,
                        color)

    def draw_circle(
        self, center_x: int, center_y: int, thickness: int, color: int
    ) -> None:
        radius_float = thickness / 2.0
        half_t = thickness // 2
        for y in range(center_y - half_t, center_y + half_t + 1):
            for x in range(center_x - half_t, center_x + half_t + 1):
                dx = x - center_x
                dy = y - center_y
                if (dx * dx) + (dy * dy) <= (radius_float * radius_float):
                    self.mlx.mlx_pixel_put(
                        self.mlx_ptr, self.win_ptr, x, y, color)

    def draw_maze(self) -> None:
        self.mlx.mlx_clear_window(self.mlx_ptr, self.win_ptr)

        palette = self.palettes[self.color_palette_index % len(self.palettes)]
        wall_color = palette["wall"]
        wall_thickness = 5
        for y in range(self.maze_gen.height):
            for x in range(self.maze_gen.width):
                cell = self.maze_gen.get_cell((y, x))
                px = (x * self.tile_size) + self.offset
                py = (y * self.tile_size) + self.offset
                special_color = self.get_cell_color(cell)

                margin = 5
                inner_size = self.tile_size - (margin * 2)
                corner_radius = 2

                self.draw_rectangle(
                    px, py, self.tile_size, self.tile_size, palette["bg"])
                if special_color in (palette["entry"], palette["exit"]):
                    self.draw_rounded_square(
                        px + margin,
                        py + margin,
                        inner_size,
                        corner_radius,
                        special_color
                    )
                elif special_color == palette["42"]:
                    self.draw_rounded_square(
                        px + 3,
                        py + 3,
                        self.tile_size - 6,
                        corner_radius,
                        special_color
                    )
        segments = set()
        for y in range(self.maze_gen.height):
            for x in range(self.maze_gen.width):
                cell = self.maze_gen.get_cell((y, x))
                if cell.walls["N"] == 1:
                    segments.add(((x, y), (x + 1, y)))
                if cell.walls["W"] == 1:
                    segments.add(((x, y), (x, y + 1)))
                if cell.walls["S"] == 1:
                    segments.add(((x, y + 1), (x + 1, y + 1)))
                if cell.walls["E"] == 1:
                    segments.add(((x + 1, y), (x + 1, y + 1)))

        vertex_degrees: dict[Any, Any] = {}
        for v1, v2 in segments:
            vertex_degrees[v1] = vertex_degrees.get(v1, 0) + 1
            vertex_degrees[v2] = vertex_degrees.get(v2, 0) + 1
        half_t = wall_thickness // 2
        for v1, v2 in segments:
            px1 = (v1[0] * self.tile_size) + self.offset
            py1 = (v1[1] * self.tile_size) + self.offset
            px2 = (v2[0] * self.tile_size) + self.offset
            py2 = (v2[1] * self.tile_size) + self.offset
            if py1 == py2:
                start_x = min(px1, px2)
                length = abs(px1 - px2) + 1
                self.draw_rectangle(
                    start_x, py1 - half_t, length, wall_thickness, wall_color)
            else:
                start_y = min(py1, py2)
                length = abs(py1 - py2) + 1
                self.draw_rectangle(
                    px1 - half_t, start_y, wall_thickness, length, wall_color)
        for vertex in vertex_degrees.keys():
            px = (vertex[0] * self.tile_size) + self.offset
            py = (vertex[1] * self.tile_size) + self.offset
            self.draw_circle(px, py, wall_thickness, wall_color)
        self.draw_ui()
        self.mlx.mlx_do_sync(self.mlx_ptr)

    def draw_ui(self) -> None:
        text_y = (
            self.maze_gen.height * self.tile_size) + self.offset + (
                self.ui_height // 2)
        text_x = self.offset

        text_color = 0xFFFFFFFF

        menu_text = "1: regen   2: path    3: color    4/esc: quit"

        self.mlx.mlx_string_put(
            self.mlx_ptr,
            self.win_ptr,
            text_x,
            text_y,
            text_color,
            menu_text
        )

    def animate_path(self, path_coords: list[tuple[int, int]]) -> None:
        palette = self.palettes[self.color_palette_index % len(self.palettes)]
        path_color = palette["path"]
        corner_radius = 4
        margin = 6
        inner_size = self.tile_size - (margin * 2)
        for y, x in path_coords:
            px = (x * self.tile_size) + self.offset
            py = (y * self.tile_size) + self.offset
            self.draw_rounded_square(
                        px + margin,
                        py + margin,
                        inner_size,
                        corner_radius,
                        path_color
                    )
            self.mlx.mlx_do_sync(self.mlx_ptr)
            time.sleep(0.05)

    def handle_input(self, keycode: int, param: Any = None) -> None:
        print(f"Touche détectée : {keycode}")
        if keycode == 49:
            dict_cpy = self.maze_dict.copy()
            dict_cpy['seed'] += datetime.datetime.now().second
            self.maze_gen = MazeGenerator(**dict_cpy)
            self.maze_gen.generate_maze()
            self.draw_maze()

        elif keycode == 50:
            self.show_path = not self.show_path
            self.draw_maze()
            if self.show_path:
                coords = self.maze_gen.shortest_path[1:-1]
                self.animate_path(coords)

        elif keycode == 51:
            self.color_palette_index += 1
            self.draw_maze()

        elif keycode == 65307 or keycode == 52:
            self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
            self.mlx.mlx_loop_exit(self.mlx_ptr)

    def run(self) -> None:
        self.maze_gen.generate_maze()
        self.draw_maze()
        self.mlx.mlx_hook(self.win_ptr, 2, 1, self.handle_input, None)
        self.mlx.mlx_loop(self.mlx_ptr)

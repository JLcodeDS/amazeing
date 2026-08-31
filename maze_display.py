"""Module for managing the graphic user interface and visualization
of the maze.

Utilizes MiniLibX (MLX) bindings to render maze grids, wall geometry,
animated paths, and user interactions.
"""

import time
import random
from mlx import Mlx
from typing import Any
from mazegen.maze_generator import Cell, Cell42, MazeGenerator


class MazeDisplay:
    """Manages window lifecycle, MLX rendering pipelines, themes,
    and input events.

    Attributes:
        maze_dict (dict[str, Any]): Configuration properties used for
            maze generation.
        maze_gen (MazeGenerator): Core generator instance handling
            grid algorithms.
        tile_size (int): Pixel dimensions for each square maze cell
            grid segment.
        ui_height (int): Height of the bottom user interface banner
            in pixels.
        offset (int): Outer padding surrounding the rendering region
            in pixels.
        win_width (int): Total computed width of the application window.
        win_height (int): Total computed height of the application window.
        mlx (Mlx): MiniLibX graphical framework interface wrapper.
        mlx_ptr (Any): Pointer handle to the initialized MiniLibX context.
        win_ptr (Any): Pointer handle to the created display window.
        show_path (bool): State toggle tracking solution path visibility.
        color_palette_index (int): Active index selector for color scheme
            palettes.
        palettes (list[dict[str, int]]): Pre-defined color palettes
            holding ARGB hex values.
    """

    def __init__(self, maze_dict: Any) -> None:
        """Initializes window dimensions, loads native C libraries,
        and sets up MLX graphics.

        Args:
            maze_dict (Any): Dictionary containing parameters to instantiate
            a `MazeGenerator`.

        Raises:
            RuntimeError: If initialization of the MLX context fails
            (e.g., missing X11 display).
        """
        self.maze_dict = maze_dict
        self.maze_gen = MazeGenerator(**maze_dict)
        self.ui_height = 40
        self.offset = 15

        max_screen_w = 1400
        max_screen_h = 800

        avail_w = max_screen_w - (self.offset * 2)
        avail_h = max_screen_h - self.ui_height - (self.offset * 2)

        max_tile_w = avail_w // self.maze_gen.width
        max_tile_h = avail_h // self.maze_gen.height

        self.tile_size = max(2, min(30, max_tile_w, max_tile_h))

        self.win_width = (
            self.maze_gen.width * self.tile_size) + (self.offset * 2)
        if self.win_width < 475:
            self.win_width = 475
        self.win_height = (
            self.maze_gen.height * self.tile_size) + self.ui_height \
            + (self.offset * 2)

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
        """Determines the appropriate color integer for a given cell
        type or coordinate.

        Args:
            cell (Cell): Target cell to query.

        Returns:
            int: Calculated ARGB hex color code based on active palette and
            cell role.
        """
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
        """Fills a solid axis-aligned rectangular region with a given color.

        Args:
            start_x (int): Top-left starting X pixel position.
            start_y (int): Top-left starting Y pixel position.
            width (int): Rectangle horizontal width in pixels.
            height (int): Rectangle vertical height in pixels.
            color (int): ARGB hex color code.
        """
        for y in range(start_y, start_y + height):
            for x in range(start_x, start_x + width):
                self.mlx.mlx_pixel_put(self.mlx_ptr, self.win_ptr, x, y, color)

    def draw_rounded_square(
        self, start_x: int, start_y: int, size: int, radius: int, color: int
    ) -> None:
        """Renders a square shape with smoothed/rounded corner radiuses.

        Args:
            start_x (int): Top-left X origin pixel location.
            start_y (int): Top-left Y origin pixel location.
            size (int): Side length dimension of the square in pixels.
            radius (int): Corner curve radius length in pixels.
            color (int): ARGB hex color code.
        """
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
        """Renders a filled circular node used for seamless wall joint caps.

        Args:
            center_x (int): Center X coordinate of the circle in pixels.
            center_y (int): Center Y coordinate of the circle in pixels.
            thickness (int): Diameter dimension of the circle in pixels.
            color (int): ARGB hex color code.
        """
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
        """Clears the window buffer and draws the entire maze
        structure and UI."""
        self.mlx.mlx_clear_window(self.mlx_ptr, self.win_ptr)

        palette = self.palettes[self.color_palette_index % len(self.palettes)]
        wall_color = palette["wall"]
        wall_thickness = max(1, self.tile_size // 6)
        for y in range(self.maze_gen.height):
            for x in range(self.maze_gen.width):
                cell = self.maze_gen.get_cell((y, x))
                px = (x * self.tile_size) + self.offset
                py = (y * self.tile_size) + self.offset
                special_color = self.get_cell_color(cell)

                margin = max(1, self.tile_size // 6)
                corner_radius = max(0, margin - 1)
                inner_size = self.tile_size - (margin * 2)

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
        """Renders the command shortcut reference menu and the current seed
        at the bottom of the window on two separate lines."""

        # On calcule le centre de la zone d'UI
        base_y = (
            self.maze_gen.height * self.tile_size) + self.offset + \
            (self.ui_height // 2)
        text_x = self.offset

        text_color = 0xFFFFFFFF

        menu_text = "1: regen   2: path    3: color    4/esc: quit"
        seed_text = f"SEED: {self.maze_gen.seed}"

        self.mlx.mlx_string_put(
            self.mlx_ptr,
            self.win_ptr,
            text_x,
            base_y - 12,
            text_color,
            menu_text
        )

        self.mlx.mlx_string_put(
            self.mlx_ptr,
            self.win_ptr,
            text_x,
            base_y + 10,
            text_color,
            seed_text
        )

    def animate_path(self, path_coords: list[tuple[int, int]]) -> None:
        """Sequentially draws solution path markers cell-by-cell with
        a frame delay.

        Args:
            path_coords (list[tuple[int, int]]): Ordered sequence of
                (row, col) coordinates.
        """
        self._render_path_sequence(path_coords, "path", animated=True)

    def non_animated_path(self, path_coords: list[tuple[int, int]]) -> None:
        """Draws the entire solution path instantly without frame delays.

        Args:
            path_coords (list[tuple[int, int]]): Ordered sequence of
                (row, col) coordinates.
        """
        self._render_path_sequence(path_coords, "path", animated=False)

    def remove_path(self, path_coords: list[tuple[int, int]]) -> None:
        """Clears solution path markers by redrawing them using the
        background color.

        Args:
            path_coords (list[tuple[int, int]]): Ordered sequence of
                (row, col) coordinates.
        """
        self._render_path_sequence(path_coords, "bg", animated=False)

    def handle_input(self, keycode: int, param: Any = None) -> None:
        """Event handler processing keyboard inputs for controls
        (regen, path toggle, theme, exit).

        Args:
            keycode (int): Integer key code emitted by MiniLibX keyboard
                event.
            param (Any, optional): Optional parameter payload passed by
                MLX hook.
        """
        if keycode == 49:
            dict_cpy = self.maze_dict.copy()
            dict_cpy['seed'] = random.randint(0, 999999999)
            self.show_path = False
            self.maze_gen = MazeGenerator(**dict_cpy)
            self.maze_gen.generate_maze()
            print(f"Maze regenerated with SEED: {self.maze_gen.seed}")
            self.draw_maze()

        elif keycode == 50:
            self.show_path = not self.show_path
            coords = self.maze_gen.shortest_path[1:-1]
            if self.show_path:
                self.animate_path(coords)
            else:
                self.remove_path(coords)

        elif keycode == 51:
            self.color_palette_index += 1
            coords = self.maze_gen.shortest_path[1:-1]
            if self.show_path:
                self.draw_maze()
                self.non_animated_path(coords)
            else:
                self.draw_maze()

        elif keycode == 65307 or keycode == 52:
            self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
            self.mlx.mlx_loop_exit(self.mlx_ptr)

    def _render_path_sequence(self, path_coords: list[tuple[int, int]],
                              color_key: str, animated: bool = False) -> None:
        """Internal utility method to draw or erase a sequence of path cells.

        Handles the geometric rendering of the maze path, retrieving the
        appropriate color from the active palette, and managing the display
        synchronization for optional frame-by-frame animation.

        Args:
            path_coords (list[tuple[int, int]]): Ordered sequence of
                (row, col) coordinates.
            color_key (str): Dictionary key to retrieve the target color from
                the palette (e.g., "path" or "bg").
            animated (bool, optional): If True, forces an MLX display sync
                and a time delay after drawing each cell. Defaults to False.
        """
        palette = self.palettes[self.color_palette_index % len(self.palettes)]
        draw_color = palette[color_key]

        margin = max(1, self.tile_size // 6)
        corner_radius = max(0, margin - 1)
        inner_size = self.tile_size - (margin * 2)

        for y, x in path_coords:
            px = (x * self.tile_size) + self.offset
            py = (y * self.tile_size) + self.offset
            self.draw_rounded_square(
                px + margin, py + margin, inner_size, corner_radius, draw_color
            )
            if animated:
                self.mlx.mlx_do_sync(self.mlx_ptr)
                time.sleep(0.01)
        if not animated:
            self.mlx.mlx_do_sync(self.mlx_ptr)

    def run(self) -> None:
        """Generates the initial maze structure, performs initial draw,
        and starts MLX event loop."""
        self.maze_gen.generate_maze()
        print(f"Maze generated with SEED: {self.maze_gen.seed}")
        self.draw_maze()
        self.mlx.mlx_hook(self.win_ptr, 2, 1, self.handle_input, None)
        self.mlx.mlx_loop(self.mlx_ptr)

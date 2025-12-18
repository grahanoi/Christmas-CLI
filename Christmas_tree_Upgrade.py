#!/usr/bin/env python3
"""
Fullscreen Christmas Tree Animation with Snowfall (STABLE TREE)
Optimized for Raspberry Pi

Features:
- Fixed, non-moving tree geometry
- Dynamically scaled to terminal size
- Vertically & horizontally centered
- Blinking ornaments (tree itself stays still)
- Pulsing star
- Snowfall animation over the whole screen
"""

import time
import random
import os
import shutil

# ANSI Color codes
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

SNOW_CHARS = ['❄', '*', '·']
ORNAMENT_CHARS = ['●', '◆', '■', '▲', '♦', '♥']
ORNAMENT_COLORS = [Colors.RED, Colors.BLUE, Colors.MAGENTA, Colors.CYAN, Colors.YELLOW]


def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')


# ---------- TREE PRE-COMPUTATION (IMPORTANT) ----------

def generate_tree_layout(width, height):
    """Generate fixed tree geometry and ornament positions"""

    max_tree_width = int(width * 0.7)
    if max_tree_width % 2 == 0:
        max_tree_width += 1

    tree_height = int(height * 0.65)
    tree_top = (height - tree_height) // 2

    rows = []
    ornament_map = {}

    ornament_id = 0

    for i in range(tree_height):
        row_width = min(max_tree_width, 1 + 2 * i)
        start_x = (width - row_width) // 2
        y = tree_top + i

        for x in range(row_width):
            # Place ornaments sparsely and FIXED
            if random.random() < 0.05:
                ornament_map[(start_x + x, y)] = ornament_id
                ornament_id += 1

        rows.append((start_x, row_width, y))

    trunk_width = max_tree_width // 6
    trunk_x = (width - trunk_width) // 2
    trunk_y = tree_top + tree_height

    return rows, ornament_map, (trunk_x, trunk_y, trunk_width), tree_top


# ---------- DRAWING ----------

def draw_scene(blink_state, star_bright, snowflakes, tree_data):
    rows, ornament_map, trunk, tree_top = tree_data
    term = shutil.get_terminal_size()
    width, height = term.columns, term.lines

    buffer = [[' ' for _ in range(width)] for _ in range(height)]

    # Snow
    for x, y, char in snowflakes:
        if 0 <= x < width and 0 <= y < height:
            buffer[y][x] = Colors.WHITE + char + Colors.RESET

    # Star
    star_x = width // 2
    star_color = Colors.YELLOW + Colors.BOLD if star_bright else Colors.YELLOW
    buffer[tree_top][star_x] = star_color + '★' + Colors.RESET

    # Tree body (STABLE)
    for start_x, row_width, y in rows:
        if y >= height:
            continue
        for x in range(row_width):
            pos = (start_x + x, y)
            if pos in ornament_map:
                oid = ornament_map[pos]
                char = ORNAMENT_CHARS[oid % len(ORNAMENT_CHARS)]
                # Blink: alternate between colored ornament and dark foliage
                if blink_state:
                    color = ORNAMENT_COLORS[oid % len(ORNAMENT_COLORS)]
                else:
                    color = Colors.GREEN + Colors.BOLD
                buffer[y][start_x + x] = color + char + Colors.RESET
            else:
                buffer[y][start_x + x] = Colors.GREEN + '*' + Colors.RESET

    # Trunk
    trunk_x, trunk_y, trunk_width = trunk
    for t in range(2):
        y = trunk_y + t
        if y >= height:
            continue
        for x in range(trunk_width):
            buffer[y][trunk_x + x] = Colors.YELLOW + '█' + Colors.RESET

    # Message
    message = '❄ Merry Christmas ZHAW ❄'
    msg_y = trunk_y + 3
    if msg_y < height:
        start_x = (width - len(message)) // 2
        for i, c in enumerate(message):
            buffer[msg_y][start_x + i] = Colors.BOLD + Colors.RED + c + Colors.RESET

    return '\n'.join(''.join(row) for row in buffer)


# ---------- ANIMATION ----------

def animate():
    term = shutil.get_terminal_size()
    width, height = term.columns, term.lines

    tree_data = generate_tree_layout(width, height)

    snowflakes = []
    frame = 0

    try:
        while True:
            # Snow generation
            if len(snowflakes) < width // 2:
                snowflakes.append((random.randint(0, width - 1), 0, random.choice(SNOW_CHARS)))

            # Snow falling
            snowflakes = [(x, y + 1, c) for x, y, c in snowflakes if y + 1 < height]

            clear_screen()
            print(draw_scene(
                blink_state=(frame % 8 < 4),
                star_bright=(frame % 12 < 6),
                snowflakes=snowflakes,
                tree_data=tree_data
            ))

            time.sleep(0.1)
            frame += 1

    except KeyboardInterrupt:
        clear_screen()
        print('\n🎄 Frohe Weihnachten! 🎄\n')


if __name__ == '__main__':
    clear_screen()
    print('Starting stable fullscreen Christmas tree with snowfall...')
    time.sleep(1)
    animate()

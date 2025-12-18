#!/usr/bin/env python3
"""
Stable Fullscreen Christmas Tree with Snowfall
Raspberry Pi optimized (no shaking)
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


def generate_tree_layout(width, height):
    max_tree_width = int(width * 0.7)
    if max_tree_width % 2 == 0:
        max_tree_width += 1

    tree_height = int(height * 0.65)
    tree_top = (height - tree_height) // 2

    rows = []
    ornament_map = {}
    oid = 0

    for i in range(tree_height):
        row_width = min(max_tree_width, 1 + 2 * i)
        start_x = (width - row_width) // 2
        y = tree_top + i

        for x in range(row_width):
            if random.random() < 0.06:
                ornament_map[(start_x + x, y)] = oid
                oid += 1

        rows.append((start_x, row_width, y))

    trunk_width = max_tree_width // 6
    trunk_x = (width - trunk_width) // 2
    trunk_y = tree_top + tree_height

    return rows, ornament_map, (trunk_x, trunk_y, trunk_width), tree_top


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

    # Tree body (stable)
    for start_x, row_width, y in rows:
        if y >= height:
            continue
        for x in range(row_width):
            pos = (start_x + x, y)
            if pos in ornament_map:
                oid = ornament_map[pos]
                char = ORNAMENT_CHARS[oid % len(ORNAMENT_CHARS)]
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


def animate():
    term = shutil.get_terminal_size()
    width, height = term.columns, term.lines

    tree_data = generate_tree_layout(width, height)
    snowflakes = []
    frame = 0

    FPS_DELAY = 0.25
    BLINK_PERIOD = 20
    STAR_PERIOD = 30
    SNOW_LIMIT = width // 4

    # Clear once & hide cursor
    print('\033[2J\033[?25l', end='')

    try:
        while True:
            if len(snowflakes) < SNOW_LIMIT:
                snowflakes.append((random.randint(0, width - 1), 0, random.choice(SNOW_CHARS)))

            snowflakes = [(x, y + 1, c) for x, y, c in snowflakes if y + 1 < height]

            blink_state = (frame % BLINK_PERIOD) < (BLINK_PERIOD // 2)
            star_bright = (frame % STAR_PERIOD) < (STAR_PERIOD // 2)

            scene = draw_scene(blink_state, star_bright, snowflakes, tree_data)
            print('\033[H' + scene, end='', flush=True)

            time.sleep(FPS_DELAY)
            frame += 1

    except KeyboardInterrupt:
        print('\033[?25h')
        print('\n🎄 Merry Christmas! 🎄\n')


if __name__ == '__main__':
    animate()
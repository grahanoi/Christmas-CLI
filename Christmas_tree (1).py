#!/usr/bin/env python3
"""
Terminal Christmas Tree Animation - Version A (Classic Blinking)
Features: Blinking ornaments, pulsing star, colored decorations
"""

import time
import random
import os
import shutil  # For getting terminal size

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

def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def draw_tree(blink_state, star_bright, ornament_chars, ornament_positions):
    """Draw the Christmas tree with ornaments and star"""
    
    # Get terminal width for centering
    try:
        terminal_width = shutil.get_terminal_size().columns
    except:
        terminal_width = 80  # Default if can't detect
    
    # Tree structure - each row has width and ornament positions
    tree_rows = [
        # (width, [ornament positions])
        (1, []),           # Star
        (3, ornament_positions[0]),          # Top tier
        (5, ornament_positions[1]),
        (7, ornament_positions[2]),
        (9, ornament_positions[3]),
        (11, ornament_positions[4]),
        (13, ornament_positions[5]),  # Middle tier
        (15, ornament_positions[6]),
        (17, ornament_positions[7]),
        (19, ornament_positions[8]),
        (21, ornament_positions[9]),
        (23, ornament_positions[10]),
        (25, ornament_positions[11]), # Bottom tier
        (27, ornament_positions[12]),
        (29, ornament_positions[13]),
        (31, ornament_positions[14]),
        (33, ornament_positions[15]),
    ]
    
    trunk_rows = 2
    trunk_width = 3
    
    output = []
    
    # Calculate tree width for centering
    max_width = max(row[0] for row in tree_rows)
    
    # Extra padding to center the entire tree in the terminal
    left_margin = ' ' * max(0, (terminal_width - max_width) // 2)
    
    # Star
    star_color = Colors.YELLOW + Colors.BOLD if star_bright else Colors.YELLOW
    star = star_color + '★' + Colors.RESET
    padding = ' ' * ((max_width - 1) // 2)
    output.append(left_margin + padding + star)
    
    # Ornament colors to cycle through
    ornament_colors = [Colors.RED, Colors.BLUE, Colors.MAGENTA, Colors.CYAN, Colors.YELLOW]
    
    # Counter for ornament positions
    ornament_index = 0
    
    # Draw tree body
    for row_num, (width, ornament_positions) in enumerate(tree_rows[1:], 1):
        padding = ' ' * ((max_width - width) // 2)
        row = []
        
        for i in range(width):
            if i in ornament_positions:
                # Ornament - blink effect with special characters
                char = ornament_chars[ornament_index]
                ornament_index += 1
                
                if blink_state and random.random() > 0.3:  # 70% chance to light up when blinking
                    color = random.choice(ornament_colors)
                    row.append(color + char + Colors.RESET)
                else:
                    row.append(Colors.GREEN + char + Colors.RESET)
            else:
                # Regular tree foliage
                row.append(Colors.GREEN + '*' + Colors.RESET)
        
        output.append(left_margin + padding + ''.join(row))
    
    # Trunk
    trunk_padding = ' ' * ((max_width - trunk_width) // 2)
    for _ in range(trunk_rows):
        output.append(left_margin + trunk_padding + Colors.YELLOW + '█' * trunk_width + Colors.RESET)
    
    # Add festive message
    output.append('')
    message = 'Merry Christmas!'
    msg_padding = ' ' * ((max_width - len(message)) // 2)
    output.append(left_margin + msg_padding + Colors.BOLD + Colors.RED + message + Colors.RESET)
    
    return '\n'.join(output)

def animate_tree():
    """
    Animate the Christmas tree endlessly with changing ornament characters
    """
    # Special ASCII characters for ornaments
    special_chars = ['●', '◆', '◇', '■', '□', '▲', '▼', '♦', '♥', '♠', '♣', '☼', '○', '◉', '◎', '▪', '▫', '◘']
    
    frame = 0
    cycle_frames = 20  # New characters every 20 frames (40 seconds at 0.5 FPS)
    fps = 0.5
    frame_delay = 1.0 / fps
    
    # Tree widths for each row
    tree_widths = [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33]
    
    # Function to generate random ornament positions
    def generate_ornament_positions():
        positions = []
        for width in tree_widths:
            # Random number of ornaments per row (1 to 3)
            num_ornaments = random.randint(1, 3)
            # Random positions within the row width
            row_positions = sorted(random.sample(range(width), min(num_ornaments, width)))
            positions.append(row_positions)
        return positions
    
    # Initialize ornament positions
    ornament_positions = generate_ornament_positions()
    total_ornaments = sum(len(positions) for positions in ornament_positions)
    
    # Initialize ornament characters
    ornament_chars = [random.choice(special_chars) for _ in range(total_ornaments)]
    
    try:
        while True:  # Endless loop
            clear_screen()
            
            # With 30% probability, regenerate ornament positions
            if random.random() < 0.3:
                ornament_positions = generate_ornament_positions()
                total_ornaments = sum(len(positions) for positions in ornament_positions)
                ornament_chars = [random.choice(special_chars) for _ in range(total_ornaments)]
            
            # Change ornament characters at the start of each cycle
            if frame % cycle_frames == 0:
                ornament_chars = [random.choice(special_chars) for _ in range(total_ornaments)]
            
            # Blink state changes every few frames
            blink_state = (frame // 2) % 2 == 0  # Toggle every 2 frames
            
            # Star pulse effect (slower than ornaments)
            star_bright = (frame // 4) % 2 == 0  # Toggle every 4 frames
            
            tree = draw_tree(blink_state, star_bright, ornament_chars, ornament_positions)
            print(tree)
            
            time.sleep(frame_delay)
            frame += 1
            
    except KeyboardInterrupt:
        clear_screen()
        print("\n🎄 Thanks for watching! Happy Holidays! 🎄\n")

def main():
    """Main function"""
    clear_screen()
    print("Starting Endless Christmas Tree Animation...")
    print("Press Ctrl+C to stop\n")
    time.sleep(2)
    
    # Run animation endlessly
    animate_tree()

if __name__ == "__main__":
    main()

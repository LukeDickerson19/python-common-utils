import time
import math
import sys

# Define 8 unique characters. The color, not the character, will now carry most of the intensity.
SPECTRUM_CHARS = ["█", "█", "█", "█", "█", "█", "█", "█"] 
# Using block characters for higher intensity steps to represent solid color fields.

# ANSI Reset Code
ANSI_RESET = "\033[0m"

# Configuration for the animation
WIDTH = 120        # Total horizontal width of the animation
FREQUENCY = 0.2    # Base speed of the spectrum shift
ROWS = 2000        # Number of rows (frames) to print
SLEEP_TIME = 0.02  # Time delay between printing lines (speed)
NUM_CHARS = len(SPECTRUM_CHARS) 

# Helper function to generate 24-bit True Color ANSI code
def get_true_color_code(r, g, b):
    # Format: \033[38;2;R;G;Bm (Foreground color)
    return f"\033[38;2;{r};{g};{b}m"

# --- Animation Loop ---
def animate_spectrum():
    print("--- Morphing True Color (24-bit) Spectrum Animation ---")
    print("Pattern A will smoothly transition into **Pulsing Horizontal Bands** over the duration.")
    print(f"Duration: {ROWS} rows at {SLEEP_TIME}s/row ({ROWS * SLEEP_TIME} seconds total)")
    print(f"Press Ctrl+C to stop.")
    time.sleep(1)

    # Loop through a set number of frames/rows
    for i in range(ROWS):
        # 't' acts as the primary time variable, controlling the fast scrolling
        t = i * FREQUENCY
        
        # 'pattern_time' acts as a slow modulator for Pattern A
        pattern_time = i / ROWS * 2 * math.pi * 5 

        # 'y_pos' introduces a vertical dependency to the pattern
        y_pos = i * 0.01

        line = ""

        # Global hue shift based on time for continuous color cycling
        hue_shift = i * 0.05 

        # --- MORPH FACTOR: Transitions from 0.0 (start) to 1.0 (end) over ROWS ---
        morph_factor = i / ROWS 

        # Generate the pattern for the current line
        for x in range(WIDTH):
            
            # --- Pattern A Calculation (Original Complex Wave) ---
            # This is the starting pattern (morph_factor = 0.0)
            x_coeff_A1 = 0.1 + math.sin(pattern_time * 0.3) * 0.04
            t_coeff_A1 = 0.5 + math.cos(pattern_time * 0.2) * 0.3
            t_coeff_A2 = 0.2 + math.sin(pattern_time * 0.1) * 0.1
            
            wave_value_A = (
                math.sin(x * x_coeff_A1 + t * t_coeff_A1 + y_pos * 0.1) * 1.0 +
                math.cos(x * 0.05 - t * t_coeff_A2 + y_pos * 0.5) * 1.0
            )

            # --- Pattern B Calculation (Target Pattern: Pulsing Horizontal Bands) ---
            # This is the ending pattern (morph_factor = 1.0)
            wave_value_B = (
                math.sin(y_pos * 1.5 + t * 0.2) * 1.8 +      # Wide, slow horizontal bands moving vertically
                math.cos(t * 0.5) * 0.2                      # Subtle time-based global pulse
            )

            # --- Combined Morphing Wave Value (Linear Interpolation) ---
            # As morph_factor goes from 0 to 1, wave_value transitions from A to B.
            wave_value = (wave_value_A * (1.0 - morph_factor)) + (wave_value_B * morph_factor)
            
            # 1. Normalize the wave value from roughly [-2.0, 2.0] to [0.0, 1.0]:
            normalized_value = (wave_value + 2.0) / 4.0
            
            # --- True Color Calculation (RGB Spectrum) ---
            
            # Map the normalized wave value (0.0 to 1.0) to a position in the color cycle (0 to 2*pi)
            color_position = normalized_value * math.pi * 2
            
            # Use sine waves offset by 120 degrees (2*pi/3) to generate continuous R, G, B values (0-1)
            # Add the global hue_shift to cycle the entire spectrum over time
            R_norm = math.sin(color_position + hue_shift) * 0.5 + 0.5
            G_norm = math.sin(color_position + hue_shift + 2 * math.pi / 3) * 0.5 + 0.5
            B_norm = math.sin(color_position + hue_shift + 4 * math.pi / 3) * 0.5 + 0.5

            # Scale to 0-255 and clamp
            R = max(0, min(255, int(R_norm * 255)))
            G = max(0, min(255, int(G_norm * 255)))
            B = max(0, min(255, int(B_norm * 255)))

            color_code = get_true_color_code(R, G, B)
            
            # --- Character Selection (Intensity Mapping) ---
            
            # Scale the normalized value to the character index range [0, 7]:
            char_index = int(normalized_value * NUM_CHARS)

            # Clamp the index safely within the bounds
            if char_index < 0:
                char_index = 0
            elif char_index >= NUM_CHARS:
                char_index = NUM_CHARS - 1
            
            char_to_print = SPECTRUM_CHARS[char_index]
            
            # Append color, character, and reset code
            line += color_code + char_to_print + ANSI_RESET

        # Print the fully generated line
        print(line)
        sys.stdout.flush() 

        # Pause to control the "animation speed"
        time.sleep(SLEEP_TIME)

    # Print a final reset code
    print(ANSI_RESET + "\n--- Animation Finished ---")

# Execute the function
if __name__ == "__main__":
    # Check if the terminal likely supports True Color
    if sys.stdout.isatty():
        try:
            animate_spectrum()
        except KeyboardInterrupt:
            print(ANSI_RESET + "\nAnimation stopped by user.")
    else:
        print("Warning: Terminal does not appear to support interactive TTY output.")
        print("The animation may not display correctly or colors may be missing.")
        time.sleep(2)
        try:
            animate_spectrum()
        except KeyboardInterrupt:
            print(ANSI_RESET + "\nAnimation stopped by user.")


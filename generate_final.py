import pyautogui
import os
import time

# Define the coordinates of the 10x10 grid and cell size
x_start = 804
y_start = 481
cell_size = 30  # Updated from 29 to 30 pixels

# Define the target frame duration (1 frame per second = 1000 milliseconds)
frame_duration = 1000  # milliseconds

# Define the screenshot coordinates and output folder
screenshot_coords = (727, 193, 1171, 923)

# Define the base directory for relative paths
base_dir = os.path.dirname(__file__)  # Get the directory of the current script

# Define input and output directories
final_sequence_folder = os.path.join(base_dir, "bad_apple", "final_sequence")
input_folder = os.path.join(base_dir, "bad_apple", "matrices_sequence")

# Ensure the final sequence folder exists
os.makedirs(final_sequence_folder, exist_ok=True)

# Function to click a cell at a given row and column
def click_cell(row, col):
    x = x_start + col * cell_size + cell_size / 2
    y = y_start + row * cell_size + cell_size / 2
    pyautogui.click(x, y)

# Function to draw a binary matrix with batched clicks
def draw_binary_matrix(matrix):
    start_time = time.time()  # Record the start time

    # Collect all click positions
    click_positions = []
    for row in range(10):
        for col in range(10):
            state = matrix[row][col]
            if state == 0:
                click_positions.append((row, col))
    
    # Perform clicks in a batch
    for row, col in click_positions:
        click_cell(row, col)
    
    end_time = time.time()  # Record the end time
    duration = end_time - start_time
    print(f"Time to draw frame: {duration:.4f} seconds")

    # Calculate and introduce delay to make each frame fit into the desired time
    elapsed_time = duration * 1000  # Convert to milliseconds
    if elapsed_time < frame_duration:
        time.sleep((frame_duration - elapsed_time) / 1000)  # Convert back to seconds

# Function to clear the matrix by clicking on a specific location
def clear_matrix():
    pyautogui.click(999, 442)

# Function to take a screenshot
def take_screenshot(frame_number):
    x1, y1, x2, y2 = screenshot_coords
    screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    file_path = os.path.join(final_sequence_folder, f"bad_apple_final_{frame_number:03d}.png")
    screenshot.save(file_path)
    print(f"Screenshot saved as: {file_path}")

# Record the start time
start_time = time.time()

# Process each image in the input folder with proper numerical sorting
def numerical_sort_key(filename):
    # Extract the numerical part from the filename
    basename = os.path.splitext(filename)[0]
    parts = basename.split('_')
    return int(parts[-1])

files = sorted((f for f in os.listdir(input_folder) if f.endswith('.txt')), key=numerical_sort_key)

for index, filename in enumerate(files):
    current_time = time.time()
    # Check if 10 seconds have passed
    # if current_time - start_time >= 10:
    #     break

    file_path = os.path.join(input_folder, filename)
    
    # Read the binary matrix from the file
    with open(file_path, 'r') as file:
        matrix = [list(map(int, line.strip().split())) for line in file]
    
    # Print the matrix to the terminal
    print(f"Frame: {filename}")
    for row in matrix:
        print(' '.join(map(str, row)))
    
    # Draw the matrix on the website with batched clicks and time the operation
    draw_binary_matrix(matrix)
    
    # Take a screenshot after drawing but before clearing the matrix
    take_screenshot(index + 1)
    
    # Click to clear the matrix
    clear_matrix()

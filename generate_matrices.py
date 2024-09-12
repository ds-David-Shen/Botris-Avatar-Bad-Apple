import os
from PIL import Image
import numpy as np

# Define the base directory for relative paths
base_dir = os.path.dirname(__file__)  # Get the directory of the current script

# Define input and output directories
input_folder = os.path.join(base_dir, "bad_apple", "image_sequence")
output_folder = os.path.join(base_dir, "bad_apple", "matrices_sequence")

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

def convert_image_to_binary_matrix(image_path):
    """Convert an image to a 10x10 binary matrix."""
    # Open the image and convert it to grayscale
    with Image.open(image_path).convert('L') as img:
        # Resize the image to 10x10 pixels
        img_resized = img.resize((10, 10))
        # Convert to a numpy array
        img_array = np.array(img_resized)
        # Convert the image array to a binary matrix (0 and 1)
        binary_matrix = (img_array > 128).astype(int)
    return binary_matrix

def save_matrix_to_file(matrix, output_path):
    """Save the binary matrix to a text file."""
    with open(output_path, 'w') as f:
        for row in matrix:
            f.write(' '.join(map(str, row)) + '\n')

# Process each image file in the input folder
for i in range(1, 6563):
    # Construct the input file path
    input_file = os.path.join(input_folder, f'bad_apple_{i:03}.png')
    # Construct the output file path
    output_file = os.path.join(output_folder, f'bad_apple_{i:03}.txt')
    
    # Convert the image to a binary matrix
    binary_matrix = convert_image_to_binary_matrix(input_file)
    
    # Save the binary matrix to a text file
    save_matrix_to_file(binary_matrix, output_file)

print("Conversion completed!")

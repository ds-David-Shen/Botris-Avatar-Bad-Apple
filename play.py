import cv2
import pygame
import os
import time
import numpy as np
from scipy.io import wavfile

def wrap_text(text, font, max_width):
    """
    Wraps text to fit within a maximum width for a given font.
    """
    lines = []
    words = text.split(' ')
    line = ''
    for word in words:
        test_line = f"{line} {word}".strip()
        (w, _), _ = cv2.getTextSize(test_line, font[0], font[1], font[2])
        if w <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

# Define the relative paths to the images, audio file, and video file
base_dir = os.path.dirname(__file__)  # Get the directory of the current script
final_sequence_folder = os.path.join(base_dir, "bad_apple", "final_sequence")
audio_file = os.path.join(base_dir, "bad_apple", "bad_apple.wav")
pv_video_file = os.path.join(base_dir, "bad_apple", "bad_apple_pv.mp4")

# Initialize pygame mixer for audio playback
pygame.mixer.init()
pygame.mixer.music.load(audio_file)

target_duration = 3 * 60 + 39  # 209 seconds

# Get the audio duration using scipy
sample_rate, audio_data = wavfile.read(audio_file)
audio_duration = len(audio_data) / sample_rate

# Use the shorter duration of either the audio or the target
actual_duration = min(target_duration, audio_duration)

# Sort image files in the correct numerical order
def numerical_sort_key(filename):
    basename = os.path.splitext(filename)[0]
    parts = basename.split('_')
    return int(parts[-1])

image_files = sorted(
    [f for f in os.listdir(final_sequence_folder) if f.endswith('.png')],
    key=numerical_sort_key
)

# Total number of frames
total_frames = len(image_files)

# Calculate the frame rate to fit the total number of frames into the target duration
frame_rate = 34
frame_duration = 1.0 / frame_rate

# Play the audio
pygame.mixer.music.play()

# Initialize OpenCV windows
cv2.namedWindow("Bad Apple", cv2.WINDOW_NORMAL)

# Initialize video capture for the PV video
pv_capture = cv2.VideoCapture(pv_video_file)
if not pv_capture.isOpened():
    print("Error: Could not open video file.")
    exit()

# Get video dimensions
video_width = int(pv_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(pv_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Set image dimensions based on the first image
first_image_path = os.path.join(final_sequence_folder, image_files[0])
first_img = cv2.imread(first_image_path)
if first_img is None:
    print("Error: Could not load first image.")
    exit()
image_width, image_height = first_img.shape[1], first_img.shape[0]

# Set the combined dimensions for the display
combined_width = image_width + video_width
combined_height = max(image_height, video_height)

# Set text width to approximately half of the combined width
max_text_width = combined_width // 2

# Description text
description_text = ("This program displays a sequence of 'Bad Apple' images on the left side of the screen using the botris avatar editor, "
                    "while simultaneously showing the 'Bad Apple PV' video on the right side.")

# Font settings
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.8
font_thickness = 2
text_color = (255, 255, 255)

# Wrap the text
wrapped_text = wrap_text(description_text, (font, font_scale, font_thickness), max_text_width)
text_height = sum([cv2.getTextSize(line, font, font_scale, font_thickness)[0][1] + 10 for line in wrapped_text])

# Start time to calculate FPS
start_time = time.time()
frame_index = 0

# Play images in sequence while audio is playing
while pygame.mixer.music.get_busy() and frame_index < total_frames and (time.time() - start_time) < actual_duration:
    # Load and display the image
    img_path = os.path.join(final_sequence_folder, image_files[frame_index])
    img = cv2.imread(img_path)
    
    # Check if the image is loaded successfully
    if img is None:
        print(f"Error: Could not load image {img_path}")
        break

    # Create a black background with the size of the combined width and height
    combined_frame = np.zeros((combined_height, combined_width, 3), dtype=np.uint8)

    # Place the image on the left side
    combined_frame[0:image_height, 0:image_width] = img

    # Read the PV video frame
    ret, pv_frame = pv_capture.read()
    if not ret:
        # If no more frames, use a black frame
        pv_frame = np.zeros((video_height, video_width, 3), dtype=np.uint8)
    
    # Place the video frame on the right side
    combined_frame[0:video_height, image_width:combined_width] = pv_frame

    # Add wrapped description text at the bottom right
    y_offset = combined_height - text_height
    for line in wrapped_text:
        # Calculate the text width and start position
        text_size, _ = cv2.getTextSize(line, font, font_scale, font_thickness)
        text_width = text_size[0]
        x_offset = combined_width - text_width - 10  # 10 pixels from the right edge
        cv2.putText(combined_frame, line, (x_offset, y_offset), font, font_scale, text_color, font_thickness, cv2.LINE_AA)
        y_offset += text_size[1] + 10

    # Display the combined frame
    cv2.imshow("Bad Apple", combined_frame)

    # Wait for the frame duration or until the window is closed
    cv2.waitKey(int(frame_duration * 1000))

    # Calculate FPS and print it in the terminal
    elapsed_time = time.time() - start_time
    fps = (frame_index + 1) / elapsed_time
    print(f"Current FPS: {fps:.2f}")

    # Ensure synchronization with frame rate
    if elapsed_time < frame_duration:
        time.sleep(frame_duration - elapsed_time)

    # Move to the next frame
    frame_index += 1

# Stop the audio playback after the last image or when the duration is reached
pygame.mixer.music.stop()

# Release the PV video capture and close the OpenCV windows
pv_capture.release()
cv2.destroyAllWindows()

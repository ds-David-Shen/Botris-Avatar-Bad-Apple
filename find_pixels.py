from pynput import mouse

# Define the top-left corner of the 10x10 pixel area
top_left_x, top_left_y = 100, 200  # Replace with your coordinates

# Define the size of the area
width, height = 10, 10

# Check if the click is within the specified area
def check_click_validity(x, y, top_left_x, top_left_y, width, height):
    if (top_left_x <= x < top_left_x + width) and (top_left_y <= y < top_left_y + height):
        print("valid")
    else:
        print("invalid")

# Define the on_click function
def on_click(x, y, button, pressed):
    if pressed:  # Only check on mouse button press
        print(f"Mouse position: x={x}, y={y}")
        check_click_validity(x, y, top_left_x, top_left_y, width, height)

# Set up the listener
with mouse.Listener(on_click=on_click) as listener:
    listener.join()

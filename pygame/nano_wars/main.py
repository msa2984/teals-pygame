import sys
import pygame
from pygame.locals import *
from models.cell import Cell

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))

# Define the Circle class

# Create a list of circles
cells = [
    Cell((150, 150), 50, (255, 0, 0)),  # Red circle at (150, 150)
    Cell((300, 300), 70, (0, 0, 255)),  # Blue circle at (300, 300)
    Cell((500, 200), 40, (83, 83, 83))   # Green circle at (500, 200)
]
line_active = False  # Variable to track if the line is currently being drawn
highlighted_cell = None  # Track which cell is currently highlighted

# Game loop.
while True:
    screen.fill((0, 0, 0))  # Fill screen with black

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Handle mouse button down event
        elif event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Check if any of the cells is clicked
            for cell in cells:
                if cell.check_click(mouse_pos):
                    if cell.color == (0, 0, 255):  # If the cell is blue
                        line_active = True  # Start drawing the line
                        highlighted_cell = cell  # Track the highlighted cell
                        cell.is_highlighted = True
                        cell.line_end = mouse_pos  # Store the cursor position to draw the line
                    else:
                        # Reset line state if clicked on a non-blue cell
                        line_active = False
                        cell.is_highlighted = False
                        cell.line_end = None

        # Handle mouse motion event
        elif event.type == MOUSEMOTION:
            if line_active and highlighted_cell:  # Only update if the line is active
                mouse_pos = pygame.mouse.get_pos()
                highlighted_cell.line_end = mouse_pos  # Update the end of the line to follow the cursor

        # Handle mouse button up event
        elif event.type == MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if not any(cell.check_click(mouse_pos) for cell in cells):
                line_active = False  # Stop drawing the line when clicked outside
                if highlighted_cell:
                    highlighted_cell.is_highlighted = False  # Remove highlighting
                    highlighted_cell.line_end = None  # Stop drawing the line
                    highlighted_cell = None  # Clear the highlighted cell tracker

    # Get the current time in milliseconds
    current_time = pygame.time.get_ticks()

    # Draw all the cells
    for cell in cells:
        cell.draw(screen, current_time)

    pygame.display.flip()  # Update the display
    fpsClock.tick(fps)  # Control the frame rate


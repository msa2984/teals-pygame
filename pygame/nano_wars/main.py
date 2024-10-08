import sys
import pygame
from pygame.locals import *
from models.cell import Cell

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))

# Create a list of circles
cells = [
    Cell((150, 150), 50, (255, 0, 0)),  # Red circle at (150, 150)
    Cell((600, 150), 50, (255, 0, 0)),  # Red circle at (600, 150)
    Cell((500, 200), 40, (255, 0, 0)),  # Green circle at (500, 200)
    Cell((300, 300), 70, (0, 0, 255)),  # Blue circle at (300, 300)
    Cell((100, 300), 40, (0, 0, 255)),  # Blue circle at (100, 300)
]

line_active = False  # Variable to track if the line is currently being drawn
highlighted_cells = []  # List to track which cells are currently highlighted

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
                        if cell not in highlighted_cells:
                            highlighted_cells.append(cell)  # Add the cell to the highlighted list
                        line_active = True  # Start drawing the line
                        cell.is_highlighted = True
                        cell.line_end = mouse_pos  # Store the cursor position to draw the line
                    else:
                        # Reset line state if clicked on a non-blue cell
                        line_active = False
                        for highlighted in highlighted_cells:
                            highlighted.is_highlighted = False
                        highlighted_cells.clear()  # Clear highlighted cells
                        for cell in cells:
                            cell.line_end = None

        # Handle mouse motion event
        elif event.type == MOUSEMOTION:
            if line_active and highlighted_cells:  # Only update if the line is active
                mouse_pos = pygame.mouse.get_pos()
                # Update the end of the line for all highlighted cells
                for highlighted in highlighted_cells:
                   if not highlighted.snapped_cell:
                      highlighted.line_end = mouse_pos  # Update the end of the line to follow the cursor

        # Handle mouse button up event
        elif event.type == MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if not any(cell.check_click(mouse_pos) for cell in cells):
                line_active = False  # Stop drawing the line when clicked outside
                for highlighted in highlighted_cells:
                    highlighted.is_highlighted = False  # Remove highlighting
                    highlighted.line_end = None  # Stop drawing the line
                highlighted_cells.clear()  # Clear the highlighted cells tracker

    # Get the current time in milliseconds
    current_time = pygame.time.get_ticks()

    # Draw all the cells (circles)
    for cell in cells:
        cell.draw(screen, current_time, cells)

    # # Draw lines for all highlighted cells
    # for highlighted in highlighted_cells:
    #     if highlighted.line_end:
    #         edge_position = highlighted.get_edge_position(highlighted.line_end)
    #         pygame.draw.line(screen, (255, 255, 255), edge_position, highlighted.line_end, 2)

    pygame.display.flip()  # Update the display
    fpsClock.tick(fps)  # Control the frame rate

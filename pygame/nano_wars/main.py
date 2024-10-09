import sys
import pygame
from pygame.locals import *
from models.cell import Cell
from models.mini_cell import MiniCell, spawn_and_move_mini_cells
from constants.color import RED, BLUE, GRAY
from logic.enemy_cell import enemy_cell_logic
from logic.friendly_cell import friendly_cell_logic

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

width, height = 1920, 1080
screen = pygame.display.set_mode((width, height))

# Create a list of circles
cells = [
    Cell((150, 150), 50, RED, counter=1),  # Red circle at (150, 150)
    Cell((600, 150), 50, RED, counter=1),  # Red circle at (600, 150)
    Cell((500, 200), 40, GRAY, counter=3),  # Green circle at (500, 200)
    Cell((300, 300), 90, BLUE, counter=1),  # Blue circle at (300, 300)
    Cell((100, 300), 40, BLUE, counter=1),  # Blue circle at (100, 300)
]

line_active = False  # Variable to track if the line is currently being drawn
dragging = False
start_pos = None
highlighted_cells = []  # List to track which cells are currently highlighted
selection_rect = None
mini_cells = []  # List to track the mini cells

def check_selection(cells, selection_rect):
    selected_cells = []
    
    for cell in cells:
        if cell.color == BLUE:
            # Check if the cell is within the selection rectangle
            if selection_rect.colliderect(cell.get_rect()):  # Use get_rect() method of Cell
                selected_cells.append(cell)
    
    return selected_cells

# Game loop.
press_start_time = None
press_duration = 0

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
            dragging = True
            start_pos = pygame.mouse.get_pos()  # Get the starting position
            selection_rect = None  # Only create the rectangle if dragging outside cells
            press_start_time = pygame.time.get_ticks()  # Record the start time
            press_duration = 0  # Reset duration when starting to drag
            # Check if any of the cells is clicked
            for cell in cells:
                if cell.check_click(mouse_pos):
                    print(cell)
                    if cell.color == BLUE:  # If the cell is blue
                        selection_rect = None  # Do not draw selection rectangle if starting inside a blue cell
                        if cell not in highlighted_cells and selection_rect is None and len(highlighted_cells) == 0:
                            highlighted_cells.append(cell)  # Add the cell to the highlighted list
                            line_active = True  # Start drawing the line
                            cell.is_highlighted = True
                            cell.line_end = mouse_pos  # Store the cursor position to draw the line
                        elif len(highlighted_cells) >= 1:
                            spawn_and_move_mini_cells(highlighted_cells, cell, mini_cells)
                            line_active = friendly_cell_logic(highlighted_cells=highlighted_cells, line_active=line_active, cell=cell)
                    elif cell.color == GRAY and highlighted_cells:  # If clicked on a gray cell and any blue cells are highlighted
                        line_active = enemy_cell_logic(highlighted_cells=highlighted_cells, line_active=line_active, cell=cell)
                        spawn_and_move_mini_cells(highlighted_cells, cell, mini_cells)
                    elif cell.color == RED and highlighted_cells:
                        line_active = enemy_cell_logic(highlighted_cells=highlighted_cells, line_active=line_active, cell=cell)
                        spawn_and_move_mini_cells(highlighted_cells, cell, mini_cells)
                    break  # Stop checking other cells once a valid click inside a cell is detected
            else:
                selection_rect = pygame.Rect(start_pos, (0, 0))  # Initialize rectangle if clicked outside cells

        # Handle mouse motion event
        elif event.type == MOUSEMOTION:
            if dragging:
                current_pos = pygame.mouse.get_pos()
                
                # Calculate the press duration
                if press_start_time is not None:  # Ensure it has been set
                    press_duration = pygame.time.get_ticks() - press_start_time  # Calculate the duration
                    print(press_duration)
                
                # Highlight any blue cells being hovered over during dragging
                for cell in cells:
                    if cell.color == BLUE and cell.check_click(current_pos) and cell not in highlighted_cells and selection_rect is None and press_duration > 100:
                        highlighted_cells.append(cell)  # Highlight the cell
                        cell.is_highlighted = True
                        line_active = True
                        cell.line_end = mouse_pos  # Optionally, update the line end if needed

                # Only draw the rectangle if selection_rect is not None (i.e., not dragging over cells)
                if selection_rect is not None:
                    selection_rect.width = current_pos[0] - start_pos[0]
                    selection_rect.height = current_pos[1] - start_pos[1]

            if line_active and highlighted_cells:  # Only update if the line is active
                mouse_pos = pygame.mouse.get_pos()
                # Update the end of the line for all highlighted cells
                for highlighted in highlighted_cells:
                    if not highlighted.snapped_cell:
                        highlighted.line_end = mouse_pos  # Update the end of the line to follow the cursor
        # Handle mouse button up event
        elif event.type == MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            dragging = False
            
            # Reset press duration and start time
            press_start_time = None  # Reset start time
            press_duration = 0  # Reset duration

            if selection_rect is not None:
                # Check which cells are selected based on the selection rectangle
                selected_cells = check_selection(cells, selection_rect)

                # If the mouse clicked on any of the cells, highlight them
                if selected_cells:
                    highlighted_cells.extend(selected_cells)  # Add newly selected cells to the highlighted list
                    for cell in selected_cells:
                        cell.is_highlighted = True  # Set highlight state
                        print("HIGHLIGHT 2")
                        cell.line_end = mouse_pos  # Store the cursor position to draw the line

                    line_active = True  # Activate line drawing if any cells are highlighted
                else:
                    # If clicked outside of any cells, clear highlighted cells only if no cell was clicked
                    if not any(cell.check_click(mouse_pos) for cell in cells):
                        line_active = False  # Stop drawing the line when clicked outside
                        for highlighted in highlighted_cells:
                            highlighted.is_highlighted = False  # Remove highlighting
                            highlighted.line_end = None  # Stop drawing the line
                        highlighted_cells.clear()  # Clear the highlighted cells tracker

    # Get the current time in milliseconds
    current_time = pygame.time.get_ticks()
    
    for mini_cell in mini_cells[:]:
        mini_cell.move()
        mini_cell.draw(screen)
        if mini_cell.reached_target():
            mini_cells.remove(mini_cell)
        
    # Draw all the cells (circles)
    for cell in cells:
        cell.draw(screen, current_time, cells)
        if cell.counter == 0:
           cell.color = GRAY
    if dragging and selection_rect:
        # Get the current mouse position
        current_pos = pygame.mouse.get_pos()
        
        # Calculate the top-left corner and size of the rectangle
        x1, y1 = start_pos
        x2, y2 = current_pos
        
        # Determine the rectangle's position and size
        selection_rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
    
        # Draw the selection rectangle
        pygame.draw.rect(screen, (173, 216, 230), selection_rect, 2)  # Light blue outline
  
    pygame.display.flip()  # Update the display
    fpsClock.tick(fps)  # Control the frame rate

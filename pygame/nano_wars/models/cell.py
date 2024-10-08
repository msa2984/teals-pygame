import pygame
from pygame import *
import math

class Cell:
    def __init__(self, position, radius, color):
        self.position = position  # (x, y)
        self.radius = radius
        self.color = color
        self.highlight_color = (173, 216, 230)
        self.is_highlighted = False
        self.counter = 0
        self.last_update_time = 0
        self.update_interval = 1500  # 1.5 second
        self.font = pygame.font.SysFont(None, 48)
        self.text_color = (255, 255, 255)
        self.line_end = None  # Store the cursor position for the line
        
    @property
    def center(self):
        return (self.position[0], self.position[1])

    def draw(self, screen: Surface, current_time):
        # Update the counter if 1 second has passed
        if current_time - self.last_update_time >= self.update_interval:
            self.counter += 1
            self.last_update_time = current_time
        
        # Draw the circle
        pygame.draw.circle(screen, self.color, self.position, self.radius)

        # Draw the highlight outline if highlighted
        if self.is_highlighted:
            pygame.draw.circle(screen, self.highlight_color, self.position, self.radius + 5, 5)

        # Draw the line from the edge of the circle to the cursor
        if self.line_end:
            edge_position = self.get_edge_position(self.line_end)
            
            # Calculate the distance from the circle's center to the line_end position
            distance_to_edge = pygame.math.Vector2(self.center).distance_to(self.line_end)

            # Only draw the line if the line_end is outside the circle
            if distance_to_edge > self.radius:
                pygame.draw.line(screen, (255, 255, 255), edge_position, self.line_end, 2)

        # Render the counter as text inside the circle
        number = str(self.counter)
        text_surface = self.font.render(number, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.position)
        screen.blit(text_surface, text_rect)

    def check_click(self, mouse_pos):
        # Function to check if the mouse click is inside this circle
        dx = mouse_pos[0] - self.position[0]
        dy = mouse_pos[1] - self.position[1]
        return (dx * dx + dy * dy) <= (self.radius * self.radius)

    def get_edge_position(self, mouse_pos):
        """Calculate the point just outside the edge of the circle based on the cursor position."""
        dx = mouse_pos[0] - self.position[0]
        dy = mouse_pos[1] - self.position[1]
        
        # Calculate the angle between the circle center and the mouse position
        angle = math.atan2(dy, dx)
        
        # Calculate the x, y coordinates just outside the circle's edge (using a slightly larger radius)
        edge_x = self.position[0] + (self.radius + 5) * math.cos(angle)
        edge_y = self.position[1] + (self.radius + 5) * math.sin(angle)
        
        return (edge_x, edge_y)

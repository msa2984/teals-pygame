import math
import pygame
from constants.color import BLUE
from models.cell import Cell

class MiniCell:
    def __init__(self, start_pos, target_pos, color, transfer_total, target_cell, speed=1):
        self.pos = list(start_pos)  # Current position of the mini cell
        self.target_pos = target_pos  # Target position of the mini cell
        self.color = BLUE
        self.radius = 50  # Radius of the mini cell
        self.speed = speed  # Movement speed
        self.direction = self.calculate_direction()  # Direction towards the target
        self.transfer_total = transfer_total
        self.target_cell = target_cell

    def calculate_direction(self):
        # Calculate the direction vector towards the target
        distance, dx, dy = self.calculate_distance()
        print(f"DISTANCE: {distance}")
        return (dx / distance, dy / distance) if distance != 0 else (0, 0)
    
    def calculate_distance(self):
        dx = self.target_pos[0] - self.pos[0]
        dy = self.target_pos[1] - self.pos[1]
        distance = math.sqrt(dx**2 + dy**2)
        self.distance = distance
        return distance, dx, dy

    def move(self):
        # Move the mini cell in the direction of the target
        self.pos[0] += self.direction[0] * self.speed
        self.pos[1] += self.direction[1] * self.speed

    def reached_target(self):
        # Check if the mini cell has reached the target position
        result = math.dist(self.pos, self.target_pos) < self.radius
        # print(result)
        return result
    
    def get_radius(self):
        # Scale the radius based on transfer_total proportionally
        scaling_factor = self.radius / 100 / 1.11 # Assuming 100 corresponds to the full radius
        scaled_radius = scaling_factor * self.transfer_total
        return scaled_radius if scaled_radius < self.radius else self.radius

    
    def draw(self, screen):
        # Draw the mini cell as a circle
        radius = self.get_radius()  # Get the dynamic radius
        pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), radius)
        
        # Draw the transfer_total slightly above the mini cell
        font = pygame.font.SysFont(None, 24)  # You can adjust the font size
        text_surface = font.render(str(self.transfer_total), True, (255, 255, 255))  # White color for text
        
        # Calculate text position (slightly above the circle)
        text_x = int(self.pos[0])  # Center horizontally
        text_y = int(self.pos[1]) - radius - 5  # Adjust this value to move the text higher or lower
        text_rect = text_surface.get_rect(center=(text_x, text_y))  # Center the text above the mini cell
        
        # Draw the text on the screen
        screen.blit(text_surface, text_rect)

    

def spawn_and_move_mini_cells(cell: Cell, target_cell: Cell, mini_cells: list, transfer_total: int):
    start_pos = cell.position
    target_pos = target_cell.position
    mini_cell = MiniCell(start_pos=start_pos, target_pos=target_pos, color=cell.color, transfer_total=transfer_total, target_cell=target_cell)
    mini_cells.append(mini_cell)
    return mini_cell


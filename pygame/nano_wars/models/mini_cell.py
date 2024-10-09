import math
import pygame
from constants.color import BLUE

class MiniCell:
    def __init__(self, start_pos, target_pos, color, speed=5):
        self.pos = list(start_pos)  # Current position of the mini cell
        self.target_pos = target_pos  # Target position of the mini cell
        self.color = BLUE
        self.radius = 5  # Radius of the mini cell
        self.speed = speed  # Movement speed
        self.direction = self.calculate_direction()  # Direction towards the target

    def calculate_direction(self):
        # Calculate the direction vector towards the target
        dx = self.target_pos[0] - self.pos[0]
        dy = self.target_pos[1] - self.pos[1]
        distance = math.sqrt(dx**2 + dy**2)
        print(f"DISTANCE: {distance}")
        return (dx / distance, dy / distance) if distance != 0 else (0, 0)

    def move(self):
        # Move the mini cell in the direction of the target
        self.pos[0] += self.direction[0] * self.speed
        self.pos[1] += self.direction[1] * self.speed

    def reached_target(self):
        # Check if the mini cell has reached the target position
        return math.dist(self.pos, self.target_pos) < self.radius

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)
    

def spawn_and_move_mini_cells(highlighted_cell, target_cell, mini_cells: list):
    for cell in highlighted_cell:
        start_pos = cell.position
        target_pos = target_cell.position
        mini_cell = MiniCell(start_pos, target_pos, cell.color)
        mini_cells.append(mini_cell)


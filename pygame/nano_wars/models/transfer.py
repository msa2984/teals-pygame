from models.mini_cell import MiniCell
from models.cell import Cell

class Transfer:
    def __init__(self, target_count: int, target_cell: Cell, source_minicell: MiniCell, distance: float):
        self.target_count = target_count
        self.target_cell = target_cell
        self.source_minicell = source_minicell
        self.distance = distance

    def __repr__(self):
        return f"Transfer(target_count={self.target_count}, target_cell={self.target_cell}, source_minicell={self.source_minicell}, distance={self.distance})"

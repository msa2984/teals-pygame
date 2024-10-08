from models.cell import Cell

def gray_cell_logic(highlighted_cells: list, line_active: bool, cell: Cell) -> bool:
    if highlighted_cells:
        highlighted_cell = highlighted_cells[0]  # Get the first highlighted blue cell
        if highlighted_cell.counter > 0 and cell.counter > 0:
            amount_to_transfer = min(highlighted_cell.counter, cell.counter)
            highlighted_cell.counter -= amount_to_transfer
            cell.counter -= amount_to_transfer
        # Reset highlighting for all highlighted cells
        for highlighted in highlighted_cells:
            line_active = False
            highlighted.is_highlighted = False
            highlighted.line_end = None
        highlighted_cells.clear()  # Clear highlighted cells
        highlighted_cell = None  # Clear highlighted cell tracker
        return False  # Indicate that the line is not active anymore
    return line_active  # Return the current state if nothing happens
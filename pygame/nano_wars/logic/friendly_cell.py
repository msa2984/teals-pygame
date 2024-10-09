from models.cell import Cell

def friendly_cell_logic(highlighted_cells: list, line_active: bool, cell: Cell) -> bool:
    if highlighted_cells:
        total_transfer = 0  # Initialize total transfer amount

        # Calculate the total amount to transfer from highlighted cells
        for highlighted in highlighted_cells:
            if highlighted.counter >= 2:  # Only consider cells with at least 2
                transfer_amount = highlighted.counter // 2  # Half of their current value
                total_transfer += transfer_amount  # Add to the total transfer
                highlighted.counter -= transfer_amount  # Deduct from the highlighted cell

        # Proceed to subtract from the gray cell if there is any transfer amount
        if total_transfer > 0:
            print(f"Total transfer: {total_transfer}, friendly cell counter before: {cell.counter}")

            # Subtract the total transfer amount from the gray cell
            cell.counter += total_transfer  # This will allow it to go negative

            # Print the gray cell's counter to see its value after subtraction
            print(f"friendly cell counter after subtraction: {cell.counter}")

    return line_active  # Return the current state if nothing happens




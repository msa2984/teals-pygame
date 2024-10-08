from models.cell import Cell

def gray_cell_logic(highlighted_cells: list, line_active: bool, cell: Cell) -> bool:
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
            print(f"Total transfer: {total_transfer}, Gray cell counter before: {cell.counter}")

            # Subtract the total transfer amount from the gray cell
            cell.counter -= total_transfer  # This will allow it to go negative

            # Print the gray cell's counter to see its value after subtraction
            print(f"Gray cell counter after subtraction: {cell.counter}")

            # Check if the gray cell's counter goes below zero
            if cell.counter < 0:
                print("yo")  # This should now print if the counter goes negative
                excess_amount = abs(cell.counter)  # Calculate the excess amount
                cell.counter = 0  # Set gray cell counter to 0
                cell.color = highlighted_cells[0].color  # Change the gray cell's color to blue
                cell.counter += excess_amount  # Add excess amount to the new blue cell
                
                # Print to confirm the cell color change and the new counter value
                print(f"Gray cell became blue with counter: {cell.counter}")
        
        return False  # Indicate that the line is not active anymore
    return line_active  # Return the current state if nothing happens




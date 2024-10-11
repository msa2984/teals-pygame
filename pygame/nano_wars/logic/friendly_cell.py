from models.cell import Cell
from models.mini_cell import MiniCell, spawn_and_move_mini_cells
from models.transfer import Transfer
from pygame import *

# def friendly_cell_logic(highlighted_cells: list, line_active: bool, cell: Cell, mini_cells: MiniCell, screen: Surface) -> bool:
    
#     if highlighted_cells:
#         total_transfer = 0  # Initialize total transfer amount

#         # Calculate the total amount to transfer from highlighted cells
#         for highlighted in highlighted_cells:
#             if highlighted.counter >= 2:  # Only consider cells with at least 2
#                 spawn_and_move_mini_cells(highlighted, cell, mini_cells)
#                 print(mini_cells)
#                 while mini_cells:
#                     for mini_cell in mini_cells:
#                         mini_cell.move()
#                         mini_cell.draw(screen)
#                         if mini_cell.reached_target():
#                             print("reached target")
#                             mini_cells.remove(mini_cell)
#                             transfer_amount = highlighted.counter // 2  # Half of their current value
#                             total_transfer += transfer_amount  # Add to the total transfer
#                             highlighted.counter -= transfer_amount  # Deduct from the highlighted cell

#         # Proceed to subtract from the gray cell if there is any transfer amount
#         if total_transfer > 0:
#             print(f"Total transfer: {total_transfer}, friendly cell counter before: {cell.counter}")

#             # Subtract the total transfer amount from the gray cell
#             cell.counter += total_transfer  # This will allow it to go negative

#             # Print the gray cell's counter to see its value after subtraction
#             print(f"friendly cell counter after subtraction: {cell.counter}")

#     return line_active  # Return the current state if nothing happens

# This function should handle the transfer logic only
def handle_transfer(highlighted_cells, target_cell, mini_cells) -> list[Transfer]:
    transfer_obj_list = []  # List to store transfer objects
    
    for highlighted in highlighted_cells:
        if highlighted.counter >= 2:
            transfer_amount = highlighted.counter // 2
            spawn_and_move_mini_cells(highlighted, target_cell, mini_cells, transfer_total=transfer_amount)  # Spawn mini-cells
            
            highlighted.counter -= transfer_amount

            # Create a Transfer object and append to the list
            # transfer_obj = Transfer(target_count=transfer_amount, target_cell=target_cell, source_minicell=mini_cell, distance=mini_cell.distance)
            # transfer_obj_list.append(transfer_obj)
    return transfer_obj_list  # Return the list of Transfer objects

# This function should manage the movement and drawing of mini-cells
def update_mini_cells(mini_cells: list[MiniCell], screen):
    # Iterate over mini-cells and update them
    for mini_cell in mini_cells[:]:  # Use slice to safely remove during iteration
        # print(mini_cell.distance)
        mini_cell.move()
        mini_cell.draw(screen)
        if mini_cell.reached_target():
            mini_cell.target_cell.counter += mini_cell.transfer_total
            print("reached target")
            mini_cells.remove(mini_cell)
            return True







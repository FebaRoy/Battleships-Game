from typing import Optional
from support import *


def create_empty_board(size: int) -> list:
    """Creates an empty board with the given size."""
    return [[EMPTY_SQUARE for _ in range(size)] for _ in range(size)]


def print_board(board: list, show_ships: bool = True) -> None:
    """Prints the game board.

    Parameters:
        board: The game board to print.
        show_ships: Whether to display the ship locations or hide them.
    """
    size = len(board)
    print("  " + " ".join(chr(ord('A') + i) for i in range(size)))
    for i, row in enumerate(board):
        display_row = [
            (cell if show_ships or cell not in [ACTIVE_SHIP_SQUARE] else EMPTY_SQUARE)
            for cell in row
        ]
        print(str(i + 1).rjust(2) + " " + ROW_SEPARATOR.join(display_row))


def save_output(board: list, filename: str) -> None:
    """Saves the current board state to a file in the gameplay folder."""
    with open(f'gameplay/{filename}', 'w') as file:
        file.write("  " + " ".join(chr(ord('A') + i) for i in range(len(board))) + "\n")
        for i, row in enumerate(board):
            file.write(str(i + 1).rjust(2) + " " + ROW_SEPARATOR.join(row) + "\n")


def get_coordinate_input(board_size: int, coordinate: str) -> Optional[Position]:
    """Validates a single coordinate input."""
    coordinate = coordinate.upper()
    if len(coordinate) != 2:
        print(INVALID_COORDINATE_LENGTH)
        return None
    letter, number = coordinate[0], coordinate[1]
    if letter < 'A' or letter >= chr(ord('A') + board_size):
        print(INVALID_COORDINATE_LETTER)
        return None
    if not number.isdigit() or int(number) < 1 or int(number) > board_size:
        print(INVALID_COORDINATE_NUMBER)
        return None
    return (ord(letter) - ord('A'), int(number) - 1)


def place_ship(board: list, ship_length: int) -> bool:
    """Prompts the player to place a ship on the board and validates the placement."""
    while True:
        coordinates_str = input(prompt_for_ship_coordinates(ship_length))
        coordinates = coordinates_str.split(',')

        # Check for the correct number of coordinates
        if len(coordinates) != ship_length:
            print(INVALID_COORDINATE_SEQUENCE_LENGTH)
            continue

        positions = []
        for coordinate in coordinates:
            # Validate each coordinate
            position = get_coordinate_input(len(board), coordinate.strip())
            if position is None:
                break
            positions.append(position)

        # If not all positions were valid, retry
        if len(positions) != ship_length:
            continue

        # Validate that the ship is either vertical or horizontal
        row_set = {pos[1] for pos in positions}
        col_set = {pos[0] for pos in positions}

        if len(row_set) != 1 and len(col_set) != 1:
            print(INVALID_BENDY_SHIP)
            continue

        # Validate that the ship is connected (no gaps)
        if len(row_set) == 1:  # Horizontal placement
            cols = sorted([pos[0] for pos in positions])
            if cols[-1] - cols[0] != ship_length - 1:
                print(INVALID_SHIP_CONNECTIONS)
                continue
        if len(col_set) == 1:  # Vertical placement
            rows = sorted([pos[1] for pos in positions])
            if rows[-1] - rows[0] != ship_length - 1:
                print(INVALID_SHIP_CONNECTIONS)
                continue

        # Check that the placement doesn't overlap existing ships
        for pos in positions:
            if board[pos[1]][pos[0]] != EMPTY_SQUARE:
                print(INVALID_SHIP_PLACEMENT)
                break
        else:
            # Place the ship if all validations passed
            for pos in positions:
                board[pos[1]][pos[0]] = ACTIVE_SHIP_SQUARE
            return True


def setup_phase() -> tuple[list, list]:
    """Sets up the game by prompting for board size and ship placements."""
    board_size = int(input("Enter board size : "))
    ship_sizes = list(map(int, input("Enter comma-separated ship sizes: ").split(',')))

    player_one_board = create_empty_board(board_size)
    player_two_board = create_empty_board(board_size)

    print(P1_PLACEMENT_MESSAGE)
    print_board(player_one_board)
    for size in ship_sizes:
        while not place_ship(player_one_board, size):
            pass
        print_board(player_one_board)
        save_output(player_one_board, 'player_one_board.txt')  # Save output for Player 1

    print(P2_PLACEMENT_MESSAGE)
    print_board(player_two_board)
    for size in ship_sizes:
        while not place_ship(player_two_board, size):
            pass
        print_board(player_two_board)
        save_output(player_two_board, 'player_two_board.txt')  # Save output for Player 2

    return player_one_board, player_two_board


def attack_position(board: list, position: Position) -> Result:
    """Handles an attack on a specific position on the board."""
    col, row = position  # Ensure we unpack correctly (col is for the horizontal, row for the vertical)
    if board[row][col] == ACTIVE_SHIP_SQUARE:
        board[row][col] = DEAD_SHIP_SQUARE
        return (True, "Hit!")
    elif board[row][col] == EMPTY_SQUARE:
        board[row][col] = MISS_SQUARE
        return (True, "Miss!")
    else:
        return (False, "Position already attacked.")



def check_for_win(board: list) -> bool:
    """Checks if all ships on the board have been destroyed."""
    for row in board:
        if ACTIVE_SHIP_SQUARE in row:
            return False
    return True


def turn_phase(board: list, player_name: str) -> bool:
    """Manages a single turn for a player."""
    print(f"{player_name}'s turn:")
    print_board(board, show_ships=False)  # Hide ship locations during gameplay
    while True:
        coordinate_input = input(TURN_INPUT_MESSAGE)
        position = get_coordinate_input(len(board), coordinate_input)
        if position is None:
            continue
        valid, message = attack_position(board, position)
        print(message)
        if valid:
            break
    save_output(board, f'{player_name.lower()}_board.txt')
    return check_for_win(board)


def play_game() -> None:
    """Main function to play the game."""
    player_one_board, player_two_board = setup_phase()

    game_over = False
    while not game_over:
        game_over = turn_phase(player_two_board, PLAYER_ONE)
        if game_over:
            print(GAME_OVER_GRAPHIC)
            print(f"{PLAYER_ONE} wins!")
            break

        print(NEXT_TURN_GRAPHIC)

        game_over = turn_phase(player_one_board, PLAYER_TWO)
        if game_over:
            print(GAME_OVER_GRAPHIC)
            print(f"{PLAYER_TWO} wins!")
            break

        print(NEXT_TURN_GRAPHIC)


if __name__ == "__main__":
    play_game()

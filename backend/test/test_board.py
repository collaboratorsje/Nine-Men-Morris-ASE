import pytest
from game_logic.board import Board
from game_logic.player import Player

@pytest.fixture
def board():
    return Board(game_type="9mm")  # Default to 9mm

def test_board_initialization(board):
    assert board.size == 7
    assert len(board.grid) == 7
    assert all(len(row) == 7 for row in board.grid)

def test_get_valid_positions(board):
    valid_positions = board.get_valid_positions()
    assert (0, 0) in valid_positions
    assert (6, 6) in valid_positions
    assert (3, 3) not in valid_positions  # Example of an invalid position

def test_is_valid_position(board):
    assert board.is_valid_position(0, 0) is True
    assert board.is_valid_position(3, 3) is False
    assert board.is_valid_position(6, 6) is True

def test_is_adjacent(board):
    # Test known adjacent positions
    assert board.is_adjacent(0, 0, 0, 3) is True
    assert board.is_adjacent(0, 0, 3, 0) is True
    # Test positions that are not adjacent
    assert board.is_adjacent(0, 0, 1, 1) is False
    assert board.is_adjacent(0, 3, 3, 6) is False

def test_check_for_mill(board):
    class MockPlayer:
        def __init__(self, player_id):
            self.player_id = player_id
    
    player = MockPlayer(player_id="X")

    # Place pieces to form a mill at top row
    board.grid[0][0] = "X"
    board.grid[0][3] = "X"
    board.grid[0][6] = "X"
    assert board.check_for_mill(0, 3, player) is True

    # Place pieces but not forming a mill
    board.grid[1][1] = "X"
    board.grid[1][3] = "X"
    board.grid[1][5] = None  # One piece missing
    assert board.check_for_mill(1, 3, player) is False

def test_check_for_mill_false(board):
    class MockPlayer:
        def __init__(self, player_id):
            self.player_id = player_id

    player = MockPlayer(player_id=1)

    # Place pieces that do not form a mill
    board.grid[0][0] = 1  # Top left
    board.grid[1][3] = 1  # Middle of the second row
    board.grid[5][5] = 1  # Bottom right of the sixth row

    # Check that no mill is detected at each of these positions
    assert board.check_for_mill(0, 0, player) is False, "No mill should be detected at (0, 0)"
    assert board.check_for_mill(1, 3, player) is False, "No mill should be detected at (1, 3)"
    assert board.check_for_mill(5, 5, player) is False, "No mill should be detected at (5, 5)"

def test_display(board, capsys):
    # Setup some pieces on the board
    board.grid[0][0] = "X"
    board.grid[1][3] = "O"
    board.grid[6][6] = "X"
    board.display()
    captured = capsys.readouterr()
    assert "X" in captured.out
    assert "O" in captured.out
    
def test_12mm_valid_positions():
    board = Board(game_type="12mm")
    valid_positions = board.get_valid_positions()
    assert (1, 1) in valid_positions
    assert (3, 3) not in valid_positions  # Still invalid center position


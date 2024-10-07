import pytest
from game_logic.board import Board

def test_board_initialization():
    board = Board()
    assert board.size == 7
    assert len(board.grid) == 7
    assert all(len(row) == 7 for row in board.grid)

def test_valid_positions():
    board = Board()
    valid_positions = board.get_valid_positions()
    assert (0, 0) in valid_positions
    assert (6, 6) in valid_positions
    assert (3, 3) not in valid_positions  # Example of an invalid position

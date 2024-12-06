import pytest
from game_logic.board import Board
from game_logic.computerplayer import ComputerPlayer
from game_logic.player import Player

@pytest.fixture
def board():
    return Board(game_type="9mm")  # Provide the required game_type argument

@pytest.fixture
def computer_player():
    return ComputerPlayer(player_id=2, pieces=9)

@pytest.fixture
def opponent():
    return Player(player_id=1, pieces=9)

def test_decide_placement_prioritize_mill(board, computer_player):
    # Set up board where a mill can be formed
    board.grid[0][0] = 2
    board.grid[0][3] = 2
    # Computer should choose (0, 6) to form a mill
    move = computer_player.decide_placement(board)
    assert move == (0, 6), "Computer should prioritize forming a mill."

def test_decide_placement_block_mill(board, computer_player, opponent):
    # Set up board where the opponent is close to forming a mill
    board.grid[0][0] = 1
    board.grid[0][3] = 1
    # Computer should choose (0, 6) to block the opponent
    move = computer_player.decide_placement(board)
    assert move == (0, 6), "Computer should prioritize blocking opponent's mill."

def test_decide_placement_random(board, computer_player):
    # No mills or blocks possible; computer should choose any valid position
    move = computer_player.decide_placement(board)
    assert move in board.get_valid_positions(), "Computer should choose a valid position randomly."

def test_decide_move_form_mill(board, computer_player):
    # Set up board where moving a piece forms a mill
    computer_player.placed_pieces = [(0, 3), (0, 6)]
    board.grid[0][3] = 2
    board.grid[0][6] = 2
    board.grid[0][0] = None  # Target position for mill formation
    board.adjacent_positions = {
        (0, 3): [(0, 0), (0, 6)],  # Add adjacency rules
        (0, 6): [(0, 3), (0, 0)]
    }
    
    # Computer should move (0, 3) to (0, 0) to form a mill
    move = computer_player.decide_move(board)
    assert move == ((0, 3), (0, 0)), "Computer should move to form a mill."

def test_decide_move_block_mill(board, computer_player, opponent):
    # Set up board where the opponent is close to forming a mill
    opponent.placed_pieces = [(0, 0), (0, 6)]
    board.grid[0][0] = 1  # Opponent's piece
    board.grid[0][6] = 1  # Opponent's piece
    board.grid[0][3] = None  # Target position for the block

    # Computer player's pieces
    computer_player.placed_pieces = [(1, 1)]  # Computer owns this piece
    board.grid[1][1] = 2  # Computer's piece

    # Adjacency setup to allow legal moves
    board.adjacent_positions = {
        (1, 1): [(0, 3)],  # Computer can move to block
        (0, 3): [(1, 1), (0, 0), (0, 6)]
    }

    # Computer should move its piece from (1, 1) to (0, 3) to block the mill
    move = computer_player.decide_move(board)
    assert move == ((1, 1), (0, 3)), "Computer should move to block opponent's mill."

def test_decide_removal_valid_piece(board, computer_player, opponent):
    # Opponent has one piece outside a mill
    opponent.placed_pieces = [(0, 0), (0, 3)]
    board.grid[0][0] = 1
    board.grid[0][3] = 1
    piece_to_remove = computer_player.decide_removal(board, opponent)
    assert piece_to_remove == (0, 0) or piece_to_remove == (0, 3), "Computer should remove a valid piece."

def test_decide_removal_all_mills(board, computer_player, opponent):
    # Opponent's pieces are all in mills
    opponent.placed_pieces = [(0, 0), (0, 3), (0, 6)]
    board.grid[0][0] = 1
    board.grid[0][3] = 1
    board.grid[0][6] = 1
    piece_to_remove = computer_player.decide_removal(board, opponent)
    assert piece_to_remove in opponent.placed_pieces, "Computer should remove any opponent's piece when all are in mills."

def test_flying_phase(board, computer_player):
    # Simulate flying phase (3 pieces left)
    computer_player.placed_pieces = [(0, 0), (3, 3), (6, 6)]
    board.grid[0][0] = 2
    board.grid[3][3] = 2
    board.grid[6][6] = 2
    move = computer_player.decide_move(board)
    assert move is not None, "Computer should be able to fly during the flying phase."

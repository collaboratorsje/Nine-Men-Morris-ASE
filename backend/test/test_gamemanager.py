from game_logic.board import Board
from game_logic.player import Player
from game_logic.gamemanager import GameManager

def test_place_piece():
    board = Board()
    player1 = Player(1, 9)
    player2 = Player(2, 9)
    
    # Initialize game with Player 1's turn
    game_manager = GameManager(board, player1, player2, starting_player_id=1)
    
    # Player 1 places piece at (0, 0)
    assert game_manager.place_piece(0, 0) == True
    assert board.grid[0][0] == 1  # Check that the piece was placed correctly

    # Player 2's turn now
    assert game_manager.get_current_player() == 2
    
    # Player 2 places a piece at (1, 1)
    assert game_manager.place_piece(1, 1) == True
    assert board.grid[1][1] == 2  # Check that Player 2's piece was placed

def test_turn_management():
    board = Board()
    player1 = Player(1, 9)
    player2 = Player(2, 9)
    
    # Initialize game with Player 1 starting
    game_manager = GameManager(board, player1, player2, starting_player_id=1)
    
    # Initial turn should be Player 1
    assert game_manager.get_current_player() == 1

    # After Player 1 places a piece, the turn should switch to Player 2
    game_manager.place_piece(0, 0)
    assert game_manager.get_current_player() == 2

    # After Player 2 places a piece, the turn should switch back to Player 1
    game_manager.place_piece(1, 1)
    assert game_manager.get_current_player() == 1

def test_turn_indicator():
    """Ensure turn indicator is correct based on game state."""
    board = Board()
    player1 = Player(1, 9)
    player2 = Player(2, 9)
    game_manager = GameManager(board, player1, player2, starting_player_id=1)

    # Initially, it should be Player 1's turn
    assert game_manager.get_current_player() == 1
    
    # Player 1 places a piece, it should now be Player 2's turn
    game_manager.place_piece(0, 0)
    assert game_manager.get_current_player() == 2
    
    # Player 2 places a piece, it should switch back to Player 1
    game_manager.place_piece(1, 1)
    assert game_manager.get_current_player() == 1

def test_remaining_pieces():
    """Ensure the number of pieces left is correctly tracked for both players."""
    board = Board()
    player1 = Player(1, 9)
    player2 = Player(2, 9)
    game_manager = GameManager(board, player1, player2, starting_player_id=1)

    # Player 1 places a piece
    game_manager.place_piece(0, 0)
    assert player1.pieces == 8  # Player 1 should have 8 pieces left
    
    # Player 2 places a piece
    game_manager.place_piece(1, 1)
    assert player2.pieces == 8  # Player 2 should have 8 pieces left
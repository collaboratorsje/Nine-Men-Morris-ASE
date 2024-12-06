from game_logic.player import Player
from game_logic.board import Board

def test_player_initialization():
    player1 = Player(1, 9)
    player2 = Player(2, 9)
    assert player1.player_id == 1
    assert player2.player_id == 2
    assert player1.pieces == 9
    assert player2.pieces == 9

def test_place_piece():
    player1 = Player(1, 9)
    assert player1.place_piece((0, 0)) == True  # Successfully place a piece
    assert player1.pieces == 8  # Player should have one less piece

def test_remove_piece_multiple_pieces():
    board = Board(game_type="9mm")  # Include game_type
    player1 = Player(1, 9)
    player1.place_piece((0, 0))
    player1.place_piece((1, 1))
    player1.place_piece((2, 2))

    assert player1.remove_piece((1, 1)) == True  # Successfully remove the piece at (1, 1)
    assert (1, 1) not in player1.placed_pieces  # Ensure the piece is removed
    assert player1.placed_pieces == [(0, 0), (2, 2)]  # Remaining pieces should be (0,0) and (2,2)
    assert player1.pieces == 6  # Pieces count should be back to original count
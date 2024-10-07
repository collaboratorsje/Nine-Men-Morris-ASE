from game_logic.player import Player

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

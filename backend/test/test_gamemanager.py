from game_logic.board import Board
from game_logic.player import Player
from game_logic.gamemanager import GameManager

class TestGameManager:
    def test_place_piece(self):
        board = Board()
        player1 = Player(1, 9)
        player2 = Player(2, 9)
        game_manager = GameManager(board, player1, player2, starting_player_id=1)

        # Player 1 places a piece at (0, 0)
        result = game_manager.place_piece(0, 0)
        assert result['success'] == True
        assert board.grid[0][0] == 1  # Piece placed correctly
        assert game_manager.get_current_player() == 2  # Turn switched to Player 2

        # Player 2 places a piece at an invalid spot (occupied)
        result = game_manager.place_piece(0, 0)
        assert result['success'] == False
        assert result['message'] == "Invalid position or position already occupied"

        # Test placing a piece when not in placing phase
        game_manager.phase = 'moving'
        result = game_manager.place_piece(1, 1)
        assert result['success'] == False
        assert result['message'] == "Not in placing phase"

    def test_move_piece(self):
        board = Board()  # Assuming this initializes an empty board
        player1 = Player(1, 9)  # Player with 9 pieces
        player2 = Player(2, 9)  # Another player with 9 pieces
        game_manager = GameManager(board, player1, player2, starting_player_id=1)

        # Place pieces to enter the moving phase
        game_manager.place_piece(0, 0)  # Player 1 places piece at (0, 0)
        game_manager.place_piece(1, 1)  # Player 2 places piece at (1, 1)
        game_manager.place_piece(2, 2)  # Continue placing pieces as needed
        game_manager.place_piece(3, 3)

        # Now switch to the moving phase
        game_manager.phase = 'moving'

        # Attempt a valid move
        result = game_manager.move_piece(0, 0, 0, 3)  # Move piece from (0, 0) to (0, 1)

        # Check if the move was successful
        assert result['success'] is True
        assert board.grid[0][3] > 0  # Ensure the piece is now in the new position
        assert board.grid[0][0] == None  # Ensure the old position is empty

        # You may want to check if the piece count has been managed correctly


    def test_remove_piece(self):
        player = Player(player_id=1, pieces=9)  # Initialize a player with 9 pieces
        player.place_piece((1, 1))  # Place a piece at (1, 1)
        
        # Assert that the piece was placed correctly
        assert (1, 1) in player.placed_pieces  # Check that (1, 1) is in placed_pieces
        
        # Now remove the piece and check the result
        result = player.remove_piece((1, 1))
        assert result is True  # Should return True if removal is successful
        assert (1, 1) not in player.placed_pieces  # Ensure (1, 1) has been removed from placed_pieces
        
        # Try to remove a piece that doesn't exist
        result = player.remove_piece((2, 2))  # Attempt to remove a piece that was never placed
        assert result is False  # Should return False since (2, 2) was not placed


    def test_switch_turn(self):
        board = Board()
        player1 = Player(1, 9)
        player2 = Player(2, 9)
        game_manager = GameManager(board, player1, player2, starting_player_id=1)

        assert game_manager.get_current_player() == 1  # Initial turn
        game_manager.switch_turn()
        assert game_manager.get_current_player() == 2  # Turn switched
        game_manager.switch_turn()
        assert game_manager.get_current_player() == 1  # Switched back

    def test_get_board_state(self):
        board = Board()
        player1 = Player(1, 9)
        player2 = Player(2, 9)
        game_manager = GameManager(board, player1, player2, starting_player_id=1)

        # Place pieces and check state
        game_manager.place_piece(0, 0)
        state = game_manager.get_board_state()
        assert state['grid'][0][0] == 1
        assert state['player1_pieces'] == 8
        assert state['player2_pieces'] == 9

    def test_determine_phase(self):
        board = Board()
        player1 = Player(1, 9)
        player2 = Player(2, 9)
        game_manager = GameManager(board, player1, player2, starting_player_id=1)

        # Placing phase
        assert game_manager.determine_phase() == "placing"

        # Flying phase
        board = Board()
        player1 = Player(1, 0)
        player2 = Player(2, 0)
        game_manager = GameManager(board, player1, player2, starting_player_id=1)
        board.grid[0][0] = 2
        board.grid[0][3] = 2
        board.grid[0][6] = 2
        assert game_manager.determine_phase() == "flying"

        # Moving phase
        board.grid[2][2] = 2
        assert game_manager.determine_phase() == "moving"

    def test_all_pieces_in_mills(self):
        board = Board()
        player1 = Player(1, 0)
        player2 = Player(2, 0)
        game_manager = GameManager(board, player1, player2, starting_player_id=1)
        board.grid[0][0] = 2
        board.grid[0][3] = 2
        board.grid[0][6] = 2
        
        result = game_manager.all_pieces_in_mills(player2)  # Adjust as necessary
        assert result is True  # Check that the method correctly identifies the mill

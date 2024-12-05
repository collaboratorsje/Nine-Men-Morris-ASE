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
    
    def test_get_pieces_on_board(self):
        board = Board()
        player1 = Player(1, 9)
        player2 = Player(2, 9)
        game_manager = GameManager(board, player1, player2, starting_player_id=1)

        # Place some pieces for Player 1
        board.grid[0][0] = 1
        board.grid[1][1] = 1
        board.grid[2][2] = 1

        # Place some pieces for Player 2
        board.grid[3][3] = 2
        board.grid[4][4] = 2

        # Check the number of pieces on the board for each player
        player1_count = game_manager.get_pieces_on_board(1)
        player2_count = game_manager.get_pieces_on_board(2)

        # Assertions
        assert player1_count == 3, "Player 1 should have 3 pieces on the board."
        assert player2_count == 2, "Player 2 should have 2 pieces on the board."

    def test_invalid_move_does_not_change_piece_count(self):
        board = Board()
        player1 = Player(1, 9)
        player2 = Player(2, 9)
        game_manager = GameManager(board, player1, player2, starting_player_id=1)

        # Place pieces to set up the board
        game_manager.place_piece(0, 0)  # Player 1
        game_manager.place_piece(1, 1)  # Player 2
        game_manager.place_piece(2, 2)  # Player 1
        game_manager.place_piece(3, 3)  # Player 2

        # Capture the number of pieces on the board for each player
        player1_count_before = game_manager.get_pieces_on_board(1)
        player2_count_before = game_manager.get_pieces_on_board(2)

        # Attempt an invalid move by Player 1 (e.g., moving to an occupied position)
        result = game_manager.move_piece(0, 0, 1, 1)  # (1, 1) is occupied by Player 2

        # Check that the move was unsuccessful
        assert result['success'] is False, "Move should be unsuccessful"

        # Capture the number of pieces on the board after the invalid move
        player1_count_after = game_manager.get_pieces_on_board(1)
        player2_count_after = game_manager.get_pieces_on_board(2)

        # Assertions to ensure the piece count remains unchanged
        assert player1_count_before == player1_count_after, "Player 1's piece count should remain the same after an invalid move."
        assert player2_count_before == player2_count_after, "Player 2's piece count should remain the same after an invalid move."

    def test_move_to_adjacent_valid_cell(self):
        # Initialize board, players, and game manager
        board = Board()
        player1 = Player(1, 9)
        player2 = Player(2, 9)
        game_manager = GameManager(board, player1, player2, starting_player_id=1)

        # Carefully place pieces for both players, alternating turns and avoiding mill formations
        game_manager.place_piece(0, 0)  # Player 1
        game_manager.place_piece(0, 3)  # Player 2
        game_manager.place_piece(0, 6)  # Player 1
        game_manager.place_piece(1, 1)  # Player 2
        game_manager.place_piece(1, 5)  # Player 1
        game_manager.place_piece(2, 3)  # Player 2
        game_manager.place_piece(3, 2)  # Player 1
        game_manager.place_piece(3, 4)  # Player 2
        game_manager.place_piece(4, 2)  # Player 1
        game_manager.place_piece(4, 4)  # Player 2
        game_manager.place_piece(5, 1)  # Player 1
        game_manager.place_piece(5, 5)  # Player 2
        game_manager.place_piece(6, 0)  # Player 1
        game_manager.place_piece(6, 6)  # Player 2
        game_manager.place_piece(6, 3)  # Player 1
        game_manager.place_piece(3, 6)  # Player 2

        # Transition the game to the moving phase
        game_manager.phase = 'moving'

        # Ensure the game is not over before attempting the move
        game_over_status = game_manager.check_game_over()
        assert not game_over_status["game_over"], "The game should not be over before attempting the move"

        # Attempt to move Player 1's piece from (0, 0) to (3, 0), an adjacent and valid empty cell
        result = game_manager.move_piece(0, 0, 3, 0)

        # Assert that the move is successful
        assert result['success'] is True, "The move to an adjacent valid cell should be successful"
        assert board.grid[0][0] is None, "The original cell should be empty after the move"
        assert board.grid[3][0] == 1, "The piece should be in the new position"

    def test_move_to_invalid_cell(self):
        # Initialize board, players, and game manager
        board = Board()
        player1 = Player(1, 9)
        player2 = Player(2, 9)
        game_manager = GameManager(board, player1, player2, starting_player_id=1)

        # Carefully place pieces for both players, alternating turns and avoiding mill formations
        game_manager.place_piece(0, 0)  # Player 1
        game_manager.place_piece(0, 3)  # Player 2
        game_manager.place_piece(0, 6)  # Player 1
        game_manager.place_piece(1, 1)  # Player 2
        game_manager.place_piece(1, 5)  # Player 1
        game_manager.place_piece(2, 3)  # Player 2
        game_manager.place_piece(3, 2)  # Player 1
        game_manager.place_piece(3, 4)  # Player 2
        game_manager.place_piece(4, 2)  # Player 1
        game_manager.place_piece(4, 4)  # Player 2
        game_manager.place_piece(5, 1)  # Player 1
        game_manager.place_piece(5, 5)  # Player 2
        game_manager.place_piece(6, 0)  # Player 1
        game_manager.place_piece(6, 6)  # Player 2
        game_manager.place_piece(6, 3)  # Player 1
        game_manager.place_piece(3, 6)  # Player 2

        # Transition the game to the moving phase
        game_manager.phase = 'moving'

        # Attempt to move Player 1's piece from (0, 0) to (0, 3), an occupied cell
        result = game_manager.move_piece(0, 0, 0, 3)

        # Assert that the move fails
        assert result['success'] is False, "The move to an occupied cell should fail"
        assert result['message'] == "Invalid move: destination is occupied or out of bounds", "The error message should indicate an invalid move"
        assert board.grid[0][0] == 1, "The original piece should remain in the same position"
        assert board.grid[0][3] == 2, "The destination cell should still be occupied by Player 2's piece"

    def test_move_to_any_vacant_cell_flying_phase(self):
        # Initialize board, players, and game manager
        board = Board()
        player1 = Player(1, 3)  # Player 1 has only 3 pieces, entering the flying phase
        player2 = Player(2, 9)  # Player 2 still has all 9 pieces
        game_manager = GameManager(board, player1, player2, starting_player_id=1)

        # Simulate placing pieces to transition Player 1 to the flying phase
        game_manager.place_piece(0, 0)  # Player 1
        game_manager.place_piece(0, 3)  # Player 2
        game_manager.place_piece(0, 6)  # Player 1
        game_manager.place_piece(1, 1)  # Player 2
        game_manager.place_piece(3, 0)  # Player 1
        game_manager.place_piece(1, 5)  # Player 2
        game_manager.place_piece(2, 3)  # Player 2
        game_manager.place_piece(3, 4)  # Player 2

        # Transition the game to the flying phase for Player 1
        game_manager.phase = 'flying'

        # Attempt to move Player 1's piece from (0, 0) to (4, 3), a valid vacant cell
        result = game_manager.move_piece(0, 0, 4, 3)

        # Assert that the move is successful
        assert result['success'] is True, "The move to any vacant cell should be successful in the flying phase"
        assert board.grid[0][0] is None, "The original cell should be empty after the move"
        assert board.grid[4][3] == 1, "The piece should be in the new position"

    def test_move_to_occupied_cell_flying_phase(self):
        # Initialize board, players, and game manager
        board = Board()
        player1 = Player(1, 3)  # Player 1 has only 3 pieces, in the flying phase
        player2 = Player(2, 9)  # Player 2 has all 9 pieces
        game_manager = GameManager(board, player1, player2, starting_player_id=1)

        # Simulate placing pieces to transition Player 1 to the flying phase
        game_manager.place_piece(0, 0)  # Player 1
        game_manager.place_piece(0, 3)  # Player 2
        game_manager.place_piece(0, 6)  # Player 1
        game_manager.place_piece(1, 1)  # Player 2
        game_manager.place_piece(3, 0)  # Player 1
        game_manager.place_piece(1, 5)  # Player 2
        game_manager.place_piece(2, 3)  # Player 2
        game_manager.place_piece(3, 4)  # Player 2

        # Transition the game to the flying phase for Player 1
        game_manager.phase = 'flying'

        # Attempt to move Player 1's piece from (0, 0) to (0, 3), an occupied cell
        result = game_manager.move_piece(0, 0, 0, 3)

        # Assert that the move fails
        assert result['success'] is False, "The move to an occupied cell should fail in the flying phase"
        assert result['message'] == "Invalid move: destination is occupied or out of bounds", "The error message should indicate an invalid move"
        assert board.grid[0][0] == 1, "The original piece should remain in the same position"
        assert board.grid[0][3] == 2, "The destination cell should remain occupied by Player 2's piece"

    def test_determine_phase_placing(self):
        board = Board()
        player1 = Player(1, 9)
        player2 = Player(2, 9)
        game_manager = GameManager(board, player1, player2, starting_player_id=1)

        # Both players have pieces left to place, so the phase should be "placing"
        assert game_manager.determine_phase() == "placing", "Phase should be 'placing' when both players have pieces to place."

    def test_determine_phase_moving(self):
        board = Board()
        player1 = Player(1, 0)  # All pieces are placed for Player 1
        player2 = Player(2, 0)  # All pieces are placed for Player 2
        game_manager = GameManager(board, player1, player2, starting_player_id=1)

        # Place more than 3 pieces on the board for both players
        board.grid[0][0] = 1
        board.grid[0][3] = 1
        board.grid[0][6] = 1
        board.grid[3][0] = 1
        board.grid[3][4] = 1  # Player 1 now has 5 pieces

        board.grid[1][1] = 2
        board.grid[1][3] = 2
        board.grid[1][5] = 2
        board.grid[4][2] = 2
        board.grid[4][4] = 2  # Player 2 now has 5 pieces

        # Now both players have more than 3 pieces on the board, so the phase should be "moving"
        assert game_manager.determine_phase() == "moving", "Phase should be 'moving' when all pieces are placed and both players have more than 3 pieces on the board."

    def test_determine_phase_flying(self):
        board = Board()
        player1 = Player(1, 0)  # All pieces are placed for Player 1
        player2 = Player(2, 0)  # All pieces are placed for Player 2
        game_manager = GameManager(board, player1, player2, starting_player_id=1)

        # Simulate Player 1 having only 3 pieces left on the board
        board.grid[0][0] = 1
        board.grid[0][3] = 1
        board.grid[0][6] = 1

        # Player 2 still has more than 3 pieces
        board.grid[1][1] = 2
        board.grid[1][3] = 2
        board.grid[1][5] = 2
        board.grid[2][2] = 2

        # Player 1 has only 3 pieces, so the phase should be "flying"
        assert game_manager.determine_phase() == "flying", "Phase should be 'flying' when a player has only 3 pieces on the board."

    def test_all_pieces_in_mills(self):
        # Initialize board, players, and game manager
        board = Board()
        player1 = Player(1, 0)  # Player 1 has placed all pieces
        player2 = Player(2, 0)  # Player 2 has placed all pieces
        game_manager = GameManager(board, player1, player2, starting_player_id=1)

        # Simulate placing pieces to form mills for Player 1
        player1.placed_pieces = [(0, 0), (0, 3), (0, 6)]  # This forms a mill
        board.grid[0][0] = 1
        board.grid[0][3] = 1
        board.grid[0][6] = 1

        # Check if all pieces for Player 1 are in mills
        result = game_manager.all_pieces_in_mills(player1)
        assert result is True, "All Player 1's pieces should be in mills"

        # Simulate placing pieces where not all are part of a mill for Player 2
        player2.placed_pieces = [(1, 1), (1, 3), (4, 2)]  # Not all form a mill
        board.grid[1][1] = 2
        board.grid[1]

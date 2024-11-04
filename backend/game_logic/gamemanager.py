class GameManager:
    def __init__(self, board, player1, player2, starting_player_id=1):
        """Initialize the game with a board and two players."""
        self.board = board
        self.player1 = player1
        self.player2 = player2
        # Set the current player based on the starting player ID
        self.current_player = self.get_player_by_id(starting_player_id)  
        self.phase = 'placing'  # Track the current phase of the game

    def switch_turn(self):
        """Switch the current player after a successful move."""
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2

    def get_current_player(self):
        """Return the ID of the current player."""
        return self.current_player.player_id

    def get_player_by_id(self, player_id):
        """Return the player object based on player_id."""
        return self.player1 if player_id == 1 else self.player2

    def place_piece(self, x, y):
        """Handle placing a piece on the board for the current player."""
        player = self.current_player  # Use current player directly

        if self.phase != 'placing':
            return False
        
        if self.board.is_valid_position(x, y) and self.board.grid[x][y] is None:
            if player.place_piece((x, y)):  # Place the piece for the current player
                self.board.grid[x][y] = player.player_id
                if self.board.check_for_mill(x, y, player):
                    # In the real game, you would allow player to remove an opponent's piece now
                    pass

                # Transition to the moving phase if both players have placed all pieces
                if self.player1.pieces == 0 and self.player2.pieces == 0:
                    self.phase = 'moving'

                # Switch turn to the other player
                self.switch_turn()

                return True
        return False

    def select_piece(self, x, y):
        player = self.current_player

        # Ensure the selected piece belongs to the current player
        if self.board.grid[x][y] != player.player_id:
            return {"success": False, "message": "Invalid selection: Not your piece."}

        # Check if the piece has any valid adjacent moves
        if not self.board.has_adjacent_moves(x, y):
            return {"success": False, "message": "No available moves for this piece. Please select another."}

        # Mark as selected if valid
        self.selected_piece = (x, y)
        return {"success": True}

    def move_piece(self, from_x, from_y, to_x, to_y):
        """Move a piece on the board with adjacency checks for the 'Moving' phase."""
        player = self.current_player  # Use current player directly

        # Ensure the destination is empty and valid
        if not self.board.is_valid_position(to_x, to_y) or self.board.grid[to_x][to_y] is not None:
            print("Invalid move: destination is not empty or out of bounds")
            return False

        # Allow any move in the 'Flying' phase, or ensure the move is adjacent in the 'Moving' phase
        if self.phase == 'flying' or self.board.is_adjacent(from_x, from_y, to_x, to_y):
            # Move the piece
            self.board.grid[to_x][to_y] = player.player_id
            self.board.grid[from_x][from_y] = None  # Clear the old position
            print(f"Moved piece from ({from_x}, {from_y}) to ({to_x}, {to_y})")
            self.switch_turn()
            return True

        # If we get here, the move was invalid
        print(f"Move from ({from_x}, {from_y}) to ({to_x}, {to_y}) failed: not adjacent")
        return False

    def remove_piece(self, x, y):
        """Remove an opponent's piece from the board."""
        opponent = self.player1 if self.current_player == self.player2 else self.player2

        # Check if the selected piece belongs to the opponent
        if self.board.grid[x][y] != opponent.player_id:
            print("Invalid removal: You can only remove the opponent's piece.")
            return False

        # Check if the piece to be removed is not part of a mill
        # Players should not remove pieces that are part of a mill unless all opponent's pieces are in mills
        if self.board.check_for_mill(x, y, opponent) and not self.all_pieces_in_mills(opponent):
            print("Invalid removal: Cannot remove a piece that is part of a mill unless all opponent's pieces are in mills.")
            return False

        # Remove the piece from the board
        self.board.grid[x][y] = None
        opponent.remove_piece((x, y))  # Update opponent's piece count
        print(f"Removed opponent's piece at ({x}, {y})")

        # Switch turn back to the current player after removal
        self.switch_turn()

        # Use determine_phase to dynamically set the game phase
        self.phase = self.determine_phase()
        return True

    def all_pieces_in_mills(self, player):
        """Check if all of the player's pieces are in mills."""
        for x, y in player.placed_pieces:
            if not self.board.check_for_mill(x, y, player):
                return False
        return True

    def get_board_state(self):
        """Return the current state of the board along with player info."""
        return {
            'grid': self.board.grid,
            'player1_pieces': self.player1.pieces,
            'player2_pieces': self.player2.pieces,
            'current_turn': self.current_player.player_id  # Add current player info
        }

    def get_pieces_on_board(self, player_id):
        """Return the number of pieces a player has on the board."""
        count = sum(1 for row in self.board.grid for piece in row if piece == player_id)
        return count

    def determine_phase(self):
            """Determine the current phase of the game."""
            if self.player1.pieces > 0 or self.player2.pieces > 0:
                return "placing"
            elif self.get_pieces_on_board(1) == 3 or self.get_pieces_on_board(2) == 3:
                return "flying"
            else:
                return "moving"

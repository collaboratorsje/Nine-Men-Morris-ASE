class GameManager:
    def __init__(self, board, player1, player2, starting_player_id=1):
        """Initialize the game with a board and two players."""
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.get_player_by_id(starting_player_id)
        self.phase = self.determine_phase()
        self.waiting_for_removal = False

    def switch_turn(self):
            """Switch the current player after a successful move and check for game over."""
            self.current_player = self.player1 if self.current_player == self.player2 else self.player2
            # Check for game over at the start of the new player's turn
            game_over_status = self.check_game_over()
            if game_over_status["game_over"]:
                print("Game Over:", game_over_status["message"])

    def get_current_player(self):
        """Return the ID of the current player."""
        return self.current_player.player_id

    def get_player_by_id(self, player_id):
        """Return the player object based on player_id."""
        return self.player1 if player_id == 1 else self.player2

    def place_piece(self, x, y):
        """Handle placing a piece on the board for the current player."""
        if self.waiting_for_removal:
            return {"success": False, "message": "Remove an opponent's piece before placing another."}

        if self.phase != 'placing':
            return {"success": False, "message": "Not in placing phase"}

        if self.board.is_valid_position(x, y) and self.board.grid[x][y] is None:
            if self.current_player.place_piece((x, y)):
                self.board.grid[x][y] = self.current_player.player_id
                self.current_player.placed_pieces.append((x, y))  # Add piece to placed_pieces
                mill_formed = self.board.check_for_mill(x, y, self.current_player)

                if mill_formed:
                    self.waiting_for_removal = True
                    return {
                        "success": True,
                        "mill_formed": True,
                        "board": self.get_board_state(),
                        "current_player": self.get_current_player(),
                        "phase": self.phase,
                        "message": "Mill formed! Remove an opponent's piece."
                    }

                self.phase = self.determine_phase()
                self.switch_turn()

                return {
                    "success": True,
                    "mill_formed": False,
                    "board": self.get_board_state(),
                    "current_player": self.get_current_player(),
                    "phase": self.phase
                }

        return {"success": False, "message": "Invalid position or position already occupied"}

    def move_piece(self, from_x, from_y, to_x, to_y):
        """Move a piece on the board with adjacency checks for the 'Moving' phase."""
        # Check for game over before taking any action
        game_over_status = self.check_game_over()
        if game_over_status["game_over"]:
            return {
                "success": True,
                "game_over": True,
                "winner": game_over_status["winner"],
                "message": game_over_status["message"],
                "board": self.get_board_state()
            }

        if not self.board.is_valid_position(to_x, to_y) or self.board.grid[to_x][to_y] is not None:
            return {"success": False, "message": "Invalid move: destination is occupied or out of bounds"}

        # Check if the move is valid (adjacent or flying)
        if self.phase == 'flying' or self.board.is_adjacent(from_x, from_y, to_x, to_y):
            # Move the piece
            self.board.grid[to_x][to_y] = self.current_player.player_id
            self.board.grid[from_x][from_y] = None

            # Update the player's placed_pieces list
            if (from_x, from_y) in self.current_player.placed_pieces:
                self.current_player.placed_pieces.remove((from_x, from_y))
            self.current_player.placed_pieces.append((to_x, to_y))

            # Check if moving the piece forms a mill
            mill_formed = self.board.check_for_mill(to_x, to_y, self.current_player)
            if mill_formed:
                self.waiting_for_removal = True
                return {
                    "success": True,
                    "mill_formed": True,
                    "board": self.get_board_state(),
                    "current_player": self.get_current_player(),
                    "phase": self.phase,
                    "message": "Mill formed! Remove an opponent's piece."
                }

            # If no mill is formed, switch turns
            self.switch_turn()
            self.phase = self.determine_phase()

            return {
                "success": True,
                "mill_formed": False,
                "board": self.get_board_state(),
                "current_player": self.get_current_player(),
                "phase": self.phase
            }

        return {"success": False, "message": "Invalid move: move is not adjacent"}

    def remove_piece(self, x, y):
        """Remove an opponent's piece from the board."""
        # Check for game over before taking any action
        game_over_status = self.check_game_over()
        if game_over_status["game_over"]:
            return {
                "success": True,
                "game_over": True,
                "winner": game_over_status["winner"],
                "message": game_over_status["message"],
                "board": self.get_board_state()
            }

        if not self.waiting_for_removal:
            return {"success": False, "message": "No mill formed. You cannot remove a piece now."}

        opponent = self.player1 if self.current_player == self.player2 else self.player2

        if self.board.grid[x][y] != opponent.player_id:
            return {"success": False, "message": "Invalid removal: You can only remove the opponent's piece."}

        # Check if the piece to be removed is part of a mill
        if self.board.check_for_mill(x, y, opponent):
            if not self.all_pieces_in_mills(opponent):
                return {"success": False, "message": "Cannot remove a piece that is part of a mill unless all opponent's pieces are in mills."}

        # Remove the piece from the board
        self.board.grid[x][y] = None

        # Remove the piece from the opponent's placed_pieces
        if (x, y) in opponent.placed_pieces:
            opponent.placed_pieces.remove((x, y))

        opponent.remove_piece((x, y))
        self.waiting_for_removal = False
        self.phase = self.determine_phase()
        self.switch_turn()

        return {
            "success": True,
            "board": self.get_board_state(),
            "current_player": self.get_current_player(),
            "phase": self.phase,
            "message": "Piece removed successfully. It's now the next player's turn."
        }

    def get_board_state(self):
        """Return the current state of the board along with player info."""
        return {
            'grid': self.board.grid,
            'player1_pieces': self.player1.pieces,
            'player2_pieces': self.player2.pieces,
            'current_turn': self.current_player.player_id,
        }

    def get_pieces_on_board(self, player_id):
        """Return the number of pieces a player has on the board."""
        return sum(1 for row in self.board.grid for piece in row if piece == player_id)

    def determine_phase(self):
        """Determine the current phase of the game."""
        if self.player1.pieces > 0 or self.player2.pieces > 0:
            return "placing"
        elif self.get_pieces_on_board(1) == 3 or self.get_pieces_on_board(2) == 3:
            return "flying"
        else:
            return "moving"

    def all_pieces_in_mills(self, player):
        """Check if all of the player's pieces are in mills."""
        # Check all placed pieces to see if they are part of a mill
        for x, y in player.placed_pieces:
            if not self.board.check_for_mill(x, y, player):
                print(f"Piece at ({x}, {y}) is not in a mill.")
                return False
        print("All pieces are in mills.")
        return True
    
    def has_valid_moves(self, player):
        """Check if the player has any valid moves."""
        if self.phase == 'flying':
            # In the flying phase, the player can move to any unoccupied valid position
            for x in range(len(self.board.grid)):
                for y in range(len(self.board.grid[x])):
                    if self.board.is_valid_position(x, y) and self.board.grid[x][y] is None:
                        return True
        else:
            # In the moving phase, check for valid adjacent moves
            for x in range(len(self.board.grid)):
                for y in range(len(self.board.grid[x])):
                    if self.board.grid[x][y] == player.player_id:
                        # Use the Board's adjacency logic to check for valid moves
                        for nx, ny in self.board.adjacent_positions.get((x, y), []):
                            if self.board.grid[nx][ny] is None:
                                return True
        return False
    
    def check_game_over(self):
        """Check if the game is over only during the moving or flying phase."""
        if self.phase not in ['moving', 'flying']:
            return {"game_over": False}

        player1_pieces_on_board = self.get_pieces_on_board(1)
        player2_pieces_on_board = self.get_pieces_on_board(2)

        # Check if Player 1 has fewer than 3 pieces
        if player1_pieces_on_board < 3:
            print("Game Over: Player 2 wins! Player 1 has fewer than 3 pieces.")
            return {
                "game_over": True,
                "winner": "Player 2",
                "message": "Game Over! Player 1 has fewer than 3 pieces. Player 2 wins!"
            }

        # Check if Player 2 has fewer than 3 pieces
        if player2_pieces_on_board < 3:
            print("Game Over: Player 1 wins! Player 2 has fewer than 3 pieces.")
            return {
                "game_over": True,
                "winner": "Player 1",
                "message": "Game Over! Player 2 has fewer than 3 pieces. Player 1 wins!"
            }

        # Check if Player 1 has no valid moves
        if not self.has_valid_moves(self.player1):
            print("Game Over: Player 2 wins! Player 1 cannot make a valid move.")
            return {
                "game_over": True,
                "winner": "Player 2",
                "message": "Game Over! Player 1 cannot make a valid move. Player 2 wins!"
            }

        # Check if Player 2 has no valid moves
        if not self.has_valid_moves(self.player2):
            print("Game Over: Player 1 wins! Player 2 cannot make a valid move.")
            return {
                "game_over": True,
                "winner": "Player 1",
                "message": "Game Over! Player 2 cannot make a valid move. Player 1 wins!"
            }

        # If no game-over conditions are met, continue the game
        return {"game_over": False}
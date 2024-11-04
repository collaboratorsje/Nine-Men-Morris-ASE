class GameManager:
    def __init__(self, board, player1, player2, starting_player_id=1):
        """Initialize the game with a board and two players."""
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.get_player_by_id(starting_player_id)
        self.phase = 'placing'
        self.waiting_for_removal = False

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
        if self.waiting_for_removal:
            return {"success": False, "message": "Remove an opponent's piece before placing another."}

        if self.phase != 'placing':
            return {"success": False, "message": "Not in placing phase"}

        if self.board.is_valid_position(x, y) and self.board.grid[x][y] is None:
            if self.current_player.place_piece((x, y)):
                self.board.grid[x][y] = self.current_player.player_id
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
        player = self.current_player

        if not self.board.is_valid_position(to_x, to_y) or self.board.grid[to_x][to_y] is not None:
            print("Invalid move: destination is not empty or out of bounds")
            return False

        if self.phase == 'flying' or self.board.is_adjacent(from_x, from_y, to_x, to_y):
            self.board.grid[to_x][to_y] = player.player_id
            self.board.grid[from_x][from_y] = None
            print(f"Moved piece from ({from_x}, {from_y}) to ({to_x}, {to_y})")
            self.switch_turn()
            return True

        print(f"Move from ({from_x}, {from_y}) to ({to_x}, {to_y}) failed: not adjacent")
        return False

    def remove_piece(self, x, y):
        """Remove an opponent's piece from the board."""
        if not self.waiting_for_removal:
            return {"success": False, "message": "No mill formed. You cannot remove a piece now."}

        opponent = self.player1 if self.current_player == self.player2 else self.player2

        if self.board.grid[x][y] != opponent.player_id:
            return {"success": False, "message": "Invalid removal: You can only remove the opponent's piece."}

        if self.board.check_for_mill(x, y, opponent) and not self.all_pieces_in_mills(opponent):
            return {"success": False, "message": "Cannot remove a piece that is part of a mill unless all opponent's pieces are in mills."}

        self.board.grid[x][y] = None
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
            'current_turn': self.current_player.player_id
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
        for x, y in player.placed_pieces:
            if not self.board.check_for_mill(x, y, player):
                return False
        return True
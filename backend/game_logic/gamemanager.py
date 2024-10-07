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
                if self.check_for_mill(x, y, player):
                    # In the real game, you would allow player to remove an opponent's piece now
                    pass

                # Transition to the moving phase if both players have placed all pieces
                if self.player1.pieces == 0 and self.player2.pieces == 0:
                    self.phase = 'moving'

                # Switch turn to the other player
                self.switch_turn()

                return True
        return False

    def move_piece(self, from_x, from_y, to_x, to_y):
        """Handle moving a piece on the board."""
        player = self.current_player

        if self.phase != 'moving' and self.phase != 'flying':
            return False

        if self.board.grid[from_x][from_y] == player.player_id:
            # Check if the move is valid (adjacent or flying phase)
            if self.phase == 'flying' or self.is_adjacent(from_x, from_y, to_x, to_y):
                if self.board.grid[to_x][to_y] is None:
                    # Move the piece
                    self.board.grid[from_x][from_y] = None
                    self.board.grid[to_x][to_y] = player.player_id
                    if self.check_for_mill(to_x, to_y, player):
                        # In real game, you would allow player to remove an opponent's piece now
                        pass

                    # Switch turn to the other player
                    self.switch_turn()

                    return True
        return False

    def remove_piece(self, x, y):
        """Remove an opponent's piece."""
        opponent = self.player1 if self.current_player == self.player2 else self.player2

        if self.board.grid[x][y] == opponent.player_id:
            if not self.check_for_mill(x, y, opponent) or self.all_pieces_in_mills(opponent):
                self.board.grid[x][y] = None
                opponent.remove_piece((x, y))
                return True
        return False

    def check_for_mill(self, x, y, player=None):
        """Check if placing or moving a piece forms a mill (three in a row)."""
        player_id = player.player_id if player else self.current_player.player_id
        # Add logic to check if the move forms a mill (horizontal or vertical)
        row = self.board.grid[x]
        col = [self.board.grid[i][y] for i in range(self.board.size)]
        return row.count(player_id) == 3 or col.count(player_id) == 3

    def is_adjacent(self, from_x, from_y, to_x, to_y):
        """Check if two positions are adjacent on the board."""
        # Define adjacency rules (could be based on actual Nine Men's Morris graph)
        adjacent_positions = {
            (0, 0): [(0, 3), (3, 0)],
            (0, 3): [(0, 0), (0, 6), (1, 3)],
            # Add all adjacency rules for positions
            # ...
        }
        return (to_x, to_y) in adjacent_positions.get((from_x, from_y), [])

    def all_pieces_in_mills(self, player):
        """Check if all of the opponent's pieces are in mills."""
        for piece in player.placed_pieces:
            if not self.check_for_mill(piece[0], piece[1], player):
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


class GameManager:
    def __init__(self, board, player1, player2):
        """Initialize the game with a board and two players."""
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1  # Start with player 1
        self.phase = 'placing'  # Track the current phase of the game

    def switch_turn(self):
        """Switch the current player."""
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2

    def place_piece(self, x, y):
        """Handle placing a piece on the board."""
        if self.board.is_valid_position(x, y) and self.board.grid[x][y] is None:
            if self.current_player.place_piece((x, y)):
                self.board.grid[x][y] = self.current_player.player_id
                self.switch_turn()
                return True
        return False

    def move_piece(self, from_x, from_y, to_x, to_y):
        """Handle moving a piece on the board."""
        if self.board.grid[from_x][from_y] == self.current_player.player_id and self.board.grid[to_x][to_y] is None:
            self.board.grid[from_x][from_y] = None
            self.board.grid[to_x][to_y] = self.current_player.player_id
            self.switch_turn()
            return True
        return False

    def remove_piece(self, x, y):
        """Remove an opponent's piece."""
        opponent = self.player1 if self.current_player == self.player2 else self.player2
        if opponent.remove_piece((x, y)):
            self.board.grid[x][y] = None
            return True
        return False

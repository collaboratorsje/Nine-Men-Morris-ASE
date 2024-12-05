# Inside computerplayer.py
from .player import Player
import random

class ComputerPlayer(Player):
    def __init__(self, player_id, pieces):
        self.player_id = player_id
        self.pieces = pieces  # Number of pieces to place (9 or 12)
        self.placed_pieces = []  # Track where the player's pieces are placed
        self.type = "ComputerPlayer"

    def decide_placement(self, board):
        """Decide where to place a piece, randomly."""
        valid_positions = [
            (x, y) for x, y in board.valid_positions if board.grid[x][y] is None
        ]
        print(f"Valid positions for placement: {valid_positions}")
        if not valid_positions:
            print("No valid positions available for placement.")
            return None
        chosen_position = random.choice(valid_positions)
        print(f"Computer chose position {chosen_position} for placement.")
        return chosen_position

    def decide_move(self, board):
        """Decide which piece to move and where, randomly."""
        for from_x, from_y in self.placed_pieces:
            for to_x, to_y in board.adjacent_positions.get((from_x, from_y), []):
                if board.grid[to_x][to_y] is None:
                    print(f"Computer deciding move. Moving from ({from_x}, {from_y}) to ({to_x}, {to_y})")
                    return (from_x, from_y), (to_x, to_y)
        print("Computer deciding move. No valid moves found.")
        return None, None

    def decide_removal(self, board, opponent):
        """Decide which opponent's piece to remove, randomly."""
        removable_pieces = [
            pos for pos in opponent.placed_pieces
            if not board.check_for_mill(pos[0], pos[1], opponent) or self.all_opponent_pieces_in_mills(board, opponent)
        ]
        print(f"Removable pieces for the computer: {removable_pieces}")
        return random.choice(removable_pieces) if removable_pieces else None

    def all_opponent_pieces_in_mills(self, board, opponent):
        """Check if all opponent pieces are in mills."""
        for pos in opponent.placed_pieces:
            if not board.check_for_mill(pos[0], pos[1], opponent):
                return False
        return True



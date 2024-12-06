from .player import Player
import random

class ComputerPlayer(Player):
    def __init__(self, player_id, pieces):
        self.player_id = player_id
        self.pieces = pieces  # Number of pieces to place (9 or 12)
        self.placed_pieces = []  # Track where the player's pieces are placed
        self.type = "ComputerPlayer"

    def decide_placement(self, board):
        """Decide where to place a piece, prioritizing mills."""
        # Prioritize forming mills
        for x, y in board.valid_positions:
            if board.grid[x][y] is None and self.forms_mill(x, y, board):
                print(f"Computer prioritizing mill formation at {x, y}")
                return x, y

        # Block opponent's mills
        opponent_id = 1 if self.player_id == 2 else 2
        for x, y in board.valid_positions:
            if board.grid[x][y] is None and self.blocks_opponent_mill(x, y, board, opponent_id):
                print(f"Computer blocking opponent's mill at {x, y}")
                return x, y

        # Fallback to random placement
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
        """Decide which piece to move and where, prioritizing mills and flying when applicable."""
        opponent_id = 1 if self.player_id == 2 else 2

        # Flying phase: when the computer has only three pieces left
        if len(self.placed_pieces) == 3:
            print("Computer is in the flying phase.")
            # Prioritize forming mills during flying phase
            for from_x, from_y in self.placed_pieces:
                for to_x in range(board.size):
                    for to_y in range(board.size):
                        if board.is_valid_position(to_x, to_y) and board.grid[to_x][to_y] is None:
                            if self.forms_mill(to_x, to_y, board):
                                print(f"Computer flying to form mill from ({from_x}, {from_y}) to ({to_x}, {to_y})")
                                return (from_x, from_y), (to_x, to_y)

            # Try to block opponent's mills during flying phase
            for from_x, from_y in self.placed_pieces:
                for to_x in range(board.size):
                    for to_y in range(board.size):
                        if board.is_valid_position(to_x, to_y) and board.grid[to_x][to_y] is None:
                            if self.blocks_opponent_mill(to_x, to_y, board, opponent_id):
                                print(f"Computer flying to block opponent mill from ({from_x}, {from_y}) to ({to_x}, {to_y})")
                                return (from_x, from_y), (to_x, to_y)

            # Fallback to random flying move
            for from_x, from_y in self.placed_pieces:
                for to_x in range(board.size):
                    for to_y in range(board.size):
                        if board.is_valid_position(to_x, to_y) and board.grid[to_x][to_y] is None:
                            print(f"Computer flying randomly from ({from_x}, {from_y}) to ({to_x}, {to_y})")
                            return (from_x, from_y), (to_x, to_y)

        else:  # Normal moving phase
            # Prioritize forming mills in normal phase
            for from_x, from_y in self.placed_pieces:
                for to_x, to_y in board.adjacent_positions.get((from_x, from_y), []):
                    if board.grid[to_x][to_y] is None and self.forms_mill(to_x, to_y, board):
                        print(f"Computer moving to form mill from ({from_x}, {from_y}) to ({to_x}, {to_y})")
                        return (from_x, from_y), (to_x, to_y)

            # Try to block opponent's mills in normal phase
            for from_x, from_y in self.placed_pieces:
                for to_x, to_y in board.adjacent_positions.get((from_x, from_y), []):
                    if board.grid[to_x][to_y] is None and self.blocks_opponent_mill(to_x, to_y, board, opponent_id):
                        print(f"Computer moving to block opponent mill from ({from_x}, {from_y}) to ({to_x}, {to_y})")
                        return (from_x, from_y), (to_x, to_y)

            # Fallback to random move
            for from_x, from_y in self.placed_pieces:
                for to_x, to_y in board.adjacent_positions.get((from_x, from_y), []):
                    if board.grid[to_x][to_y] is None:
                        print(f"Computer moving randomly from ({from_x}, {from_y}) to ({to_x}, {to_y})")
                        return (from_x, from_y), (to_x, to_y)

        print("Computer deciding move. No valid moves found.")
        return None, None

    def decide_removal(self, board, opponent):
        """Decide which opponent's piece to remove, prioritizing pieces outside mills."""
        removable_pieces = [
            pos for pos in opponent.placed_pieces
            if not board.check_for_mill(pos[0], pos[1], opponent) or self.all_opponent_pieces_in_mills(board, opponent)
        ]
        print(f"Removable pieces for the computer: {removable_pieces}")
        if removable_pieces:
            chosen_piece = random.choice(removable_pieces)
            print(f"Computer removing opponent's piece at {chosen_piece}")
            return chosen_piece
        print("No pieces available for removal.")
        return None

    def forms_mill(self, x, y, board):
        """Check if placing or moving to (x, y) forms a mill for the computer."""
        result = board.check_for_mill(x, y, self)
        print(f"Checking if placing at ({x}, {y}) forms a mill: {result}")
        return result

    def blocks_opponent_mill(self, x, y, board, opponent_id):
        """Check if placing or moving to (x, y) blocks an opponent's mill."""
        # Temporarily place the opponent's piece at (x, y) to simulate the mill
        board.grid[x][y] = opponent_id
        blocks_mill = board.check_for_mill(x, y, Player(opponent_id, 0))  # Check as if it was the opponent's piece
        board.grid[x][y] = None  # Remove the simulated placement
        return blocks_mill

    def all_opponent_pieces_in_mills(self, board, opponent):
        """Check if all opponent pieces are in mills."""
        for pos in opponent.placed_pieces:
            if not board.check_for_mill(pos[0], pos[1], opponent):
                return False
        return True
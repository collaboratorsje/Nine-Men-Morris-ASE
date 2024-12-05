class Player:
    def __init__(self, player_id, pieces):
        """Initialize the player with a given ID and the number of pieces."""
        self.player_id = player_id
        self.pieces = pieces  # Number of pieces to place (12 or 12)
        self.placed_pieces = []  # Track where the player's pieces are placed
        self.type = "Player"  # Explicit type

    def to_dict(self):
        return {
            "player_id": self.player_id,
            "pieces": self.pieces,
            "placed_pieces": self.placed_pieces,
            "type": self.type,
        }

    def place_piece(self, position):
        """Place a piece for the player."""
        if self.pieces > 0:
            self.placed_pieces.append(position)
            self.pieces -= 1
            return True
        return False

    def remove_piece(self, position):
        """Remove a piece from the board."""
        if position in self.placed_pieces:
            self.placed_pieces.remove(position)
            return True
        return False
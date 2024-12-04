class Board:
    def __init__(self, game_type='nine_mens_morris'):
        """Initialize the board with a 7x7 grid and valid positions."""
        self.size = 7
        self.grid = [[None for _ in range(7)] for _ in range(7)]  # 7x7 grid with None values
        self.valid_positions = self.get_valid_positions()

    def get_valid_positions(self):
        """Return the valid positions for placing pieces based on Nine Men's Morris."""
        # Return a list of tuples that represent all the valid positions on the board
        return [
            (0, 0), (0, 3), (0, 6),  # Top row
            (1, 1), (1, 3), (1, 5),  # Second row
            (2, 2), (2, 3), (2, 4),  # Third row
            (3, 0), (3, 1), (3, 2), (3, 4), (3, 5), (3, 6),  # Middle row
            (4, 2), (4, 3), (4, 4),  # Fifth row
            (5, 1), (5, 3), (5, 5),  # Sixth row
            (6, 0), (6, 3), (6, 6),  # Bottom row
        ]

    def is_valid_position(self, x, y):
        """Check if the given (x, y) position is valid within the board."""
        return (x, y) in self.valid_positions

    # Define adjacent positions for the Nine Men's Morris board
    adjacent_positions = {
        (0, 0): [(0, 3), (3, 0)], (0, 3): [(0, 0), (0, 6), (1, 3)], (0, 6): [(0, 3), (3, 6)],
        (1, 1): [(1, 3), (3, 1)], (1, 3): [(1, 1), (1, 5), (0, 3), (2, 3)], (1, 5): [(1, 3), (3, 5)],
        (2, 2): [(2, 3), (3, 2)], (2, 3): [(2, 2), (2, 4), (1, 3)], (2, 4): [(2, 3), (3, 4)],
        (3, 0): [(0, 0), (3, 1), (6, 0)], (3, 1): [(3, 0), (1, 1), (3, 2), (5, 1)],
        (3, 2): [(3, 1), (2, 2), (3, 4), (4, 2)], (3, 4): [(3, 2), (2, 4), (3, 5), (4, 4)],
        (3, 5): [(3, 4), (1, 5), (3, 6), (5, 5)], (3, 6): [(0, 6), (3, 5), (6, 6)],
        (4, 2): [(3, 2), (4, 3)], (4, 3): [(4, 2), (4, 4), (5, 3)], (4, 4): [(3, 4), (4, 3)],
        (5, 1): [(3, 1), (5, 3)], (5, 3): [(5, 1), (5, 5), (4, 3), (6, 3)], (5, 5): [(3, 5), (5, 3)],
        (6, 0): [(3, 0), (6, 3)], (6, 3): [(6, 0), (6, 6), (5, 3)], (6, 6): [(3, 6), (6, 3)]
    }

    def is_adjacent(self, from_x, from_y, to_x, to_y):
        """Check if two positions are adjacent based on the Nine Men's Morris layout."""
        return (to_x, to_y) in self.adjacent_positions.get((from_x, from_y), [])
    
    mill_combinations = {
    # Top row mills
    (0, 0): [[(0, 3), (0, 6)], [(3, 0), (6, 0)]],
    (0, 3): [[(0, 0), (0, 6)], [(1, 3), (2, 3)]],
    (0, 6): [[(0, 0), (0, 3)], [(3, 6), (6, 6)]],

    # First inner row mills
    (1, 1): [[(1, 3), (1, 5)], [(3, 1), (5, 1)]],
    (1, 3): [[(0, 3), (2, 3)], [(1, 1), (1, 5)]],
    (1, 5): [[(1, 1), (1, 3)], [(3, 5), (5, 5)]],

    # Second inner row mills
    (2, 2): [[(2, 3), (2, 4)], [(3, 2), (4, 2)]],
    (2, 3): [[(0, 3), (1, 3)], [(2, 2), (2, 4)]],
    (2, 4): [[(2, 2), (2, 3)], [(3, 4), (4, 4)]],

    # Left column mills
    (3, 0): [[(0, 0), (6, 0)], [(3, 1), (3, 2)]],
    (3, 1): [[(1, 1), (5, 1)], [(3, 0), (3, 2)]],
    (3, 2): [[(2, 2), (4, 2)], [(3, 0), (3, 1)]],

    # Right column mills
    (3, 4): [[(2, 4), (4, 4)], [(3, 5), (3, 6)]],
    (3, 5): [[(1, 5), (5, 5)], [(3, 4), (3, 6)]],
    (3, 6): [[(0, 6), (6, 6)], [(3, 4), (3, 5)]],

    # Bottom row mills
    (4, 2): [[(2, 2), (3, 2)], [(4, 3), (4, 4)]],
    (4, 3): [[(4, 2), (4, 4)], [(5, 3), (6, 3)]],
    (4, 4): [[(2, 4), (3, 4)], [(4, 2), (4, 3)]],

    # Bottom inner row mills
    (5, 1): [[(3, 1), (1, 1)], [(5, 3), (5, 5)]],
    (5, 3): [[(4, 3), (6, 3)], [(5, 1), (5, 5)]],
    (5, 5): [[(3, 5), (1, 5)], [(5, 1), (5, 3)]],

    # Bottom outer row mills
    (6, 0): [[(3, 0), (0, 0)], [(6, 3), (6, 6)]],
    (6, 3): [[(5, 3), (4, 3)], [(6, 0), (6, 6)]],
    (6, 6): [[(3, 6), (0, 6)], [(6, 0), (6, 3)]]
    }

    def check_for_mill(self, x, y, player):
        """Check if placing or moving a piece forms a mill."""
        player_id = player.player_id
        for mill in self.mill_combinations.get((x, y), []):
            if all(self.grid[pos[0]][pos[1]] == player_id for pos in mill):
                return True
        return False
    
    def display(self):
        """Display the current board layout (for debugging)."""
        for row in self.grid:
            print(row)
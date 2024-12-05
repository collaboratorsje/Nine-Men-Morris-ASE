from .player import Player
from .computerplayer import ComputerPlayer
from .board import Board

class GameManager:
    def __init__(self, board, player1, player2, game_type, starting_player_id=1, opponent_type="human"):
        """Initialize the game with a board and two players."""
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.game_type = game_type
        self.current_player = self.get_player_by_id(starting_player_id)
        self.phase = self.determine_phase()
        self.waiting_for_removal = False
        self.opponent_type = opponent_type  # Store the opponent type


    def switch_turn(self):
        """Switch the current player."""
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2
        print(f"Turn switched to Player {self.current_player.player_id}")
        print(f"Current player type: {type(self.current_player)}")
        if isinstance(self.current_player, ComputerPlayer):
            print("It's the computer's turn. Delegating to handle_computer_turn.")
            self.handle_computer_turn()
        else:
            print("It's a human player's turn.")

    def get_current_player(self):
        """Return the ID of the current player."""
        return self.current_player.player_id

    def get_player_by_id(self, player_id):
        """Return the player object based on player_id."""
        return self.player1 if player_id == 1 else self.player2

    def place_piece(self, x, y):
        """Handle placing a piece on the board for the current player."""
        print(f"Attempting to place piece at ({x}, {y}) for Player {self.current_player.player_id}")
        if self.waiting_for_removal:
            print("Cannot place piece: waiting for opponent piece removal.")
            return {"success": False, "message": "Remove an opponent's piece before placing another."}

        if self.phase != 'placing':
            print("Cannot place piece: not in placing phase.")
            return {"success": False, "message": "Not in placing phase"}

        if self.board.is_valid_position(x, y) and self.board.grid[x][y] is None:
            if self.current_player.place_piece((x, y)):
                self.board.grid[x][y] = self.current_player.player_id
                self.current_player.placed_pieces.append((x, y))
                mill_formed = self.board.check_for_mill(x, y, self.current_player)

                if mill_formed:
                    self.waiting_for_removal = True
                    print(f"Mill formed at ({x}, {y}) for Player {self.current_player.player_id}")
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

        print(f"Failed to place piece at ({x}, {y}) for Player {self.current_player.player_id}")
        return {"success": False, "message": "Invalid position or position already occupied"}

    def move_piece(self, from_x, from_y, to_x, to_y):
        """Move a piece on the board."""
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

        print(f"Phase: {self.phase}. Moving piece from ({from_x}, {from_y}) to ({to_x}, {to_y})")
        print(f"Current player's placed pieces before move: {self.current_player.placed_pieces}")

        # Dynamically count the player's pieces on the board
        actual_piece_count = sum(
            1 for row in self.board.grid for cell in row if cell == self.current_player.player_id
        )
        print(f"Actual piece count for player {self.current_player.player_id}: {actual_piece_count}")

        # Check adjacency or allow flying if player has exactly 3 pieces on the board
        if actual_piece_count == 3 or self.board.is_adjacent(from_x, from_y, to_x, to_y):
            # Update the grid
            self.board.grid[to_x][to_y] = self.current_player.player_id
            self.board.grid[from_x][from_y] = None
            print(f"Updated grid after move: {self.board.grid}")

            # Ensure proper removal of `from_x, from_y`
            if (from_x, from_y) in self.current_player.placed_pieces:
                print(f"Removing ({from_x}, {from_y}) from placed_pieces.")
                self.current_player.placed_pieces = [
                    piece for piece in self.current_player.placed_pieces if piece != (from_x, from_y)
                ]
            else:
                print(f"ERROR: ({from_x}, {from_y}) not found in placed_pieces during move!")

            # Ensure no duplicates before adding `to_x, to_y`
            if (to_x, to_y) not in self.current_player.placed_pieces:
                print(f"Adding ({to_x}, {to_y}) to placed_pieces.")
                self.current_player.placed_pieces.append((to_x, to_y))
            else:
                print(f"WARNING: ({to_x}, {to_y}) already exists in placed_pieces!")

            # Check for mill formation
            mill_formed = self.board.check_for_mill(to_x, to_y, self.current_player)
            print(f"Mill formed at ({to_x}, {to_y}): {mill_formed}")

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

            # Switch turn and determine new phase
            self.switch_turn()
            self.phase = self.determine_phase()
            print(f"Turn switched. New phase: {self.phase}")

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
        # Check if the game is already over
        game_over_status = self.check_game_over()
        if game_over_status["game_over"]:
            return {
                "success": True,
                "game_over": True,
                "winner": game_over_status["winner"],
                "message": game_over_status["message"],
                "board": self.get_board_state()
            }

        # Ensure a mill has been formed and removal is expected
        if not self.waiting_for_removal:
            return {"success": False, "message": "No mill formed. You cannot remove a piece now."}

        # Determine the opponent
        opponent = self.player1 if self.current_player == self.player2 else self.player2

        # Ensure the position belongs to the opponent
        if self.board.grid[x][y] != opponent.player_id:
            return {"success": False, "message": "Invalid removal: You can only remove the opponent's piece."}

        # Check if the piece is part of a mill
        if self.board.check_for_mill(x, y, opponent):
            # Validate if all opponent's pieces are in mills
            if not self.all_pieces_in_mills(opponent):
                return {"success": False, "message": "Cannot remove a piece that is part of a mill unless all opponent's pieces are in mills."}

        # Perform the removal
        self.board.grid[x][y] = None
        if (x, y) in opponent.placed_pieces:
            opponent.placed_pieces.remove((x, y))

        opponent.remove_piece((x, y))
        self.waiting_for_removal = False
        self.phase = self.determine_phase()

        # Re-check if removing this piece results in a game over
        game_over_status = self.check_game_over()
        if game_over_status["game_over"]:
            return {
                "success": True,
                "game_over": True,
                "winner": game_over_status["winner"],
                "message": game_over_status["message"],
                "board": self.get_board_state()
            }

        # Switch the turn to the next player
        self.switch_turn()

        return {
            "success": True,
            "board": self.get_board_state(),
            "current_player": self.get_current_player(),
            "phase": self.phase,
            "message": "Piece removed successfully. It's now the next player's turn."
        }

    def handle_computer_turn(self):
        """Handle the computer's turn."""
        if not isinstance(self.current_player, ComputerPlayer):
            print("ERROR: Current player is not a ComputerPlayer. handle_computer_turn should not have been called.")
            return

        print(f"Computer is taking its turn in phase: {self.phase}")

        if self.phase == "placing":
            position = self.current_player.decide_placement(self.board)
            if position:
                print(f"Computer decided to place a piece at: {position}")
                self.place_piece(*position)
            else:
                print("Computer failed to decide a valid placement.")
        elif self.phase in ["moving", "flying"]:
            from_pos, to_pos = self.current_player.decide_move(self.board)
            if from_pos and to_pos:
                print(f"Computer decided to move a piece from {from_pos} to {to_pos}")
                self.move_piece(*from_pos, *to_pos)
            else:
                print("Computer failed to decide a valid move.")

    def handle_computer_removal(self):
        """Handle the computer removing an opponent's piece."""
        opponent = self.player1 if self.current_player == self.player2 else self.player2
        position = self.current_player.decide_removal(self.board, opponent)
        if position:
            self.remove_piece(*position)

    @staticmethod
    def deserialize_player(data):
        player_type = data.get("type", "Player")
        if player_type == "ComputerPlayer":
            print(f"Deserializing as ComputerPlayer: {data}")
            player = ComputerPlayer(data["player_id"], data["pieces"])
        else:
            print(f"Deserializing as Player: {data}")
            player = Player(data["player_id"], data["pieces"])
        player.placed_pieces = data["placed_pieces"]
        return player


    def to_dict(self):
        return {
            "board": self.board.to_dict(),
            "player1": self.player1.to_dict(),
            "player2": self.player2.to_dict(),
            "current_player_id": self.get_current_player(),
            "phase": self.phase,
            "opponent_type": self.opponent_type,
        }

    @classmethod
    def from_dict(cls, data):
        board = Board.from_dict(data["board"])
        player1 = cls.deserialize_player(data["player1"])
        player2 = cls.deserialize_player(data["player2"])
        print(f"Restoring GameManager: Player 1 type: {type(player1)}, Player 2 type: {type(player2)}")
        game_manager = cls(
            board, player1, player2, data["board"]["game_type"], starting_player_id=data.get("current_player_id")
        )
        game_manager.phase = data["phase"]
        game_manager.opponent_type = data.get("opponent_type", "human")
        game_manager.current_player = game_manager.get_player_by_id(data["current_player_id"])
        return game_manager


    def get_board_state(self):
        """Return the current state of the board."""
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
        # Check if the placing phase is still ongoing
        if self.player1.pieces > 0 or self.player2.pieces > 0:
            return "placing"

        # Check if any player has fewer than 3 pieces on the board
        player1_pieces_on_board = self.get_pieces_on_board(1)
        player2_pieces_on_board = self.get_pieces_on_board(2)

        if player1_pieces_on_board < 3 or player2_pieces_on_board < 3:
            return "game_over"

        # Check if either player is in the flying phase
        if player1_pieces_on_board == 3 or player2_pieces_on_board == 3:
            return "flying"

        # Otherwise, the game is in the moving phase
        return "moving"

    def all_pieces_in_mills(self, player):
        """Check if all the player's pieces are in mills."""
        print(f"Checking if all pieces for Player {player.player_id} are in mills.")
        print(f"Player {player.player_id} placed pieces: {player.placed_pieces}")
        for x, y in player.placed_pieces:
            is_mill = self.board.check_for_mill(x, y, player)
            print(f"Piece at ({x}, {y}) is in mill: {is_mill}")
            if not is_mill:
                return False
        return True

    def has_valid_moves(self, player):
        if self.phase == 'flying':
            for x in range(len(self.board.grid)):
                for y in range(len(self.board.grid[x])):
                    if self.board.is_valid_position(x, y) and self.board.grid[x][y] is None:
                        return True
        else:
            for x in range(len(self.board.grid)):
                for y in range(len(self.board.grid[x])):
                    if self.board.grid[x][y] == player.player_id:
                        for nx, ny in self.board.adjacent_positions.get((x, y), []):
                            if self.board.grid[nx][ny] is None:
                                return True
        return False

    def check_game_over(self):
        """Check if the game is over and return the status."""
        # Ensure both pieces on the board and pieces left to place are considered
        if self.get_pieces_on_board(1) < 3 and self.player1.pieces == 0:
            return {
                "game_over": True,
                "winner": "Player 2",
                "message": "Player 1 has fewer than 3 pieces and no pieces left to place. Player 2 wins!"
            }
        if self.get_pieces_on_board(2) < 3 and self.player2.pieces == 0:
            return {
                "game_over": True,
                "winner": "Player 1",
                "message": "Player 2 has fewer than 3 pieces and no pieces left to place. Player 1 wins!"
            }

        # If a player cannot make a valid move
        if not self.has_valid_moves(self.player1) and self.player1.pieces == 0:
            return {
                "game_over": True,
                "winner": "Player 2",
                "message": "Player 1 has no valid moves left. Player 2 wins!"
            }
        if not self.has_valid_moves(self.player2) and self.player2.pieces == 0:
            return {
                "game_over": True,
                "winner": "Player 1",
                "message": "Player 2 has no valid moves left. Player 1 wins!"
            }

        # Game is not over
        return {
            "game_over": False
        }




from flask import Flask, jsonify, request
from game_logic.board import Board
from game_logic.player import Player
from game_logic.gamemanager import GameManager

app = Flask(__name__)

# Initialize global game_manager
game_manager = None

@app.route('/api/setup', methods=['POST'])
def setup_game():
    """Set up the game with the initial player."""
    data = request.get_json()
    starting_player = data['firstPlayer']  # Get the starting player from the frontend

    global game_manager
    board = Board()
    player1 = Player(1, 9)  # Player 1 has 9 pieces for Nine Men's Morris
    player2 = Player(2, 9)  # Player 2 has 9 pieces
    starting_player_id = 1 if starting_player == 'player1' else 2

    # Initialize GameManager with the chosen starting player
    game_manager = GameManager(board, player1, player2, starting_player_id)
    return jsonify(success=True, board=game_manager.get_board_state(), current_player=game_manager.get_current_player())

@app.route('/api/place', methods=['POST'])
def place_piece():
    """Place a piece on the board at a given position."""
    data = request.get_json()  # Get the position data from the frontend
    x = data['x']
    y = data['y']

    # No need to pass player, GameManager handles turn internally
    print(f"Placing piece at position ({x}, {y}) by Player {game_manager.get_current_player()}")

    success = game_manager.place_piece(x, y)  # Use GameManager to place the piece
    phase = game_manager.determine_phase()  # Get the updated phase
    print("Updated Phase:", phase)  # Debug print to check the updated phase

    # Return the updated board state, current player, and game phase
    return jsonify(success=success, board=game_manager.get_board_state(), current_player=game_manager.get_current_player(), phase=phase)

@app.route('/api/move', methods=['POST'])
def move_piece():
    """Move a piece on the board from one position to another."""
    data = request.get_json()
    print("Received data:", data)  # Log incoming data

    # Check for required fields in data
    if not data or 'from_x' not in data or 'from_y' not in data or 'to_x' not in data or 'to_y' not in data:
        print("Invalid data received: missing coordinates")
        return jsonify(success=False, error="Invalid data: coordinates are missing"), 400

    from_x = data['from_x']
    from_y = data['from_y']
    to_x = data['to_x']
    to_y = data['to_y']

    # Attempt the move and capture success status
    success = game_manager.move_piece(from_x, from_y, to_x, to_y)
    phase = game_manager.determine_phase()
    print(f"Attempted move from ({from_x}, {from_y}) to ({to_x}, {to_y}) - Success: {success}")
    print("Updated Phase:", phase)

    if not success:
        # Log and return a clear error if the move was not successful
        print(f"Move failed: piece cannot move from ({from_x}, {from_y}) to ({to_x}, {to_y})")
        return jsonify(success=False, error="Invalid move: move failed due to game rules or invalid destination"), 400

    # If move successful, return the updated board, player, and phase
    return jsonify(
        success=True,
        board=game_manager.get_board_state(),
        current_player=game_manager.get_current_player(),
        phase=phase
    )

@app.route('/api/board', methods=['GET'])
def get_board():
    phase = game_manager.determine_phase()
    print("Phase:", phase)  # Debug print to check the phase
    return jsonify(
        board=game_manager.get_board_state(),
        current_player=game_manager.get_current_player(),
        phase=phase  # Include the game phase
    )


@app.route('/api/reset', methods=['POST'])
def reset_board():
    """Reset the board to its initial empty state."""
    global game_manager
    board = Board()  # Recreate the board
    player1 = Player(1, 9)  # Reset players with 9 pieces each
    player2 = Player(2, 9)
    # Reset to initial state but keep the starting player (decided during setup)
    game_manager = GameManager(board, player1, player2, game_manager.get_current_player())
    return jsonify(success=True, board=game_manager.get_board_state(), current_player=game_manager.get_current_player())

if __name__ == '__main__':
    app.run(debug=True)

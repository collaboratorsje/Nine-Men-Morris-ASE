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
    starting_player = data['firstPlayer']

    global game_manager
    board = Board()
    player1 = Player(1, 9)
    player2 = Player(2, 9)
    starting_player_id = 1 if starting_player == 'player1' else 2

    game_manager = GameManager(board, player1, player2, starting_player_id)
    return jsonify(success=True, board=game_manager.get_board_state(), current_player=game_manager.get_current_player())

@app.route('/api/place', methods=['POST'])
def place_piece():
    """Place a piece on the board at a given position."""
    data = request.get_json()
    x = data['x']
    y = data['y']

    print(f"Placing piece at position ({x}, {y}) by Player {game_manager.get_current_player()}")

    result = game_manager.place_piece(x, y)
    success = result.get("success", False)
    mill_formed = result.get("mill_formed", False)
    message = result.get("message", "")

    phase = game_manager.phase  # Use the updated phase from GameManager
    print("Updated Phase:", phase)

    return jsonify(
        success=success,
        mill_formed=mill_formed,
        message=message,
        board=game_manager.get_board_state(),
        current_player=game_manager.get_current_player(),
        phase=phase
    )

@app.route('/api/move', methods=['POST'])
def move_piece():
    """Move a piece on the board from one position to another."""
    data = request.get_json()
    print("Received data:", data)

    if not data or 'from_x' not in data or 'from_y' not in data or 'to_x' not in data or 'to_y' not in data:
        print("Invalid data received: missing coordinates")
        return jsonify(success=False, error="Invalid data: coordinates are missing"), 400

    from_x = data['from_x']
    from_y = data['from_y']
    to_x = data['to_x']
    to_y = data['to_y']

    result = game_manager.move_piece(from_x, from_y, to_x, to_y)
    success = result.get("success", False)
    mill_formed = result.get("mill_formed", False)
    message = result.get("message", "")

    phase = game_manager.phase
    print(f"Attempted move from ({from_x}, {from_y}) to ({to_x}, {to_y}) - Success: {success}")
    print("Updated Phase:", phase)

    if not success:
        return jsonify(success=False, error=message), 400

    return jsonify(
        success=success,
        mill_formed=mill_formed,
        message=message,
        board=game_manager.get_board_state(),
        current_player=game_manager.get_current_player(),
        phase=phase
    )

@app.route('/api/remove', methods=['POST'])
def remove_piece():
    """Remove an opponent's piece from the board."""
    data = request.get_json()
    x = data['x']
    y = data['y']

    result = game_manager.remove_piece(x, y)
    success = result.get("success", False)
    message = result.get("message", "")

    phase = game_manager.phase
    print(f"Attempted to remove piece at ({x}, {y}) - Success: {success}")
    print("Updated Phase:", phase)

    if not success:
        return jsonify(success=False, message=message), 400

    return jsonify(
        success=True,
        board=game_manager.get_board_state(),
        current_player=game_manager.get_current_player(),
        phase=phase,
        message=message
    )

@app.route('/api/board', methods=['GET'])
def get_board():
    phase = game_manager.phase
    print("Phase:", phase)
    return jsonify(
        board=game_manager.get_board_state(),
        current_player=game_manager.get_current_player(),
        phase=phase
    )

@app.route('/api/reset', methods=['POST'])
def reset_board():
    """Reset the board to its initial empty state."""
    global game_manager
    phase = game_manager.phase
    print("Phase in reset:", phase)
    board = Board()
    player1 = Player(1, 9)
    player2 = Player(2, 9)
    game_manager = GameManager(board, player1, player2, game_manager.get_current_player())

    return jsonify(
        success=True, 
        board=game_manager.get_board_state(), 
        current_player=game_manager.get_current_player(), 
        phase=phase)

if __name__ == '__main__':
    app.run(debug=True)


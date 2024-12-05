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
    

    game_type = data['gameType']
    board = Board(game_type)

    if not game_type:
        return jsonify(success=False, error="Missing 'game_Type' in request payload"), 410

    if game_type == '9mm':
        player1 = Player(1, 9)
        player2 = Player(2, 9)
    else:
        player1 = Player(1, 12)
        player2 = Player(2, 12)

    starting_player_id = 1 if starting_player == 'player1' else 2

    try:
        game_manager = GameManager(board, player1, player2, game_type, starting_player_id)
    except Exception as e:
        print(f"Error initializing GameManager: {e}")
        return jsonify(success=False, error="Internal server error"), 510

    return jsonify(
        success=True,
        board=game_manager.get_board_state(),
        current_player=game_manager.get_current_player(),
        phase=game_manager.phase
    )

def check_and_return_game_over():
    """Centralized check for game-over conditions."""
    game_over_status = game_manager.check_game_over()
    if game_over_status["game_over"]:
        return jsonify(
            success=True,
            game_over=True,
            message=game_over_status["message"],
            board=game_manager.get_board_state(),
            current_player=None,
            phase="game_over"
        )
    return None

@app.route('/api/place', methods=['POST'])
def place_piece():
    """Place a piece on the board at a given position."""
    data = request.get_json()
    x = data['x']
    y = data['y']

    result = game_manager.place_piece(x, y)
    success = result.get("success", False)
    mill_formed = result.get("mill_formed", False)
    message = result.get("message", "")

    # Check for game over
    game_over_response = check_and_return_game_over()
    if game_over_response:
        return game_over_response

    return jsonify(
        success=success,
        mill_formed=mill_formed,
        message=message,
        board=game_manager.get_board_state(),
        current_player=game_manager.get_current_player(),
        phase=game_manager.phase
    )

@app.route('/api/move', methods=['POST'])
def move_piece():
    """Move a piece on the board from one position to another."""
    data = request.get_json()

    # Debugging: Log the data received from the frontend
    print("Backend received move_piece payload:", data)

    if not data or 'from_x' not in data or 'from_y' not in data or 'to_x' not in data or 'to_y' not in data:
        return jsonify(success=False, error="Invalid data: coordinates are missing"), 420

    from_x = data['from_x']
    from_y = data['from_y']
    to_x = data['to_x']
    to_y = data['to_y']

    result = game_manager.move_piece(from_x, from_y, to_x, to_y)
    success = result.get("success", False)
    mill_formed = result.get("mill_formed", False)
    message = result.get("message", "")

    # Debugging: Log the result of the move operation
    print(f"Move result: {result}, Success: {success}, Mill Formed: {mill_formed}, Message: {message}")

    phase = game_manager.phase
    print(f"Game Phase after move: {phase}")

    if not success:
        return jsonify(success=False, error=message), 430

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

    # Check for game over
    game_over_response = check_and_return_game_over()
    if game_over_response:
        return game_over_response

    if not success:
        return jsonify(success=False, message=message), 440

    return jsonify(
        success=True,
        board=game_manager.get_board_state(),
        current_player=game_manager.get_current_player(),
        phase=game_manager.phase,
        message=message
    )

@app.route('/api/board', methods=['GET'])
def get_board():
    """Get the current state of the board."""
    return jsonify(
        board=game_manager.get_board_state(),
        current_player=game_manager.get_current_player(),
        phase=game_manager.phase,
        game_type=game_manager.game_type
    )

@app.route('/api/reset', methods=['POST'])
def reset_board():
    """Reset the board to its initial empty state."""

    global game_manager

    game_type = game_manager.game_type
    if game_type == '9mm':
        player1 = Player(1, 9)
        player2 = Player(2, 9)
    else:
        player1 = Player(1, 12)
        player2 = Player(2, 12)

    # player1 = Player(1, 9)
    # player2 = Player(2, 9)
        
    board = Board(game_type)

    try:
        game_manager = GameManager(board, player1, player2, game_type, starting_player_id=1)
    except Exception as e:
        print(f"Error initializing GameManager: {e}")
        return jsonify(success=False, error="Internal server error"), 520

    return jsonify(
        success=True,
        board=game_manager.get_board_state(),
        current_player=game_manager.get_current_player(),
        phase=game_manager.phase
    )

if __name__ == '__main__':
    app.run(debug=True)

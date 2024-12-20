from flask import Flask, jsonify, request
from game_logic.board import Board
from game_logic.player import Player
from game_logic.computerplayer import ComputerPlayer
from game_logic.gamemanager import GameManager
import json

app = Flask(__name__)

# Initialize global game_manager
game_manager = None

@app.route('/api/setup', methods=['POST'])
def setup_game():
    """Set up the game with the initial player."""
    data = request.get_json()

    starting_player = data['firstPlayer']
    opponent_type = data['opponentType']
    game_type = data['gameType']

    global game_manager

    board = Board(game_type)

    if game_type == '9mm':
        player1 = Player(1, 9)
        player2 = ComputerPlayer(2, 9) if opponent_type == 'computer' else Player(2, 9)
    else:
        player1 = Player(1, 12)
        player2 = ComputerPlayer(2, 12) if opponent_type == 'computer' else Player(2, 12)

    starting_player_id = 1 if starting_player == 'player1' else 2

    try:
        game_manager = GameManager(board, player1, player2, game_type, starting_player_id, opponent_type=opponent_type)
        print(f"GameManager initialized: Player 1 type: {type(player1)}, Player 2 type: {type(player2)}")
    except Exception as e:
        print(f"Error initializing GameManager: {e}")
        return jsonify(success=False, error="Internal server error"), 510

    return jsonify(
        success=True,
        board=game_manager.get_board_state(),
        current_player=game_manager.get_current_player(),
        phase=game_manager.phase,
        waiting_for_removal=game_manager.waiting_for_removal
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
    """Place a piece on the board."""
    global game_manager

    data = request.get_json()
    x = data['x']
    y = data['y']

    print(f"Received placement request for Player {game_manager.current_player.player_id} at ({x}, {y})")
    result = game_manager.place_piece(x, y)

    # Add `waiting_for_removal` to the response
    result["waiting_for_removal"] = game_manager.waiting_for_removal

    if result.get("success"):
        # Trigger computer turn if applicable
        if isinstance(game_manager.current_player, ComputerPlayer):
            print("Triggering computer turn...")
            game_manager.handle_computer_turn()

    return jsonify(result)

@app.route('/api/move', methods=['POST'])
def move_piece():
    """Move a piece on the board from one position to another."""
    data = request.get_json()

    print("Backend received move_piece payload:", data)

    if not data or 'from_x' not in data or 'from_y' not in data or 'to_x' not in data or 'to_y' not in data:
        return jsonify(success=False, error="Invalid data: coordinates are missing"), 420

    from_x = data['from_x']
    from_y = data['from_y']
    to_x = data['to_x']
    to_y = data['to_y']

    result = game_manager.move_piece(from_x, from_y, to_x, to_y)

    result["waiting_for_removal"] = game_manager.waiting_for_removal  # Include removal state

    return jsonify(result)

@app.route('/api/remove', methods=['POST'])
def remove_piece():
    """Remove an opponent's piece from the board."""
    data = request.get_json()
    x = data['x']
    y = data['y']

    result = game_manager.remove_piece(x, y)

    result["waiting_for_removal"] = game_manager.waiting_for_removal  # Include removal state

    return jsonify(result)

@app.route('/api/board', methods=['GET'])
def get_board():
    """Get the current state of the board."""
    return jsonify(
        board=game_manager.get_board_state(),
        current_player=game_manager.get_current_player(),
        phase=game_manager.phase,
        game_type=game_manager.game_type,
        waiting_for_removal=game_manager.waiting_for_removal  # Include removal state
    )

@app.route('/api/reset', methods=['POST'])
def reset_board():
    """Reset the board to its initial empty state."""
    global game_manager

    game_type = game_manager.game_type
    starting_player_id = 1

    if game_type == '9mm':
        player1 = Player(1, 9)
        player2 = ComputerPlayer(2, 9) if game_manager.opponent_type == "computer" else Player(2, 9)
    else:
        player1 = Player(1, 12)
        player2 = ComputerPlayer(2, 12) if game_manager.opponent_type == "computer" else Player(2, 12)

    board = Board(game_type)

    try:
        game_manager = GameManager(board, player1, player2, game_type, starting_player_id, opponent_type=game_manager.opponent_type)
        print(f"GameManager reset: Player 1 type: {type(player1)}, Player 2 type: {type(player2)}")
    except Exception as e:
        print(f"Error resetting GameManager: {e}")
        return jsonify(success=False, error="Internal server error"), 520

    return jsonify(
        success=True,
        board=game_manager.get_board_state(),
        current_player=game_manager.get_current_player(),
        phase=game_manager.phase,
        waiting_for_removal=game_manager.waiting_for_removal  # Include removal state
    )

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify, request
from game_logic.board import Board
from game_logic.player import Player
from game_logic.gamemanager import GameManager

app = Flask(__name__)

# Initialize the game
board = Board()
player1 = Player(1, 9)  # 9 pieces for Nine Men's Morris
player2 = Player(2, 9)
game_manager = GameManager(board, player1, player2)

@app.route('/api/place', methods=['POST'])
def place_piece():
    data = request.get_json()  # Get the position data from the frontend
    x = data['x']
    y = data['y']

    success = game_manager.place_piece(x, y)  # Use GameManager to place the piece
    return jsonify(success=success, board=game_manager.get_board_state())

@app.route('/api/board', methods=['GET'])
def get_board():
    """Get the current state of the board."""
    return jsonify(board=game_manager.get_board_state())

@app.route('/api/reset', methods=['POST'])
def reset_board():
    """Reset the board to its initial empty state."""
    global game_manager
    board = Board()  # Recreate the board
    player1 = Player(1, 9)  # Reset players with 9 pieces each
    player2 = Player(2, 9)
    game_manager = GameManager(board, player1, player2)
    return jsonify(success=True, board=game_manager.get_board_state())

if __name__ == '__main__':
    app.run(debug=True)


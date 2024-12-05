import React, { useState, useEffect } from "react";
import "./Board.css";

const Board = ({ gameOptions }) => {
  const [pieces, setPieces] = useState({
    'a1': null, 'd1': null, 'g1': null, 'b2': null, 'd2': null, 'f2': null,
    'c3': null, 'd3': null, 'e3': null, 'a4': null, 'b4': null, 'c4': null,
    'e4': null, 'f4': null, 'g4': null, 'c5': null, 'd5': null, 'e5': null,
    'b6': null, 'd6': null, 'f6': null, 'a7': null, 'd7': null, 'g7': null
  });

  const lines = [
    { type: 'horizontal', id: 'h1', start: [0, 0], end: [0, 6] },
    { type: 'horizontal', id: 'h2', start: [1, 1], end: [1, 5] },
    { type: 'horizontal', id: 'h3', start: [3, 0], end: [3, 6] },
    { type: 'horizontal', id: 'h4' },
    { type: 'horizontal', id: 'h5' },
    { type: 'horizontal', id: 'h6' },
    { type: 'horizontal', id: 'h7' },
    { type: 'horizontal', id: 'h8' },       
    { type: 'vertical', id: 'v1', start: [0, 0], end: [6, 0] },
    { type: 'vertical', id: 'v2', start: [1, 1], end: [5, 1] },
    { type: 'vertical', id: 'v3', start: [0, 0], end: [6, 0] },
    { type: 'vertical', id: 'v4', start: [1, 1], end: [5, 1] },
    { type: 'vertical', id: 'v5', start: [0, 0], end: [6, 0] },
    { type: 'vertical', id: 'v6', start: [1, 1], end: [5, 1] },
    { type: 'vertical', id: 'v7', start: [1, 1], end: [5, 1] },
    { type: 'vertical', id: 'v8', start: [1, 1], end: [5, 1] },
    { type: 'diagonal', id: 'd1', start: [0, 0], end: [6, 6] },
    { type: 'diagonal', id: 'd2', start: [0, 6], end: [6, 0] },
    { type: 'diagonal', id: 'd3', start: [6, 6], end: [3, 3] },
    { type: 'diagonal', id: 'd4', start: [0, 6], end: [4, 4] },
];

  const filteredLines = lines.filter(
    (line) => line.type !== 'diagonal' || gameOptions.gameType === '12mm'
  );

  const [player1Pieces, setPlayer1Pieces] = useState(9);
  const [player2Pieces, setPlayer2Pieces] = useState(9);
  const [currentPlayer, setCurrentPlayer] = useState(null);
  const [phase, setPhase] = useState("placing");
  const [selectedPiece, setSelectedPiece] = useState(null);
  const [millFormed, setMillFormed] = useState(false);
  const [notification, setNotification] = useState(null); // New state for notifications
  const [gameOver, setGameOver] = useState(false);
  const [gameOverMessage, setGameOverMessage] = useState("");
  const [gameRecord, setGameRecord] = useState({ moves: [] }); // Initialize the game record

  useEffect(() => {
    fetch('/api/board')
      .then(res => res.json())
      .then(data => {
        updateBoardState(data);
      })
      .catch(error => console.error("Error fetching board state:", error));
  }, []);

  const placePiece = (position) => {
    const [x, y] = mapPositionToCoordinates(position);
    fetch('/api/place', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ x, y })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            updateBoardState(data);
            console.log("Current Player Before Recording:", currentPlayer);
            // Record the move
            setGameRecord((prevRecord) => {
                const updatedRecord = {
                    moves: [...prevRecord.moves, { action: 'place', position, player: currentPlayer }]
                };
                console.log("Updated Game Record:", updatedRecord); // Debugging log
                return updatedRecord;
            });

            if (data.mill_formed) {
                setMillFormed(true);
                showNotification("Mill formed! Remove an opponent's piece.", "success");
            }
        } else {
            showNotification(data.message, "error");
        }
    })
    .catch(error => console.error("Error placing piece:", error));
  };

  const removePiece = (position) => {
    const [x, y] = mapPositionToCoordinates(position);
    fetch('/api/remove', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ x, y })
    })
    .then(res => res.json())
    .then(data => {
        console.log("Remove Piece Response:", data); // Debugging log

        if (data.success) {
            updateBoardState(data);

            // Record the remove action
            setGameRecord((prevRecord) => {
                const updatedRecord = {
                    moves: [...prevRecord.moves, { action: 'remove', position, player: currentPlayer }]
                };
                console.log("Updated Game Record (Remove):", updatedRecord); // Debugging log
                return updatedRecord;
            });

            setMillFormed(false);
        } else {
            showNotification(data.message, "error");
        }
    })
    .catch(error => console.error("Error removing piece:", error));
  };

  const movePiece = (position) => {
    if (selectedPiece) {
      const [fromX, fromY] = mapPositionToCoordinates(selectedPiece);
      const [toX, toY] = mapPositionToCoordinates(position);
  
      // Debugging statement to ensure the payload is correct
      console.log("Move piece payload:", { from_x: fromX, from_y: fromY, to_x: toX, to_y: toY });
  
      fetch('/api/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          from_x: fromX,
          from_y: fromY,
          to_x: toX,
          to_y: toY
        })
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          updateBoardState(data);
  
          // Record the move in the gameRecord
          setGameRecord((prevRecord) => ({
            moves: [
              ...prevRecord.moves,
              { action: 'move', from: selectedPiece, to: position, player: currentPlayer }
            ]
          }));
  
          if (data.mill_formed) {
            setMillFormed(true);
            showNotification("Mill formed! Remove an opponent's piece.", "success");
          }
          setSelectedPiece(null);
        } else {
          console.error("Error from backend:", data.message);
          showNotification(data.message, "error");
          setSelectedPiece(null);
        }
      })
      .catch(error => {
        console.error("Error during fetch:", error);
        showNotification("An unexpected error occurred.", "error");
      });
    } else if (pieces[position] === currentPlayer) {
      setSelectedPiece(position);
    } else {
      showNotification("You can only select your own pieces to move.", "error");
    }
  };  
  
  const handleClick = (position) => {
    if (notification?.type === "game-over") return; // Prevent interaction after game over
  
    if (millFormed) {
      if (pieces[position] && pieces[position] !== currentPlayer) {
        removePiece(position);
      } else {
        showNotification("You must select an opponent's piece to remove.", "error");
      }
    } else if (phase === "placing") {
      if (!pieces[position]) {
        placePiece(position);
      }
    } else if (phase === "moving" || phase === "flying") {
      movePiece(position);
    }
  };

  const GameOverModal = ({ message, onReset }) => (
    <div className="modal-overlay">
      <div className="modal">
        <h2>Game Over</h2>
        <p>{message}</p>
        <div className="modal-buttons">
          <button onClick={onReset}>Reset Game</button>
          <button onClick={saveGameRecord} style={{ marginLeft: "10px" }}>
            Download Record
          </button>
        </div>
      </div>
    </div>
  );  

  const updateBoardState = (data) => {
    setPieces(mapBoardStateToPositions(data.board.grid));
    setPlayer1Pieces(data.board.player1_pieces);
    setPlayer2Pieces(data.board.player2_pieces);
    setCurrentPlayer(data.current_player);
    setPhase(data.phase);
  
    if (data.phase === "game_over" || data.game_over) {
      console.log("Game over detected via phase or flag:", data.message);
      setGameOver(true);
      setGameOverMessage(data.message || "Game Over! Thanks for playing.");
    } else if (data.message) {
      showNotification(data.message, "success");
    }
  };  

  const resetBoard = () => {
    fetch('/api/reset', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          updateBoardState(data);
          setMillFormed(false);
          setGameOver(false); // Close modal
          setGameOverMessage(""); // Clear message
        }
      })
      .catch((error) => console.error("Error resetting the board:", error));
  };

  const showNotification = (message, type) => {
    setNotification({ message, type });
    if (type !== "game-over") {
      setTimeout(() => setNotification(null), 3000);
    }
  };  

  const mapPositionToCoordinates = (position) => {
    const positionMapping = {
      'a1': [0, 0], 'd1': [0, 3], 'g1': [0, 6],
      'b2': [1, 1], 'd2': [1, 3], 'f2': [1, 5],
      'c3': [2, 2], 'd3': [2, 3], 'e3': [2, 4],
      'a4': [3, 0], 'b4': [3, 1], 'c4': [3, 2], 'e4': [3, 4], 'f4': [3, 5], 'g4': [3, 6],
      'c5': [4, 2], 'd5': [4, 3], 'e5': [4, 4],
      'b6': [5, 1], 'd6': [5, 3], 'f6': [5, 5],
      'a7': [6, 0], 'd7': [6, 3], 'g7': [6, 6]
    };
    return positionMapping[position];
  };

  const mapBoardStateToPositions = (board) => {
    const newPieces = {};
    Object.keys(pieces).forEach((position) => {
      const [x, y] = mapPositionToCoordinates(position);
      newPieces[position] = board[x][y];
    });
    return newPieces;
  };

  const saveGameRecord = () => {
    const jsonString = JSON.stringify(gameRecord, null, 2); // Pretty-print JSON
    const blob = new Blob([jsonString], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "game_record.json";
    link.click();
    URL.revokeObjectURL(url); // Clean up
  };

  return (
    <div className="board-container">
      {/* Game Over Modal */}
      {gameOver && (
        <GameOverModal
          message={gameOverMessage}
          onReset={resetBoard}
        />
      )}
  
      {/* Notifications */}
      {notification && (
        <div
          className={`notification ${notification.type}`}
          style={{
            ...(notification.type === "game-over" && {
              backgroundColor: "#ff5722",
              fontSize: "24px",
              fontWeight: "bold",
              padding: "20px 40px",
            }),
          }}
        >
          {notification.message}
        </div>
      )}
  
      <div className="board-content">
        {/* Player 1 Info */}
        <div className="player-info player-info-top">
          <h3>Player 1 (White)</h3>
          <p>Remaining pieces: {player1Pieces}</p>
        </div>
  
        {/* Game Board */}
        <div className="board">
          {filteredLines.map(({ type, id }) => (
          <div key={id} className={`line ${type} ${id}`}></div>
          ))}
          {Object.keys(pieces).map((position) => {
            const isOccupied = pieces[position];
            const isOwnedByCurrentPlayer = isOccupied && pieces[position] === currentPlayer;
            const isOpponentPiece = isOccupied && pieces[position] !== currentPlayer;
            const isRemovable = millFormed && isOpponentPiece;
            const isSelectable =
              (phase === "moving" || phase === "flying") && isOwnedByCurrentPlayer && !millFormed;
  
            const cursorStyle = isRemovable
              ? "pointer"
              : isSelectable
              ? "pointer"
              : isOccupied
              ? "not-allowed"
              : "pointer";
  
            return (
              <div
                key={position}
                className={`spot ${position} ${isOccupied ? "occupied" : ""} ${
                  isSelectable ? "selectable" : ""
                } ${selectedPiece === position ? "selected" : ""}`}
                style={{ cursor: cursorStyle }}
                onClick={() => handleClick(position)}
              >
                {isOccupied && (
                  <div
                    className={`piece ${pieces[position] === 1 ? "white" : "black"}`}
                  ></div>
                )}
              </div>
            );
          })}
        </div>
  
        {/* Player 2 Info */}
        <div className="player-info player-info-bottom">
          <h3>Player 2 (Black)</h3>
          <p>Remaining pieces: {player2Pieces}</p>
        </div>
      </div>
  
      {/* Game Phase and Turn Info */}
      <div className="game-info">
        <p>Current Turn: Player {currentPlayer || "..."}</p>
        <p>Game Phase: {phase || "placing"}</p>
      </div>
  
      {/* Reset Board Button */}
      <button className="reset-button" onClick={resetBoard}>Reset Board</button>
    </div>
  );
};  
export default Board;

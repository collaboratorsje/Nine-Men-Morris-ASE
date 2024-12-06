import React, { useState, useEffect, useCallback } from "react";
import "./Board.css";

const Board = ({ gameOptions, gameRecord = null, updateGameRecord }) => {
  console.log("Board rendering, gameRecord:", gameRecord);

  const isReplayMode = !!gameRecord; // Check if replay mode is active
  // Use this flag to toggle replay-specific functionality

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
  const [currentMoveIndex, setCurrentMoveIndex] = useState(0);
  const [recordedMoves, setRecordedMoves] = useState([]); // For recording a new game

  const mapBoardStateToPositions = useCallback((board) => {
    const newPieces = {};
    Object.keys(pieces).forEach((position) => {
      const [x, y] = mapPositionToCoordinates(position);
      newPieces[position] = board[x][y];
    });
    return newPieces;
  }, [pieces]);

  const showNotification = useCallback((message, type) => {
    setNotification({ message, type });
    if (type !== "game-over") {
        setTimeout(() => setNotification(null), 3000);
    }
  }, [setNotification]);

  const [waitingForRemoval, setWaitingForRemoval] = useState(false); // Add state for removal phase

  const updateBoardState = useCallback((data) => {
      setPieces(mapBoardStateToPositions(data.board.grid));
      setPlayer1Pieces(data.board.player1_pieces);
      setPlayer2Pieces(data.board.player2_pieces);
      setCurrentPlayer(data.current_player);
      setPhase(data.phase);
      setWaitingForRemoval(data.waiting_for_removal || false); // Update removal state
  
      if (data.phase === "game_over" || data.game_over) {
          console.log("Game over detected via phase or flag:", data.message);
          setGameOver(true);
          setGameOverMessage(data.message || "Game Over! Thanks for playing.");
      } else if (data.message) {
          showNotification(data.message, "success");
      }
  }, [mapBoardStateToPositions, setPieces, setPlayer1Pieces, setPlayer2Pieces, setCurrentPlayer, setPhase, setGameOver, setGameOverMessage, showNotification]);
  
  useEffect(() => {
    if (!gameOptions) {
      console.error("No game options provided.");
      return;
    }

    // Determine the starting player based on game options
    const startingPlayer = gameOptions.firstPlayer === 'player1' ? 1 : 2;
    console.log("Setting initial currentPlayer to:", startingPlayer);
    setCurrentPlayer(startingPlayer);

    // Reset recorded moves if it's a new game
    if (!gameRecord) {
      setRecordedMoves([]);
    }

    // Check if auto-replay is enabled and a valid gameRecord is available
    if (gameOptions.autoReplay && gameRecord && Array.isArray(gameRecord)) {
      console.log("Auto replay enabled. Starting automatic replay...");

      const replayInterval = setInterval(() => {
        if (currentMoveIndex < gameRecord.length) {
          applyMove(gameRecord[currentMoveIndex]);
          setCurrentMoveIndex((prevIndex) => prevIndex + 1);
        } else {
          console.log("Replay complete.");
          clearInterval(replayInterval);
        }
      }, 1000); // Adjust delay (e.g., 1000ms) as needed for replay speed

      // Cleanup function to clear the interval if the component unmounts or replay ends
      return () => clearInterval(replayInterval);
    }
  }, [gameOptions, gameRecord, currentMoveIndex]);

  const applyMove = (move) => {
    const { action, position, from, to, player } = move;

    setPieces((prevPieces) => {
      const updatedPieces = { ...prevPieces };
      if (action === "place") {
        updatedPieces[position] = player;
      } else if (action === "move") {
        updatedPieces[from] = null;
        updatedPieces[to] = player;
      } else if (action === "remove") {
        updatedPieces[position] = null;
      }
      return updatedPieces;
    });
  };

  const playNextMove = () => {
    if (!gameRecord || !Array.isArray(gameRecord) || currentMoveIndex >= gameRecord.length) {
        console.log("No replay data available or replay complete.");
        return;
    }

    const move = gameRecord[currentMoveIndex];
    console.log("Applying replay move:", move);
    applyMove(move);
    setCurrentMoveIndex((index) => index + 1);
  };


  const placePiece = (position) => {
    const [x, y] = mapPositionToCoordinates(position);
    fetch('/api/place', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ x, y })
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          updateBoardState(data);

          // Log the recorded move
          const newMove = { action: 'place', position, player: currentPlayer };
          console.log("Recording move in placePiece:", newMove);

          setRecordedMoves((prevMoves) => [...prevMoves, newMove]);

          if (data.mill_formed) {
            setMillFormed(true);
            showNotification("Mill formed! Remove an opponent's piece.", "success");
          }
        } else {
          showNotification(data.message, "error");
        }
      })
      .catch((error) => console.error("Error placing piece:", error));
  }; 

  const removePiece = (position) => {
    const [x, y] = mapPositionToCoordinates(position);
    fetch('/api/remove', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ x, y })
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          updateBoardState(data);
  
          // Log the recorded move
          const newMove = { action: 'remove', position, player: currentPlayer };
          console.log("Recording move in removePiece:", newMove);
  
          setRecordedMoves((prevMoves) => [...prevMoves, newMove]);
          setMillFormed(false);
        } else {
          showNotification(data.message, "error");
        }
      })
      .catch((error) => console.error("Error removing piece:", error));
  };

  const movePiece = (position) => {
    if (selectedPiece) {
      const [fromX, fromY] = mapPositionToCoordinates(selectedPiece);
      const [toX, toY] = mapPositionToCoordinates(position);
  
      fetch('/api/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ from_x: fromX, from_y: fromY, to_x: toX, to_y: toY })
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            updateBoardState(data);
  
            // Log the recorded move
            const newMove = { action: 'move', from: selectedPiece, to: position, player: currentPlayer };
            console.log("Recording move in movePiece:", newMove);
  
            setRecordedMoves((prevMoves) => [...prevMoves, newMove]);
  
            if (data.mill_formed) {
              setMillFormed(true);
              showNotification("Mill formed! Remove an opponent's piece.", "success");
            }
            setSelectedPiece(null);
          } else {
            showNotification(data.message, "error");
            setSelectedPiece(null);
          }
        })
        .catch((error) => console.error("Error moving piece:", error));
    } else if (pieces[position] === currentPlayer) {
      setSelectedPiece(position);
    } else {
      showNotification("You can only select your own pieces to move.", "error");
    }
  };
  
  const handleClick = (position) => {
    if (notification?.type === "game-over") return; // Prevent interaction after game over

    if (waitingForRemoval) { // Block interactions during removal phase
        if (pieces[position] && pieces[position] !== currentPlayer) {
            removePiece(position);
        } else {
            showNotification("You must select an opponent's piece to remove.", "error");
        }
        return; // Prevent further actions until removal is resolved
    }

    if (phase === "placing") {
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
          <button
            onClick={() => {
              console.log("Reset Button Clicked");
              onReset();
            }}
          >
            Reset Game
          </button>
          <button
            onClick={() => {
              console.log("Download Record Button Clicked");
              saveRecordedGame();
            }}
            style={{ marginLeft: "10px" }}
          >
            Download Record
          </button>
        </div>
      </div>
    </div>
  );

  const resetBoard = () => {
    console.log("Resetting the board...");
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
          console.log("Board successfully reset");
        }
      })
      .catch((error) => console.error("Error resetting the board:", error));
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

  const saveRecordedGame = () => {
    console.log("Saving Recorded Game...");
    const jsonString = JSON.stringify({ moves: recordedMoves }, null, 2);
    const blob = new Blob([jsonString], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "recorded_game.json";
    link.click();
    URL.revokeObjectURL(url); // Clean up
    console.log("Game record downloaded");
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
                onClick={() => !isReplayMode && handleClick(position)} // Disable clicks in replay mode
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
      {!isReplayMode && (
        <div className="game-info">
          <p>Current Turn: Player {currentPlayer || "..."}</p>
          <p>Game Phase: {phase || "placing"}</p>
        </div>
      )}
  
      {/* Replay Controls */}
      {isReplayMode && (
        <div className="replay-controls">
          <button onClick={playNextMove} disabled={currentMoveIndex >= gameRecord.length}>
            Next Move
          </button>
        </div>
      )}
  
      {/* Reset Board Button */}
      {!isReplayMode && (
        <button className="reset-button" onClick={resetBoard}>Reset Board</button>
      )}
    </div>
  );
};  
export default Board;

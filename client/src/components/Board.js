import React, { useState, useEffect } from 'react';
import './Board.css';

const Board = ({ gameOptions }) => {
    const [pieces, setPieces] = useState({
        'a1': null, 'd1': null, 'g1': null, 'b2': null, 'd2': null, 'f2': null,
        'c3': null, 'd3': null, 'e3': null, 'a4': null, 'b4': null, 'c4': null,
        'e4': null, 'f4': null, 'g4': null, 'c5': null, 'd5': null, 'e5': null,
        'b6': null, 'd6': null, 'f6': null, 'a7': null, 'd7': null, 'g7': null
    });

    const [player1Pieces, setPlayer1Pieces] = useState(9);  // Track player 1's remaining pieces
    const [player2Pieces, setPlayer2Pieces] = useState(9);  // Track player 2's remaining pieces
    const [currentPlayer, setCurrentPlayer] = useState(gameOptions?.firstPlayer === 'player1' ? 1 : 2);

    useEffect(() => {
        // Log gameOptions for debugging to ensure it's passed correctly
        console.log("Game Options:", gameOptions);
    }, [gameOptions]);

    // Handle placing a piece on the board
    const placePiece = (position) => {
        if (!pieces[position]) {
            const [x, y] = mapPositionToCoordinates(position);

            fetch('/api/place', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ x, y, player: currentPlayer })  // Pass the current player to backend
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    const updatedPieces = mapBoardStateToPositions(data.board.grid);  // Updated board grid
                    setPieces(updatedPieces);  // Update the state with new board data
                    setPlayer1Pieces(data.board.player1_pieces);  // Update player 1's pieces
                    setPlayer2Pieces(data.board.player2_pieces);  // Update player 2's pieces
                    
                    // Switch turn if playing human vs human
                    if (gameOptions.opponentType === 'human') {
                        setCurrentPlayer(currentPlayer === 1 ? 2 : 1);
                    }
                }
            })
            .catch(error => console.error('Error placing piece:', error));
        }
    };

    const resetBoard = () => {
        fetch('/api/reset', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                setPieces(mapBoardStateToPositions(data.board.grid));  // Reset the pieces state
                setPlayer1Pieces(data.board.player1_pieces);  // Reset player 1's pieces
                setPlayer2Pieces(data.board.player2_pieces);  // Reset player 2's pieces
                setCurrentPlayer(gameOptions?.firstPlayer === 'player1' ? 1 : 2);  // Reset to starting player
            }
        })
        .catch(error => console.error('Error resetting the board:', error));
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

    return (
        <div className="board-container">
            {/* Display player 1's remaining pieces */}
            <div className="player-info">
                <h3>Player 1 (White)</h3>
                <p>Remaining pieces: {player1Pieces}</p>
            </div>

            <div className="board">
                {Object.keys(pieces).map((position) => (
                    <div 
                        key={position}
                        className={`spot ${position} ${pieces[position] ? 'occupied' : ''}`}
                        onClick={() => placePiece(position)}
                    >
                        {pieces[position] && (
                            <div className={`piece ${pieces[position] === 1 ? 'white' : 'black'}`}></div>
                        )}
                    </div>
                ))}
            </div>

            {/* Display player 2's remaining pieces */}
            <div className="player-info">
                <h3>Player 2 (Black)</h3>
                <p>Remaining pieces: {player2Pieces}</p>
            </div>

            <p>Current Turn: Player {currentPlayer}</p>
            <button onClick={resetBoard}>Reset Board</button>
        </div>
    );
};

export default Board;




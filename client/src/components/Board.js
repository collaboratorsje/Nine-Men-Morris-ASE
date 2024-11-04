import React, { useState, useEffect } from 'react';
import './Board.css';

const Board = ({ gameOptions }) => {
    const [pieces, setPieces] = useState({
        'a1': null, 'd1': null, 'g1': null, 'b2': null, 'd2': null, 'f2': null,
        'c3': null, 'd3': null, 'e3': null, 'a4': null, 'b4': null, 'c4': null,
        'e4': null, 'f4': null, 'g4': null, 'c5': null, 'd5': null, 'e5': null,
        'b6': null, 'd6': null, 'f6': null, 'a7': null, 'd7': null, 'g7': null
    });

    const [player1Pieces, setPlayer1Pieces] = useState(9);  
    const [player2Pieces, setPlayer2Pieces] = useState(9);  
    const [currentPlayer, setCurrentPlayer] = useState(null); 
    const [phase, setPhase] = useState("placing"); 
    const [selectedPiece, setSelectedPiece] = useState(null); 

    useEffect(() => {
        fetch('/api/board')
            .then(res => res.json())
            .then(data => {
                setPieces(mapBoardStateToPositions(data.board.grid));
                setPlayer1Pieces(data.board.player1_pieces);
                setPlayer2Pieces(data.board.player2_pieces);
                setCurrentPlayer(data.current_player);
                setPhase(data.phase);
            })
            .catch(error => console.error('Error fetching board state:', error));
    }, []);

    const placePiece = (position) => {
        const [x, y] = mapPositionToCoordinates(position);
        fetch('/api/place', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ x, y, player: currentPlayer })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                updateBoardState(data);
            } else {
                console.error('Failed to place piece');
            }
        })
        .catch(error => console.error('Error placing piece:', error));
    };

    const movePiece = (position) => {
        if (selectedPiece) {
            const [fromX, fromY] = mapPositionToCoordinates(selectedPiece);
            const [toX, toY] = mapPositionToCoordinates(position);
            
            fetch('/api/move', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    from_x: fromX,
                    from_y: fromY,
                    to_x: toX,
                    to_y: toY,
                    player: currentPlayer
                })
            })
            .then(res => res.json())
            .then(data => {
                console.log('Response data:', data); // Log the full response for debugging
                if (data.success) {
                    updateBoardState(data);
                    setSelectedPiece(null); // Clear selection after moving
                } else {
                    console.error('Failed to move piece:', data.error); // Log the exact error
                    alert(`Failed to move piece: ${data.error}`);
                    setSelectedPiece(null); // Clear selection to allow picking a different piece
                }
            })
            .catch(error => {
                console.error('Error moving piece:', error);
                alert('Error moving piece: An unexpected error occurred');
            });
        } else {
            // Select a piece to move if clicked on a piece belonging to the current player
            if (pieces[position] === currentPlayer) {
                setSelectedPiece(position);
            }
        }
    };
    

    const handleClick = (position) => {
        if (phase === "placing") {
            if (!pieces[position]) {
                placePiece(position);
            }
        } else if (phase === "moving") {
            movePiece(position);
        }
    };

    const updateBoardState = (data) => {
        const updatedPieces = mapBoardStateToPositions(data.board.grid);
        setPieces(updatedPieces);
        setPlayer1Pieces(data.board.player1_pieces);
        setPlayer2Pieces(data.board.player2_pieces);
        setCurrentPlayer(data.current_player);
        setPhase(data.phase);
    };

    const resetBoard = () => {
        fetch('/api/reset', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                setPieces(mapBoardStateToPositions(data.board.grid));
                setPlayer1Pieces(data.board.player1_pieces);
                setPlayer2Pieces(data.board.player2_pieces);
                setCurrentPlayer(data.current_player);
                setPhase(data.phase);
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
            <div className="player-info">
                <h3>Player 1 (White)</h3>
                <p>Remaining pieces: {player1Pieces}</p>
            </div>

            <div className="board">
                {Object.keys(pieces).map((position) => (
                    <div 
                        key={position}
                        className={`spot ${position} ${pieces[position] ? 'occupied' : ''} ${selectedPiece === position ? 'selected' : ''}`}
                        onClick={() => handleClick(position)} // Call handleClick instead
                    >
                        {pieces[position] && (
                            <div className={`piece ${pieces[position] === 1 ? 'white' : 'black'}`}></div>
                        )}
                    </div>
                ))}
            </div>

            <div className="player-info">
                <h3>Player 2 (Black)</h3>
                <p>Remaining pieces: {player2Pieces}</p>
            </div>

            <p>Current Turn: Player {currentPlayer || '...'}</p>
            <p>Game Phase: {phase || "Loading..."}</p>
            <button onClick={resetBoard}>Reset Board</button>
        </div>
    );
};

export default Board;
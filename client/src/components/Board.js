import React, { useState, useEffect } from 'react';
import './Board.css';

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
        { type: 'diagonal', id: 'd1', start: [0, 0], end: [6, 6] },
        { type: 'diagonal', id: 'd2', start: [0, 6], end: [6, 0] },
        { type: 'diagonal', id: 'd3', start: [6, 6], end: [3, 3] },
        { type: 'diagonal', id: 'd4', start: [0, 6], end: [4, 4] },
    ];
    

    const [player1Pieces, setPlayer1Pieces] = useState(9);
    const [player2Pieces, setPlayer2Pieces] = useState(9);
    const [currentPlayer, setCurrentPlayer] = useState(null);
    const [phase, setPhase] = useState("placing");
    const [selectedPiece, setSelectedPiece] = useState(null);
    const [millFormed, setMillFormed] = useState(false); // New state for mill formation
    const [notification, setNotification] = useState({ message: '', type: '' });

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
            body: JSON.stringify({ x, y })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                updateBoardState(data);

                if (data.mill_formed) {
                    setMillFormed(true);
                    setNotification({ message: data.message, type: 'success' });
                }
            } else {
                console.error('Failed to place piece:', data.message);
                setNotification({ message: data.message, type: 'error' });
            }
        })
        .catch(error => console.error('Error placing piece:', error));
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
            if (data.success) {
                updateBoardState(data);
                setMillFormed(false); // Reset millFormed after removal
            } else {
                console.error('Failed to remove piece:', data.message);
                alert(data.message);
            }
        })
        .catch(error => console.error('Error removing piece:', error));
    };

    const handleClick = (position) => {
        if (millFormed) {
            // Handle removing an opponent's piece
            if (pieces[position] && pieces[position] !== currentPlayer) {
                removePiece(position);
            } else {
                alert("You must select an opponent's piece to remove.");
            }
        } else if (phase === "placing") {
            // Handle placing a piece
            if (!pieces[position]) {
                placePiece(position);
            }
        } else if (phase === "moving" || phase === "flying") {
            // Handle moving or flying phases
            if (selectedPiece) {
                // If a piece is already selected, attempt to move it
                movePiece(position);
            } else if (pieces[position] === currentPlayer) {
                // Select the piece to move
                setSelectedPiece(position);
            } else {
                alert("You can only select your own pieces to move.");
            }
        }
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
                    to_y: toY
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    updateBoardState(data);
    
                    if (data.mill_formed) {
                        setMillFormed(true); // Set millFormed to true if a mill is formed
                        alert(data.message); // Notify the player about the mill
                    }
    
                    setSelectedPiece(null); // Clear selection after moving
                } else {
                    console.error('Failed to move piece:', data.error);
                    alert(data.error);
                    setSelectedPiece(null);
                }
            })
            .catch(error => {
                console.error('Error moving piece:', error);
                alert('An unexpected error occurred');
            });
        } else {
            if (pieces[position] === currentPlayer) {
                setSelectedPiece(position);
            }
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
            console.log("Reset states:", {
                pieces: mapBoardStateToPositions(data.board.grid),
                player1Pieces: data.board.player1_pieces,
                player2Pieces: data.board.player2_pieces,
                currentPlayer: data.current_player,
                phase: data.phase
            });            
            if (data.success) {
                // Reset pieces to an empty state
                const emptyBoard = {
                    'a1': null, 'd1': null, 'g1': null, 'b2': null, 'd2': null, 'f2': null,
                    'c3': null, 'd3': null, 'e3': null, 'a4': null, 'b4': null, 'c4': null,
                    'e4': null, 'f4': null, 'g4': null, 'c5': null, 'd5': null, 'e5': null,
                    'b6': null, 'd6': null, 'f6': null, 'a7': null, 'd7': null, 'g7': null
                };
                setPieces(mapBoardStateToPositions(data.board.grid));
                setPlayer1Pieces(data.board.player1_pieces);
                setPlayer2Pieces(data.board.player2_pieces);
                setCurrentPlayer(data.current_player);
                setPhase(data.phase);
                setMillFormed(false); // Reset millFormed
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
            {/* Notifications */}
            {notification.message && (
                <div className={`notification ${notification.type}`}>
                    {notification.message}
                </div>
            )}
            {/* Player 1 Info */}
            <div className="player-info">
                <h3>Player 1 (White)</h3>
                <p>Remaining pieces: {player1Pieces}</p>
            </div>
    
            {/* Board */}
            <div className="board">
                {lines.map(({ type, id }) => (
                    <div key={id} className={`line ${type} ${id}`}></div>
                ))}   
                {Object.keys(pieces).map((position) => {
                    const isOwnedByCurrentPlayer = pieces[position] === currentPlayer;
                    const isSelectable = 
                        phase === "moving" && 
                        selectedPiece === null && 
                        isOwnedByCurrentPlayer;
    
                    const isEmpty = !pieces[position];
                    const hoverCursor =
                        isEmpty
                            ? "pointer" // Allow hovering over empty spots
                            : isSelectable
                            ? "pointer" // Allow selecting pieces to move
                            : "not-allowed"; // Prevent interaction with non-selectable pieces
                    
                    return (

                        <div
                            key={position}
                            className={`spot ${position} ${pieces[position] ? 'occupied' : ''} ${
                                isSelectable ? 'selectable' : ''
                            } ${selectedPiece === position ? 'selected' : ''}`}
                            style={{ cursor: hoverCursor }}
                            onClick={() => handleClick(position)}
                        >
                         
                            {pieces[position] && (
                                <div
                                    className={`piece ${
                                        pieces[position] === 1 ? 'white' : 'black'
                                    }`}
                                ></div>
                            )}
                        </div>
                    );
                })}
            </div>
    
            {/* Player 2 Info */}
            <div className="player-info">
                <h3>Player 2 (Black)</h3>
                <p>Remaining pieces: {player2Pieces}</p>
            </div>
    
            {/* Current Turn and Phase */}
            <p>Current Turn: Player {currentPlayer || '...'}</p>
            <p>Game Phase: {phase || "placing"}</p>
    
            {/* Reset Button */}
            <button onClick={resetBoard}>Reset Board</button>
        </div>
    );  
    // return (
    //     <div className="board-container">
    //         <div className="player-info">
    //             <h3>Player 1 (White)</h3>
    //             <p>Remaining pieces: {player1Pieces}</p>
    //         </div>

    //         <div className="board">
    //             {/* Render Lines */}
    //             {lines.map(({ type, id }) => (
    //                 <div key={id} className={`line ${type} ${id}`}></div>
    //             ))}

    //             {/* Render Spots */}
    //             {Object.keys(pieces).map((position) => (
    //                 <div
    //                     key={position}
    //                     className={`spot ${position} ${pieces[position] ? 'occupied' : ''} ${
    //                         selectedPiece === position ? 'selected' : ''
    //                     }`}
    //                     onClick={() => handleClick(position)}
    //                 >
    //                     {pieces[position] && (
    //                         <div
    //                             className={`piece ${pieces[position] === 1 ? 'white' : 'black'}`}
    //                         ></div>
    //                     )}
    //                 </div>
    //             ))}
    //         </div>


    //         <div className="player-info">
    //             <h3>Player 2 (Black)</h3>
    //             <p>Remaining pieces: {player2Pieces}</p>
    //         </div>

    //         <p>Current Turn: Player {currentPlayer || '...'}</p>
    //         <p>Game Phase: {phase || "placing"}</p>
    //         <button onClick={resetBoard}>Reset Board</button>
    //     </div>
    // );
};

export default Board;
// src/components/Board.js
import React, { useState } from 'react';
import './Board.css';  // Include a CSS file for board styles

const Board = () => {
    // State to track the current pieces on the board
    const [pieces, setPieces] = useState({
        // Each valid position initialized as null (no piece)
        'a1': null, 'd1': null, 'g1': null,
        'b2': null, 'd2': null, 'f2': null,
        'c3': null, 'd3': null, 'e3': null,
        'a4': null, 'b4': null, 'c4': null, 'e4': null, 'f4': null, 'g4': null,
        'c5': null, 'd5': null, 'e5': null,
        'b6': null, 'd6': null, 'f6': null,
        'a7': null, 'd7': null, 'g7': null
    });

    const placePiece = (position) => {
        if (!pieces[position]) {
            const [x, y] = mapPositionToCoordinates(position);
    
            fetch('/api/place', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ x, y })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    const updatedPieces = mapBoardStateToPositions(data.board);
                    setPieces(updatedPieces);  // Update the state with new board data
                    console.log('Updated pieces:', updatedPieces);  // Check if state is updated
                }
            })
            .catch(error => console.error('Error placing piece:', error));
        }
    };   
    
    // Utility function to map positions (like 'a1') to x, y coordinates
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
            newPieces[position] = board[x][y];  // Map backend board state to pieces
        });
        return newPieces;  // Return the updated state
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
                setPieces(mapBoardStateToPositions(data.board));  // Reset the pieces state
            }
        })
        .catch(error => console.error('Error resetting the board:', error));
    };
    
    return (
        <div className="board-container">
            <div className="board">
                {Object.keys(pieces).map((position) => (
                    <div 
                        key={position}
                        className={`spot ${position} ${pieces[position] ? 'occupied' : ''}`}  // Add position class (e.g., a1, d1)
                        onClick={() => placePiece(position)}
                    >
                        {pieces[position] && (
                            <div className={`piece ${pieces[position] === 1 ? 'white' : 'black'}`}></div>
                        )}
                    </div>
                ))}
            </div>
            <button onClick={resetBoard}>Reset Board</button>  {/* Add reset button */}
        </div>
    );    

};

export default Board;

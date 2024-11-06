import React, { useState } from 'react';

const GameSetup = ({ startGame }) => {
    const [firstPlayer, setFirstPlayer] = useState('player1');
    const [opponentType, setOpponentType] = useState('human');

    const handleSubmit = (event) => {
        event.preventDefault();
        const options = { firstPlayer, opponentType };
        console.log('Submitting game setup options:', options);

        // Send setup information to the backend to initialize the game
        fetch('/api/setup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(options)
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                // Call the function passed by the parent component to start the game
                startGame(options);
            }
        })
        .catch(error => console.error('Error setting up the game:', error));
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Game Setup</h2>

            <div>
                <label>Who goes first: </label>
                <select value={firstPlayer} onChange={(e) => setFirstPlayer(e.target.value)}>
                    <option value="player1">Player 1</option>
                    <option value="player2">Player 2</option>
                </select>
            </div>

            <div>
                <label>Opponent: </label>
                <select value={opponentType} onChange={(e) => setOpponentType(e.target.value)}>
                    <option value="human">Human</option>
                    <option value="computer">Computer</option>
                </select>
            </div>

            <button type="submit">Start Game</button>
        </form>
    );
};

export default GameSetup;
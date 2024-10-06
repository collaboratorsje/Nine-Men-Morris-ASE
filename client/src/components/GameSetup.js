import React, { useState } from 'react';

const GameSetup = ({ startGame }) => {
    const [firstPlayer, setFirstPlayer] = useState('player1');
    const [opponentType, setOpponentType] = useState('human');

    const handleSubmit = (event) => {
        event.preventDefault();
        const options = { firstPlayer, opponentType };
        console.log('Submitting game setup options:', options);
        startGame(options);  // Pass options back to the parent component (Game)
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



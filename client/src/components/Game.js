import React, { useState } from 'react';
import GameSetup from './GameSetup';  // Menu to select game options
import Board from './Board';  // The game board component

const Game = () => {
    const [gameStarted, setGameStarted] = useState(false);
    const [gameOptions, setGameOptions] = useState(null);

    const startGame = (options) => {
        console.log('Starting game with options:', options);
    
        fetch('/api/reset', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(res => {
            console.log('Response:', res);
            if (!res.ok) {
                throw new Error('Network response was not ok ' + res.statusText);
            }
            return res.json();
        })
        .then(() => {
            setGameOptions(options);  // Store the game setup options
            setGameStarted(true);     // Mark the game as started
            console.log("Board reset before starting the new game");
        })
        .catch(error => console.error('Error resetting the game before starting:', error));
    };

    return (
        <div>
            {!gameStarted && (
                <GameSetup startGame={startGame} />  // Display the setup menu before the game starts
            )}

            {gameStarted && (
                <div>
                    <h2>Game Started!</h2>
                    <p>First Player: {gameOptions.firstPlayer === 'player1' ? 'Player 1' : 'Player 2'}</p>
                    <p>Opponent: {gameOptions.opponentType === 'human' ? 'Human' : 'Computer'}</p>

                    {console.log('Passing gameOptions to Board:', gameOptions)}

                    <Board gameOptions={gameOptions} />  {/* Pass game options to the board */}
                </div>
            )}
        </div>
    );
};

export default Game;


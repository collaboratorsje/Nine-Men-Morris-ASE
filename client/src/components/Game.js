import React, { useState } from 'react';
import GameSetup from './GameSetup';  // Menu to select game options
import Board from './Board.js';  // The game board component

const Game = () => {
    const [gameStarted, setGameStarted] = useState(false);
    const [gameOptions, setGameOptions] = useState(null);
    const [gameRecord, setGameRecord] = useState(null); // State to store game record for replay

    const startGame = (options) => {
        console.log('Starting game with options:', options);

        if (options.firstPlayer === 'replay' && options.gameRecord) {
            console.log('Replay mode detected. Loading replay...');
            setGameRecord(options.gameRecord); // Store the replay moves
            setGameOptions(options);
            setGameStarted(true);
        } else {
            // Reset the game for a new match
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
        }
    };

    const loadReplay = () => {
        if (!gameRecord || gameRecord.length === 0) {
            console.error('No valid game record to replay.');
            return;
        }

        console.log('Starting replay with game record:', gameRecord);

        // Pass game record to the board for replay logic
        setGameStarted(true);
    };

    return (
        <div>
            {!gameStarted && (
                <GameSetup startGame={startGame} />  // Display the setup menu before the game starts
            )}

            {gameStarted && (
                <div>
                    <h2>{gameOptions.gameType === '9mm' ? "9 Men's Morris" : "12 Men's Morris"} Game Started!</h2>
                    <p>First Player: {gameOptions.firstPlayer === 'player1' ? 'Player 1' : 'Player 2'}</p>
                    <p>
                        Opponent: 
                        {gameOptions.opponentType === 'human'
                            ? 'Human'
                            : gameOptions.opponentType === 'computer'
                            ? 'Computer'
                            : 'Replay'}
                    </p>

                    {console.log('Passing gameOptions and gameRecord to Board:', gameOptions, gameRecord)}

                    <Board
                        gameOptions={gameOptions}
                        gameRecord={gameRecord}
                        updateGameRecord={(newRecordUpdater) => {
                            setGameRecord((prevRecord) => newRecordUpdater(prevRecord));
                        }}
                    />
                </div>
            )}
        </div>
    );
};

export default Game;

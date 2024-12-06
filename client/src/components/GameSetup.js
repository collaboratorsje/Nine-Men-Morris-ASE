import React, { useState } from 'react';
import './GameSetup.css';

const GameSetup = ({ startGame }) => {
    const [firstPlayer, setFirstPlayer] = useState('player1');
    const [opponentType, setOpponentType] = useState('human');
    const [gameRecord, setGameRecord] = useState(null); // State to store the uploaded game record
    const [gameType, setGameType] = useState('9mm');
    const [autoReplay, setAutoReplay] = useState(false); // New state for auto-replay

    const handleSubmit = (event) => {
        event.preventDefault();
        const options = { firstPlayer, opponentType, gameType };
        console.log('Submitting game setup options:', options);

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
                    startGame(options);
                }
            })
            .catch(error => console.error('Error setting up the game:', error));
    };

    const handleFileUpload = (event) => {
        const file = event.target.files[0];
        if (!file) {
            alert('No file selected.');
            return;
        }
        if (file.type !== "application/json") {
            alert('Invalid file format. Please upload a valid JSON file.');
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const parsedRecord = JSON.parse(e.target.result.trim());
                console.log("Parsed Game Record:", parsedRecord);

                if (parsedRecord && Array.isArray(parsedRecord.moves)) {
                    setGameRecord(parsedRecord); // Store the entire record
                    alert('Game record uploaded successfully! Click Replay Game to start.');
                } else {
                    alert('Invalid JSON structure. Ensure it has a "moves" array.');
                }
            } catch (error) {
                console.error("Error Parsing JSON:", error.message);
                alert('Failed to parse JSON. Ensure the file format is valid.');
            }
        };
        reader.readAsText(file);
    };

    const handleReplayGame = () => {
        if (!gameRecord) {
            alert('No game record loaded. Please upload a file first.');
            return;
        }

        startGame({ 
            firstPlayer: 'replay', 
            opponentType: 'replay', 
            gameRecord: gameRecord.moves, 
            autoReplay // Pass autoReplay flag
        });
    };

    return (
            <form onSubmit={handleSubmit} aria-labelledby="game-setup-header" className="game-setup-form">
        <header className="App-header">
            <h1 id="game-setup-header" className="game-setup-title">Play Nine Men's Morris</h1>
        </header>
        <section className="game-setup-section">
            <h2 className="game-setup-section-title">Game Setup</h2>

            <div className="game-setup-item">
                <label htmlFor="first-player-select" className="game-setup-label">Who goes first: </label>
                <select
                    id="first-player-select"
                    value={firstPlayer}
                    onChange={(e) => setFirstPlayer(e.target.value)}
                    className="game-setup-select"
                >
                    <option value="player1">Player 1</option>
                    <option value="player2">Player 2</option>
                </select>
            </div>

            <div className="game-setup-item">
                <label htmlFor="opponent-type-select" className="game-setup-label">Opponent: </label>
                <select
                    id="opponent-type-select"
                    value={opponentType}
                    onChange={(e) => setOpponentType(e.target.value)}
                    className="game-setup-select"
                >
                    <option value="human">Human</option>
                    <option value="computer">Computer</option>
                </select>
            </div>

            <div className="game-setup-item">
                <label htmlFor="game-type-select" className="game-setup-label">Game Type: </label>
                <select
                    id="game-type-select"
                    value={gameType}
                    onChange={(e) => setGameType(e.target.value)}
                    className="game-setup-select"
                >
                    <option value="9mm">9 Men's Morris</option>
                    <option value="12mm">12 Men's Morris</option>
                </select>
            </div>

            <button type="submit" className="game-setup-button" aria-label="Start the game">Start Game</button>
        </section>

        <section className="game-setup-section">
            <h3 className="game-setup-subtitle">Load Game Record</h3>
            <input
                type="file"
                accept=".json"
                onChange={handleFileUpload}
                className="game-setup-input"
                aria-label="Upload a game record file in JSON format"
            />

            <div className="game-setup-item">
                <label htmlFor="auto-replay-checkbox" className="game-setup-label">
                    <input
                        id="auto-replay-checkbox"
                        type="checkbox"
                        checked={autoReplay}
                        onChange={(e) => setAutoReplay(e.target.checked)}
                        className="game-setup-checkbox"
                    />
                    Enable Auto Replay
                </label>
            </div>

            <button
                type="button"
                onClick={handleReplayGame}
                disabled={!gameRecord}
                aria-disabled={!gameRecord}
                className="game-setup-button"
            >
                Replay Game
            </button>
        </section>
    </form>

    );
};

export default GameSetup;
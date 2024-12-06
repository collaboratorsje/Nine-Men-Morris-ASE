import React, { useState } from 'react';

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

            <div>
                <label>Game Type: </label>
                <select value={gameType} onChange={(e) => setGameType(e.target.value)}>
                    <option value="9mm">9 men's morris</option>
                    <option value="12mm">12 men's morris</option>
                </select>
            </div>

            <button type="submit">Start Game</button>

            <h3>Load Game Record</h3>
            <input type="file" accept=".json" onChange={handleFileUpload} />
            <div>
                <label>
                    <input 
                        type="checkbox" 
                        checked={autoReplay} 
                        onChange={(e) => setAutoReplay(e.target.checked)} 
                    />
                    Enable Auto Replay
                </label>
            </div>
            <button type="button" onClick={handleReplayGame} disabled={!gameRecord}>
                Replay Game
            </button>
        </form>
    );
};

export default GameSetup;
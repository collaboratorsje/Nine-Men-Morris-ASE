// src/App.js
import React from 'react';
import './App.css';  // Optional: General app-wide styles
import Board from './components/Board';  // Import the Board component

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Play Nine Men's Morris</h1>
      </header>
      <main>
        <Board />  {/* Render the Board component here */}
      </main>
    </div>
  );
}

export default App;


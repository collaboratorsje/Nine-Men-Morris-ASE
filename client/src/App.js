import React from 'react';
import './App.css';  // Optional: General app-wide styles
import Game from './components/Game';  // Import the Game component

function App() {
  return (
    <div className="App">
      {/* <header className="App-header">
        <h1>Play Nine Men's Morris</h1>
      </header> */}
      <main>
        <Game />  {/* Render the Game component here */}
      </main>
    </div>
  );
}

export default App;
import { render, screen, cleanup, fireEvent } from '@testing-library/react';
import renderer from 'react-test-renderer';
import GameSetup from '../GameSetup'; // Adjust the import path as necessary

afterEach(() => {
    cleanup();
});

// Test to check if the GameSetup component renders with default values
test('renders GameSetup component with default values', () => {
    render(<GameSetup startGame={jest.fn()} />);

    // Check that the default selections are correct
    expect(screen.getByLabelText(/who goes first/i)).toHaveValue('player1'); // Assuming 'player1' is the default
    expect(screen.getByLabelText(/opponent/i)).toHaveValue('human'); // Assuming 'human' is the default
});

// Test to check that submitting the form calls the startGame function
test('submits the game setup options', () => {
    const startGameMock = jest.fn(); // Mock the startGame function
    render(<GameSetup startGame={startGameMock} />);

    // Check the default selections
    expect(screen.getByLabelText(/who goes first/i)).toHaveValue({firstPlayer});
    expect(screen.getByLabelText(/opponent/i)).toHaveValue('human');
    
    // Change selections
    fireEvent.change(screen.getByLabelText(/who goes first/i), { target: { value: 'player2' } });
    fireEvent.change(screen.getByLabelText(/opponent/i), { target: { value: 'computer' } });
    
    // Verify the updated selections
    expect(screen.getByLabelText(/who goes first/i)).toHaveValue('player2');
    expect(screen.getByLabelText(/opponent/i)).toHaveValue('computer');
    // Submit the form
    fireEvent.click(screen.getByText(/start game/i));

    // Check that startGame was called with the correct options
    expect(startGameMock).toHaveBeenCalledWith({ firstPlayer: 'player2', opponentType: 'computer' });
});

// Test for snapshot
test('matches snapshot', () => {
    const tree = renderer.create(<GameSetup startGame={jest.fn()} />).toJSON();
    expect(tree).toMatchSnapshot();
});
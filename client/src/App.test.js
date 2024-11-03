import { render, screen, fireEvent } from '@testing-library/react';
import App from './App';  // Adjust the path based on your project structure

test('renders header inside App-header with "Play Nine Men\'s Morris" text', () => {
  render(<App />);
  
  // Find the header text
  const headerElement = screen.getByText(/play nine men's morris/i);
  
  // Check if it's inside the element with the class "App-header"
  const headerContainer = headerElement.closest('.App-header');
  expect(headerContainer).toBeInTheDocument();
  
});

test('renders the App component root element', () => {
  render(<App />);
  
  // Check if the root div with the class "App" is rendered
  const appDiv = screen.getByRole('main', { hidden: true }).closest('.App');
  expect(appDiv).toBeInTheDocument();
});

test('renders header followed by main content', () => {
  render(<App />);
  
  const headerElement = screen.getByRole('banner'); // header is the banner role
  const mainElement = screen.getByRole('main');

  // Ensure header comes before main in the DOM structure
  expect(headerElement.compareDocumentPosition(mainElement) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
});

test('applies the correct CSS classes', () => {
  render(<App />);
  
  // Check if the root div has class "App"
  const appDiv = screen.getByRole('main', { hidden: true }).closest('.App');
  expect(appDiv).toHaveClass('App');
  
  // Check if header has the class "App-header"
  const headerElement = screen.getByRole('banner');
  expect(headerElement).toHaveClass('App-header');
});

import React, { useState, useEffect } from 'react';
import './App.css';
import { AgentDataProvider } from './components/AgentDataContext';
import { ListenerProvider } from './components/ListenerContext';
import NavigationBar from './components/NavigationBar';
import Home from './components/Home';
import Listener from './components/Listener';
import Payloads from './components/Payloads';
import Callbacks from './components/Callbacks';
import Documentation from './components/Documentation';
import Login from './components/Login';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  // Now includes potential section identifiers in currentPage state
  const [currentPage, setCurrentPage] = useState('Home');

  useEffect(() => {
    // Check if a JWT token exists in localStorage to determine logged in status
    const token = localStorage.getItem('token');
    setIsLoggedIn(!!token); // Sets to true if token exists, otherwise false
  }, []);

  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
    setCurrentPage('Home'); // Navigate to home upon successful login
  };

  const handleLogout = async () => {
    // Remove the JWT token from localStorage to "log out" the user
    localStorage.removeItem('token');
    setIsLoggedIn(false);
    setCurrentPage('Login'); // Redirect to login page
  };

  const renderPage = () => {
    // Split the currentPage state into page and optional section
    const [page, section] = currentPage.split('#');
    if (!isLoggedIn) {
      return <Login onLoginSuccess={handleLoginSuccess} />;
    } else {
      switch (page) {
        case 'Listener':
          return <Listener />;
        case 'Payloads':
          return <Payloads />;
        case 'Callbacks':
          return <Callbacks />;
        case 'Documentation':
          return <Documentation activeSection={section} />;
        case 'Home':
        default:
          return <Home setCurrentPage={setCurrentPage} />;
      }
    }
  };

  return (
    <AgentDataProvider>
      <ListenerProvider>
        <div className="App">
          {isLoggedIn && <NavigationBar setCurrentPage={setCurrentPage} onLogout={handleLogout} isLoggedIn={isLoggedIn} />}
          {renderPage()}
        </div>
      </ListenerProvider>
    </AgentDataProvider>
  );
}

export default App;

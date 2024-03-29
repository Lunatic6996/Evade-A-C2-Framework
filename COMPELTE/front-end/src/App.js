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
  const [currentPage, setCurrentPage] = useState('Home');

  useEffect(() => {
    // Immediately check if a JWT token exists in localStorage to assume logged in status
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
    if (isLoggedIn === null) {
      return <div>Loading...</div>; // This can be removed or adjusted as per the new logic
    } else if (!isLoggedIn) {
      return <Login onLoginSuccess={handleLoginSuccess} />;
    } else {
      switch (currentPage) {
        case 'Listener': return <Listener />;
        case 'Payloads': return <Payloads />;
        case 'Callbacks': return <Callbacks />;
        case 'Documentation': return <Documentation />;
        default: return <Home />;
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

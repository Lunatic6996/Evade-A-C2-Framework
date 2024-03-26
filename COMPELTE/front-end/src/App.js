import React, { useState, useEffect } from 'react';
import './App.css';
import { AgentDataProvider } from './components/AgentDataContext';
import { ListenerProvider } from './components/ListenerContext'; // Import the ListenerProvider
import NavigationBar from './components/NavigationBar';
import Home from './components/Home';
import Listener from './components/Listener';
import Payloads from './components/Payloads';
import Callbacks from './components/Callbacks';
import Documentation from './components/Documentation';
import Login from './components/Login';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(null); // null indicates the auth status is being checked
  const [currentPage, setCurrentPage] = useState('Home');

  useEffect(() => {
    const checkLoginStatus = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5002/api/check_login', {
          method: 'GET',
          credentials: 'include', // Include credentials to ensure cookies are sent
        });
        const data = await response.json();
        setIsLoggedIn(!!data.logged_in); // Update login state based on the response
      } catch (error) {
        console.error("Error verifying login status:", error);
        setIsLoggedIn(false); // Assume not logged in if there's an error
      }
    };

    checkLoginStatus();
  }, []);

  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
    setCurrentPage('Home'); // Navigate to home upon successful login
  };

  const handleLogout = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5002/api/logout', {
        method: 'POST',
        credentials: 'include', // Include credentials to ensure cookies are sent
      });
      if (response.ok) {
        setIsLoggedIn(false);
        setCurrentPage('Login'); // Redirect to login upon successful logout
      }
    } catch (error) {
      console.error("Error logging out:", error);
    }
  };

  const renderPage = () => {
    if (isLoggedIn === null) {
      return <div>Loading...</div>; // Show loading or a splash screen while checking login status
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
    <AgentDataProvider> {/* Wrap the application within AgentDataProvider */}
      <ListenerProvider> {/* Additionally, wrap the application or relevant parts with ListenerProvider */}
        <div className="App">
          {isLoggedIn && <NavigationBar setCurrentPage={setCurrentPage} onLogout={handleLogout} isLoggedIn={isLoggedIn} />}
          {renderPage()}
        </div>
      </ListenerProvider>
    </AgentDataProvider>
  );
}

export default App;

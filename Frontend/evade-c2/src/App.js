import React, { useState } from 'react';
import './App.css';
import NavigationBar from './components/NavigationBar';
import Home from './components/Home';
import Listener from './components/Listener';
import Payloads from './components/Payloads';
import Callbacks from './components/Callbacks';
import Documentation from './components/Documentation';
import Login from './components/Login'; // Make sure the path is correct

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentPage, setCurrentPage] = useState('Home');

  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
  };

  const renderPage = () => {
    if (!isLoggedIn) {
      return <Login onLoginSuccess={handleLoginSuccess} />;
    }
    switch (currentPage) {
      case 'Listener':
        return <Listener />;
      case 'Payloads':
        return <Payloads />;
      case 'Callbacks':
        return <Callbacks />;
      case 'Documentation':
        return <Documentation />;
      default:
        return <Home />;
    }
  };

  return (
    <div className="App">
      {isLoggedIn && <NavigationBar setCurrentPage={setCurrentPage} />}
      {renderPage()}
    </div>
  );
}

export default App;

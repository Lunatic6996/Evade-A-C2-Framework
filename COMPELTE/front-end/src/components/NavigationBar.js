import React from 'react';
import './NavigationBar.css';

const NavigationBar = ({ setCurrentPage, onLogout, isLoggedIn }) => {
  const handleNavigation = (page) => {
    setCurrentPage(page);
  };

  return (
    <nav className="navbar">
      <div className="brand" onClick={() => handleNavigation('Home')}>Evade-C2</div>
      <ul>
        {isLoggedIn && <>
          <li onClick={() => handleNavigation('Listener')}>Listener</li>
          <li onClick={() => handleNavigation('Payloads')}>Payloads</li>
          <li onClick={() => handleNavigation('Callbacks')}>Callbacks</li>
          <li onClick={() => handleNavigation('Documentation')}>Documentation</li>
          {/* Logout option */}
          <li onClick={onLogout}>Logout</li>
        </>}
        {!isLoggedIn && 
          <li onClick={() => handleNavigation('Login')}>Login</li>
        }
      </ul>
    </nav>
  );
};

export default NavigationBar;

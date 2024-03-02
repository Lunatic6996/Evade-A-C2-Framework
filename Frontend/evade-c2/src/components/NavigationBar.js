import React from 'react';
import './NavigationBar.css';

const NavigationBar = ({ setCurrentPage }) => {
  const handleNavigation = (page) => {
    setCurrentPage(page);
  };

  return (
    // Add a class name to the nav element to scope your styles
    <nav className="navbar">
      <div className="brand">Evade-C2</div>
      <ul>
        <li onClick={() => handleNavigation('Home')}>Home</li>
        <li onClick={() => handleNavigation('Listener')}>Listener</li>
        <li onClick={() => handleNavigation('Payloads')}>Payloads</li>
        <li onClick={() => handleNavigation('Callbacks')}>Callbacks</li>
        <li onClick={() => handleNavigation('Documentation')}>Documentation</li>
      </ul>
    </nav>
  );
};

export default NavigationBar;

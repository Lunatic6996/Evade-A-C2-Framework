/* NavigationBar.js */

import React from 'react';
import './NavigationBar.css';

const NavigationBar = ({ setCurrentPage }) => {
  const handleNavigation = (page) => {
    setCurrentPage(page);
  };

  return (
    <nav>
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

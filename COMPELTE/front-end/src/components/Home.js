import React from 'react';
import './Home.css';  // Assuming you have a CSS file for styling

function Home({ setCurrentPage }) {
  return( 
    <div className="home-container">
      <h1>Welcome to Evade-C2</h1>
      <p>Welcome to the starting point of mastering the Evade-C2 framework, a sophisticated tool designed for comprehensive cybersecurity operations.</p>
      
      <h2>Getting Started</h2>
      <p>Evade-C2 supports multiple communication protocols to suit different operational needs. Explore the core functionalities:</p>
      
      <ul className="home-links">
        <li onClick={() => setCurrentPage('Documentation#listener-setup')}>
          <strong>Listeners Setup:</strong> Configure your C2 to listen over TCP, HTTP, or HTTPS.
        </li>
        <li onClick={() => setCurrentPage('Documentation#creating-payload')}>
          <strong>Creating Agents/Payloads:</strong> Initiate and manage agents with varying protocols.
        </li>
        <li onClick={() => setCurrentPage('Documentation#evade')}>
          <strong>About Evade-C2:</strong> Learn more about the capabilities and features of Evade-C2.
        </li>
        <li onClick={() => setCurrentPage('Documentation#ethical-use')}>
          <strong>Ethical and Legal Use:</strong> Explore Guidelines for Ethical Use.
        </li>
        <li onClick={() => setCurrentPage('Documentation#interact')}>
          <strong>Interacting with Agents:</strong> Find out how to Interact with Agents.
        </li>
      </ul>
    </div>
  );
}

export default Home;

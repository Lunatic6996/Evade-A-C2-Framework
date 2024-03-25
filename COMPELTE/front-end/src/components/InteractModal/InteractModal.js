import React, { useState } from 'react';
import './InteractModal.css'; // Import the CSS file specifically for InteractModal

function InteractModal({ agentId, onClose }) {
  const [command, setCommand] = useState('');
  const [output, setOutput] = useState('');

  const handleCommandSubmit = async (e) => {
    e.preventDefault();
    setOutput('Processing...');

    try {
      const response = await fetch('http://127.0.0.1:5002/api/execute-command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ agentId, command }),
      });
      const data = await response.json();
      if (response.ok) {
        console.log(data.response); // Make sure to access the correct property from the response data
        setOutput(data.response); // Set the output to the response received from the backend
      } else {
        setOutput('Error: ' + (data.error || 'Failed to execute command'));
      }
    } catch (error) {
      console.error('Failed to send command', error);
      setOutput('Network error: Failed to send command');
    }

    setCommand('');
  };

  return (
    <div className="interact-modal">
      <div className="interact-modal-content">
        <span className="interact-close-button" onClick={onClose}>&times;</span>
        <h2>Interact with Agent: {agentId}</h2>
        <form onSubmit={handleCommandSubmit} className="interact-form">
          <input
            type="text"
            value={command}
            onChange={(e) => setCommand(e.target.value)}
            placeholder="Enter command"
            className="interact-command-input"
          />
          <button type="submit" className="interact-submit-button">Send Command</button>
        </form>
        <div className="interact-command-output">{output}</div>
      </div>
    </div>
  );
}

export default InteractModal;

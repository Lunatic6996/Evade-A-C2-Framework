import React, { useState } from 'react';

function Listener() {
  // State to store form field values
  const [protocol, setProtocol] = useState('TCP');
  const [localIP, setLocalIP] = useState('');
  const [port, setPort] = useState('');

  // Handle form field changes
  const handleProtocolChange = (event) => {
    setProtocol(event.target.value);
  };

  const handleLocalIPChange = (event) => {
    setLocalIP(event.target.value);
  };

  const handlePortChange = (event) => {
    setPort(event.target.value);
  };

  // Handle form submission
  const handleSubmit = async (event) => {
    event.preventDefault(); // Prevent the form from submitting in the traditional way

    // Construct the data object to send
    const listenerConfig = {
      protocol,
      localIP,
      port,
    };

    // Send the configuration to your Flask backend
    try {
      const response = await fetch('http://127.0.0.1:5002/api/configure-listener', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(listenerConfig),
      });
      const responseData = await response.json();

      if (response.ok) {
        alert(`Listener configured successfully: ${responseData.message}`);
      } else {
        alert(`Error: ${responseData.error}`);
      }
    } catch (error) {
      console.error('Failed to configure listener', error);
      alert('Failed to send listener configuration to the server.');
    }
  };

  return (
    <div>
      <p>Welcome to Listener!</p>
      <p>You can create three different types of listener here: TCP, HTTP, and HTTPS.</p>

      <form onSubmit={handleSubmit}>
        <div>
          <label>
            Protocol:
            <select name="protocol" value={protocol} onChange={handleProtocolChange}>
              <option value="TCP">TCP</option>
              <option value="HTTP">HTTP</option>
              <option value="HTTPS">HTTPS</option>
            </select>
          </label>
        </div>
        <div>
          <label>
            Local IP:
            <input type="text" name="localIP" value={localIP} onChange={handleLocalIPChange} />
          </label>
        </div>
        <div>
          <label>
            Port:
            <input type="text" name="port" value={port} onChange={handlePortChange} />
          </label>
        </div>
        <div>
          <button type="submit">Start Listener</button>
        </div>
      </form>
    </div>
  );
}

export default Listener;

import React, { useState } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { useListener } from './ListenerContext'; // Import the context

function Listener() {
  const { listenerConfig, saveListenerConfig } = useListener(); // Use the context
  const [protocol, setProtocol] = useState(listenerConfig?.protocol || 'TCP');
  const [localIP, setLocalIP] = useState(listenerConfig?.localIP || '');
  const [port, setPort] = useState(listenerConfig?.port || '');

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
    event.preventDefault();

    if (!protocol || !localIP || !port) {
      toast.error('Please fill out all fields.');
      return;
    }

    const newListenerConfig = { protocol, localIP, port };
    // Send the configuration to your Flask backend
    try {
      const response = await fetch('http://127.0.0.1:5002/api/configure-listener', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newListenerConfig),
      });
      const responseData = await response.json();

      if (response.ok) {
        toast.success(`Listener configured successfully: ${responseData.message}`);
        saveListenerConfig(newListenerConfig); // This replaces setListenerConfigured(true);
      } else {
        toast.error(`Error: ${responseData.error}`);
      }
    } catch (error) {
      console.error('Failed to configure listener', error);
      toast.error('Failed to send listener configuration to the server.');
    }
  };

  return (
    <div style={{ display: 'flex' }}>
      <div style={{ flex: 1 }}>
        <ToastContainer />
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
      {listenerConfig && ( // This checks if listenerConfig exists
        <div style={{ flex: 1 }}>
          <h2>Configured Listener Details</h2>
          <p>Protocol: {listenerConfig.protocol}</p>
          <p>Local IP: {listenerConfig.localIP}</p>
          <p>Port: {listenerConfig.port}</p>
        </div>
      )}
    </div>
  );
}

export default Listener;
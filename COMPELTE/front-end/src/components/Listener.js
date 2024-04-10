import React, { useState } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { useListener } from './ListenerContext'; // Import the context

function Listener() {
  const { listenerConfigs, saveListenerConfig } = useListener(); // Adjusted to handle multiple configs
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


  const handleStopListener = async (protocol, localIP, port) => {
    try {
      const response = await fetch(process.env.REACT_APP_REMOVE_LISTENER, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ protocol, localIP, port }),
      });
      const responseData = await response.json();
  
      if (response.ok) {
        toast.success(`Listener stopped successfully: ${responseData.message}`);
        // Optionally, update the UI or state as needed
      } else {
        toast.error(`Error stopping listener: ${responseData.error}`);
      }
    } catch (error) {
      console.error('Failed to stop listener', error);
      toast.error('Failed to send stop listener request to the server.');
    }
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
      const response = await fetch(process.env.REACT_APP_CONFIGURE_LISTENER, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newListenerConfig),
      });
      const responseData = await response.json();

      if (response.ok) {
        // Assuming "responseData.message" contains the specific message for already configured server
        if (responseData.message.includes("already configured")) {
            toast.info(`Listener already configured: ${responseData.message}`);
        } else {
            toast.success(`Listener configured successfully: ${responseData.message}`);
            saveListenerConfig(newListenerConfig); // Adapted for handling multiple configurations
        }
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
      <div style={{ minWidth: '50%' }}>
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
      <div style={{ minWidth: '50%' }}>
        <h2>Configured Listener Details</h2>
        {listenerConfigs.length > 0 ? (
          listenerConfigs.map((config, index) => (
            <div key={index}>
              <p>Protocol: {config.protocol}</p>
              <p>Local IP: {config.localIP}</p>
              <p>Port: {config.port}</p>
              <button onClick={() => handleStopListener(config.protocol, config.localIP, config.port)}>Stop Listener</button>
            </div>
          ))          
        ) : (
          <p>No listener configured yet.</p>
        )}
      </div>
    </div>
  );
}

export default Listener;

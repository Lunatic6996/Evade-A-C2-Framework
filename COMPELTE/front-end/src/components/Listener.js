import React, { useState } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { useListener } from './ListenerContext'; // Import the context
import './ListenerStyles.css';

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

  const isValidIP = (ip) => {
    const ipRegex = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
    return ipRegex.test(ip);
  };

  const isValidPort = (port) => {
    const portRegex = /^(6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[1-9][0-9]{1,3}|0)$/;
    return portRegex.test(port);
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

    if (!isValidIP(localIP)) {
      toast.error('Invalid IP address format.');
      return;
    }

    if (!isValidPort(port)) {
      toast.error('Invalid port number.');
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
    <div className="listener-container">
        <div className="section">
            <ToastContainer />
            <p>Welcome to Listener!</p>
            <p>You can create three different types of listener here: TCP, HTTP, and HTTPS.</p>

            <form onSubmit={handleSubmit} className="form">
                <div className="label-group">
                    <label>
                        Protocol:
                        <select name="protocol" value={protocol} onChange={handleProtocolChange}>
                            <option value="TCP">TCP</option>
                            <option value="HTTP">HTTP</option>
                            <option value="HTTPS">HTTPS</option>
                        </select>
                    </label>
                </div>
                <div className="label-group">
                    <label>
                        Local IP:
                        <input type="text" name="localIP" value={localIP} onChange={handleLocalIPChange} />
                    </label>
                </div>
                <div className="label-group">
                    <label>
                        Port:
                        <input type="text" name="port" value={port} onChange={handlePortChange} />
                    </label>
                </div>
                <div>
                    <button type="submit" className="button">Start Listener</button>
                </div>
            </form>
        </div>
        <div className="section">
            <h2>Configured Listener Details</h2>
            {listenerConfigs.length > 0 ? (
                listenerConfigs.map((config, index) => (
                    <div className="config-item" key={index}>
                        <p>Protocol: {config.protocol}</p>
                        <p>Local IP: {config.localIP}</p>
                        <p>Port: {config.port}</p>
                        <button onClick={() => handleStopListener(config.protocol, config.localIP, config.port)} className="button">Stop Listener</button>
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
import React, { useState } from 'react';
import axios from 'axios';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './PayloadStyles.css';

function Payloads() {
  const [payload, setPayload] = useState({
    name: '',
    lhost: '',
    lport: '',
    type: '.py', // Setting default value for type
    protocol: 'tcp', // Setting default value for protocol
    persistence: false,
    userAgent: '',
    sleepTimer: '',
  });

  const userAgents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"
  ];

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setPayload(prevState => ({
      ...prevState,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const isValidIP = (ip) => {
    return /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(ip);
  };

  const isValidPort = (port) => {
    const num = Number(port);
    return num >= 1 && num <= 65535 && Number.isInteger(num);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Define required fields based on protocol
    const requiredFields = ['name', 'lhost', 'lport', 'type', 'protocol'];
    if (payload.protocol === 'http' || payload.protocol === 'https') {
      requiredFields.push('userAgent', 'sleepTimer');
    }

    // Check if any required field is empty or invalid
    for (const field of requiredFields) {
      if (!payload[field]) {
        toast.error('Please fill out all required fields.');
        return;
      }
    }

    if (!isValidIP(payload.lhost)) {
      toast.error('Invalid IP address format.');
      return;
    }

    if (!isValidPort(payload.lport)) {
      toast.error('Invalid port number. Port must be between 1 and 65535.');
      return;
    }

    const headers = {
      'Content-Type': 'application/json'
    };

    const generate_payload_url=process.env.REACT_APP_API_GENERATE_PAYLOAD

    axios.post(generate_payload_url, payload, { headers })
      .then(response => {
        console.log(response.data);
        window.location.href = response.data.downloadUrl;
        toast.success('Payload generated successfully!');
      })
      .catch(error => {
        console.error('There was an error generating the payload:', error);
        toast.error('Error generating payload. Please try again.');
      });
  };

  return (
    <div className="payload-container">
      <h2 className="payload-header">Welcome to Payloads!</h2>
      <p className="payload-instructions">Guide to create your first Payload</p>

      <form onSubmit={handleSubmit} className="payload-form">
        <div>
          <label>
            Name:
            <input type="text" name="name" value={payload.name} onChange={handleChange} />
          </label>
        </div>
        <div>
          <label>
            Lhost:
            <input type="text" name="lhost" value={payload.lhost} onChange={handleChange} />
          </label>
        </div>
        <div>
          <label>
            Lport:
            <input type="text" name="lport" value={payload.lport} onChange={handleChange} />
          </label>
        </div>
        <div>
          <label>
            Type (.py or .exe):
            <select name="type" value={payload.type} onChange={handleChange}>
              <option value=".py">.py</option>
              <option value=".exe">.exe</option>
            </select>
          </label>
        </div>
        <div>
          <label>
            Protocol (TCP, HTTP, HTTPS):
            <select name="protocol" value={payload.protocol} onChange={handleChange}>
              <option value="tcp">TCP</option>
              <option value="http">HTTP</option>
              <option value="https">HTTPS</option>
            </select>
          </label>
        </div>
        <div>
          <label>
            Enable Persistence:
            <input type="checkbox" name="persistence" checked={payload.persistence} onChange={handleChange} />
          </label>
        </div>

        {payload.protocol === 'http' || payload.protocol === 'https' ? (
          <>
            <div>
              <label>
                User Agent:
                <select name="userAgent" value={payload.userAgent} onChange={handleChange}>
                  <option value="">Select User Agent</option>
                  {userAgents.map((agent, index) => (
                    <option key={index} value={agent}>{agent}</option>
                  ))}
                </select>
              </label>
            </div>
            <div>
              <label>
                Sleep Timer (seconds):
                <input type="number" name="sleepTimer" value={payload.sleepTimer} onChange={handleChange} />
              </label>
            </div>
          </>
        ) : null}

        <div>
          <button type="submit">Create</button>
        </div>
      </form>
      <ToastContainer />
    </div>
  );
}

export default Payloads;

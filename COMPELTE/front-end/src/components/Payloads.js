import React, { useState } from 'react';
import axios from 'axios';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

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

  //const notify = () => toast("Wow so easy!");

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

  // Handle form submission
const handleSubmit = (e) => {
  e.preventDefault();

  // Define required fields based on protocol
  const requiredFields = ['name', 'lhost', 'lport', 'type', 'protocol'];
  if (payload.protocol === 'http' || payload.protocol === 'https') {
    requiredFields.push('userAgent', 'sleepTimer');
  }

  // Check if any required field is empty
  for (const field of requiredFields) {
    if (!payload[field]) {
      toast.error('Please fill out all required fields.');
      return;
    }
  }

  const headers = {
    'Content-Type': 'application/json'
  };

  axios.post('http://127.0.0.1:5002/api/generate-payload', payload, { headers })
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
    <div>
      <h2>Welcome to Payloads!</h2>
      <p>Guide to create your first Payload</p>

      <form onSubmit={handleSubmit}>
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
              Protocol (tcp, http, https):
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

import React, { useState } from 'react';
import axios from 'axios';

function Payloads() {
  const [payload, setPayload] = useState({
    name: '',
    lhost: '',
    lport: '',
    type: '',
    protocol: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setPayload(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const headers = {
      'Content-Type': 'application/json'
    };

    axios.post('http://127.0.0.1:5002/api/generate-payload', payload, { headers })
      .then(response => {
        console.log(response.data);
        // Use window.location.href to navigate to the download URL,
        // which should automatically trigger the file download.
        window.location.href = response.data.downloadUrl;
        alert('Payload generated successfully!');
      })
      .catch(error => {
        console.error('There was an error generating the payload:', error);
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
          <button type="submit">Create</button>
        </div>
      </form>
    </div>
  );
}

export default Payloads;

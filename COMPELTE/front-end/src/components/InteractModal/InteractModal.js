import React, { useState, useEffect } from 'react';
import './InteractModal.css'; // Import the CSS file specifically for InteractModal

function InteractModal({ agentId, onClose }) {
  const [command, setCommand] = useState('');
  const [output, setOutput] = useState('');
  const [selectedFile, setSelectedFile] = useState(null); // State to handle the selected file
  const [filesList, setFilesList] = useState([]); // State for files available for upload

  useEffect(() => {
    // Fetch the list of available files for upload
    fetchFilesList();
  }, [agentId, selectedFile]); // Dependency array includes selectedFile to refetch list when a new file is uploaded

  // Fetch the list of files from the server
  const fetchFilesList = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:5002/list_files/${agentId}`);
      const data = await response.json();
      if (response.ok) {
        setFilesList(data.files || []);
      } else {
        console.error('Failed to fetch files list:', response.statusText);
      }
    } catch (error) {
      console.error('Error fetching files list:', error);
    }
  };

  // Function to handle file selection
  const handleFileSelect = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  // Function to handle file upload to the backend
  const handleFileUpload = async () => {
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('agent_id', agentId);

    const response = await fetch('http://127.0.0.1:5002/upload', {
      method: 'POST',
      body: formData,
    });

    const result = await response.json();
    if (response.ok) {
      console.log(result.message); // Log the success message
      fetchFilesList(); // Refresh the files list
    } else {
      console.error(result.error); // Log the error
    }
  };

  // Function to handle command submission
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
        <div className="files-upload-section">
          <input type="file" onChange={handleFileSelect} className="file-input" />
          <button onClick={handleFileUpload} className="interact-upload-button">Upload</button>
          <h2>Files Available for Upload:</h2>
          <ul className="files-list">
            {filesList.map(file => (
              <li key={file}>{file}</li>
            ))}
          </ul>
        </div>
        <div className="response-section">
          <div className="interact-command-output">{output}</div>
        </div>
        <div className="command-input-section">
          <input
            type="text"
            value={command}
            onChange={(e) => setCommand(e.target.value)}
            placeholder="Enter command"
            className="interact-command-input"
          />
          <button type="submit" onClick={handleCommandSubmit} className="interact-submit-button">Send</button>
        </div>
      </div>
    </div>
  );
}

export default InteractModal;

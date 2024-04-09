import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import './InteractModal.css';

// Setup the WebSocket connection
const socket = io('http://127.0.0.1:5002');

function InteractModal({ agentId, agentName, protocol, onClose }) {
    const [command, setCommand] = useState('');
    const [output, setOutput] = useState('');
    const [selectedFile, setSelectedFile] = useState(null);
    const [filesList, setFilesList] = useState([]);

    useEffect(() => {
        fetchFilesList(); // Fetch the list of available files for upload

        socket.on('output_received', (data) => {
            if (data.http_output && (protocol === 'HTTP' || protocol === 'HTTPS') && data.http_output.agent_id === agentId) {
                const formattedOutput = `Command: ${data.http_output.command}\nResponse: ${data.http_output.output}`;
                setOutput(formattedOutput || 'No output returned.');
            }
        });

        return () => socket.off('output_received');
    }, [agentId, protocol]);

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

    const handleFileSelect = (e) => {
        setSelectedFile(e.target.files[0]);
    };

    const handleFileUpload = async () => {
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('agent_id', agentId);

        try {
            const response = await fetch('http://127.0.0.1:5002/upload', {
                method: 'POST',
                body: formData,
            });
            const result = await response.json();
            if (response.ok) {
                console.log(result.message);
                fetchFilesList();
            } else {
                console.error(result.error);
            }
        } catch (error) {
            console.error('Error during file upload:', error);
        }
    };

    const handleCommandSubmit = async (e) => {
        e.preventDefault();
        setOutput('Processing...');

        try {
            const response = await fetch(`http://127.0.0.1:5002/api/execute-command/${protocol}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ agentId, command }),
            });
            const data = await response.json();

            if (response.ok) {
                if (protocol === 'TCP') {
                    setOutput(data.response || 'Command executed with no output.');
                } else {
                    console.log('Command sent, awaiting response...');
                }
            } else {
                setOutput(`Error: ${data.error || 'Failed to execute command'}`);
            }
        } catch (error) {
            console.error('Failed to send command', error);
            setOutput(`Network error: ${error.message || 'Failed to send command'}`);
        }

        setCommand('');
    };

    return (
        <div className="interact-modal">
            <div className="interact-modal-content">
                <span className="interact-close-button" onClick={onClose}>&times;</span>
                <div className="session-info">{`${protocol.toUpperCase()} Agent ${agentName}`}</div>
                <div className="files-upload-section">
                    <input type="file" onChange={handleFileSelect} className="file-input" />
                    <button onClick={handleFileUpload} className="interact-upload-button">Upload</button>
                    <h2>Files Available for Upload:</h2>
                    <ul className="files-list">
                        {filesList.map(file => <li key={file}>{file}</li>)}
                    </ul>
                </div>
                <div className="response-section">
                    <pre className="interact-command-output">{output}</pre>
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

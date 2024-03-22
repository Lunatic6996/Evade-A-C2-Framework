import React, { useEffect } from 'react';
import io from 'socket.io-client';
import { useAgentData } from './AgentDataContext'; // Ensure this path is correct

const socket = io('http://127.0.0.1:5002'); // Update with your actual server URL

function Callbacks() {
  const { agents, setAgents } = useAgentData(); // Use the useAgentData hook here

  useEffect(() => {
    socket.on('connection_status', (data) => {
      console.log(data.message); // "Successfully connected to the server"
    });
    socket.on('agent_update', (data) => {
        console.log(data); // Log incoming data
        setAgents(prevAgents => [...prevAgents, data]);
    });
    return () => {
      socket.off('connection_status');
      socket.off('agent_update');
    };
  }, [setAgents]); // Dependency array

  return (
    <div>
      <p>Welcome to Callbacks!</p>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        {agents.map((agent, index) => (
          <div key={index} style={{ display: 'flex', marginBottom: '10px' }}>
            <p style={{ marginRight: '100px' }}>{agent.agent_id}</p>
            <p style={{ marginRight: '100px' }}>{agent.protocol}</p>
            <p>{agent.last_seen}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Callbacks;

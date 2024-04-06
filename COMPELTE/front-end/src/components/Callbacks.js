import React, { useState } from 'react';
import { useAgentData } from './AgentDataContext';
import InteractModal from './InteractModal/InteractModal'; // Ensure the path is correct

function Callbacks() {
  const { agents } = useAgentData();
  const [showModal, setShowModal] = useState(false);
  const [currentAgentId, setCurrentAgentId] = useState(null);
  const [currentProtocol, setCurrentProtocol] = useState(null);  // Added state for protocol

  const handleInteractClick = (agentId, protocol) => {
    setCurrentAgentId(agentId);
    setCurrentProtocol(protocol);  // Store the protocol when an agent is clicked
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setCurrentAgentId(null);
    setCurrentProtocol(null);  // Reset protocol on modal close
  };

  return (
    <div style={{ maxWidth: '800px', margin: 'auto' }}>
      <h2>Welcome to Callbacks!</h2>
      {agents.map((agent, index) => (
        <div key={index} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px', padding: '10px', background: '#f0f0f0', borderRadius: '5px' }}>
          <div style={{ flexGrow: 1, display: 'flex', justifyContent: 'space-between' }}>
            <span>{agent.agent_name ? `Name: ${agent.agent_name}` : `ID: ${agent.agent_id}`}</span>
            <span>Protocol: {agent.protocol}</span>
            <span>Last Seen: {agent.last_seen}</span>
          </div>
          <button onClick={() => handleInteractClick(agent.agent_id, agent.protocol)} style={{ marginLeft: '20px' }}>Interact</button>
        </div>
      ))}
      {showModal && (
        <InteractModal agentId={currentAgentId} protocol={currentProtocol} onClose={handleCloseModal} />
      )}
    </div>
  );
}

export default Callbacks;

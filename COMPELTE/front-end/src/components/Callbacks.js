import React, { useState } from 'react';
import { useAgentData } from './AgentDataContext';
import InteractModal from './InteractModal/InteractModal'; // Ensure the path is correct

function Callbacks() {
  const { agents } = useAgentData();
  const [showModal, setShowModal] = useState(false);
  const [currentAgentId, setCurrentAgentId] = useState(null);
  const [currentAgentName, setCurrentAgentName] = useState(''); // State to store the current agent's name
  const [currentProtocol, setCurrentProtocol] = useState(null);

  const handleInteractClick = (agentId, agentName, protocol) => {
    setCurrentAgentId(agentId);
    setCurrentAgentName(agentName); // Store the agent name when an agent is clicked
    setCurrentProtocol(protocol);
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setCurrentAgentId(null);
    setCurrentAgentName(''); // Reset agent name on modal close
    setCurrentProtocol(null);
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
          <button onClick={() => handleInteractClick(agent.agent_id, agent.agent_name, agent.protocol)} style={{ marginLeft: '20px' }}>Interact</button>
        </div>
      ))}
      {showModal && (
        <InteractModal 
          agentId={currentAgentId} 
          agentName={currentAgentName} 
          protocol={currentProtocol} 
          onClose={handleCloseModal} 
        />
      )}
    </div>
  );
}

export default Callbacks;

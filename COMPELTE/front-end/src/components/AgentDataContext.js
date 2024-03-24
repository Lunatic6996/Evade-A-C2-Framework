import React, { createContext, useContext, useEffect, useState } from 'react';
import io from 'socket.io-client';

// Initialize socket connection
const socket = io('http://127.0.0.1:5002');

const AgentDataContext = createContext();

export const AgentDataProvider = ({ children }) => {
  const [agents, setAgents] = useState([]);

  // Listen for agent updates
  useEffect(() => {
    socket.on('agent_update', (newAgent) => {
      setAgents((prevAgents) => [...prevAgents, newAgent]);
    });

    // Cleanup on unmount
    return () => {
      socket.off('agent_update');
    };
  }, []);

  return (
    <AgentDataContext.Provider value={{ agents, setAgents }}>
      {children}
    </AgentDataContext.Provider>
  );
};

export const useAgentData = () => useContext(AgentDataContext);

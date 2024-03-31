import React, { createContext, useContext, useEffect, useState } from 'react';
import io from 'socket.io-client';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// Initialize socket connection
const socket = io('http://127.0.0.1:5002');

const AgentDataContext = createContext();

export const AgentDataProvider = ({ children }) => {
  const [agents, setAgents] = useState([]);

  // Listen for agent updates
  useEffect(() => {
    socket.on('agent_update', (newAgent) => {
      setAgents((prevAgents) => [...prevAgents, newAgent]);
      // Prefer to display agent's name, fallback to agent ID if name is not available
      const displayInfo = newAgent.agent_name || `Agent ${newAgent.agent_id}`;
      toast.info(`Callback from ${displayInfo}`);
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

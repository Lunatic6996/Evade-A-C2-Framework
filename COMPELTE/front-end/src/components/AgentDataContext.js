import React, { createContext, useContext, useState } from 'react';

const AgentDataContext = createContext();

export const AgentDataProvider = ({ children }) => {
  const [agents, setAgents] = useState([]); // Ensure agents is initialized as an array

  return (
    <AgentDataContext.Provider value={{ agents, setAgents }}>
      {children}
    </AgentDataContext.Provider>
  );
};

// Custom hook to use the agent data context
export const useAgentData = () => useContext(AgentDataContext);

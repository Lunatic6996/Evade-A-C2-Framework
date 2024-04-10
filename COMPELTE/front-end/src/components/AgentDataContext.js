import React, { createContext, useContext, useEffect, useState } from 'react';
import io from 'socket.io-client';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// Initialize socket connection
const socket = io(process.env.REACT_APP_SOCKET);

const AgentDataContext = createContext();

export const AgentDataProvider = ({ children }) => {
    const [agents, setAgents] = useState([]);

    useEffect(() => {
        socket.on('agent_update', (newAgent) => {
            setAgents(prevAgents => [...prevAgents, newAgent]);
            // Construct a detailed notification message including type, name, and address
            const notificationMessage = `Callback from ${newAgent.protocol || 'Unknown'} agent ${newAgent.agent_name || `Agent ${newAgent.agent_id}`} from IP:PORT ${newAgent.address || 'Unknown address'}.`;
            toast.info(notificationMessage);
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

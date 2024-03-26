import React, { createContext, useContext, useState } from 'react';

const ListenerContext = createContext();

export const useListener = () => useContext(ListenerContext);

export const ListenerProvider = ({ children }) => {
  const [listenerConfig, setListenerConfig] = useState(null);

  const saveListenerConfig = (config) => {
    setListenerConfig(config);
  };

  return (
    <ListenerContext.Provider value={{ listenerConfig, saveListenerConfig }}>
      {children}
    </ListenerContext.Provider>
  );
};

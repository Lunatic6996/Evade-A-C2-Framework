import React, { createContext, useContext, useState } from 'react';

const ListenerContext = createContext();

export const useListener = () => useContext(ListenerContext);

export const ListenerProvider = ({ children }) => {
  const [listenerConfigs, setListenerConfigs] = useState([]); // Initialize as an empty array

  const saveListenerConfig = (config) => {
    setListenerConfigs((prevConfigs) => [...prevConfigs, config]); // Append new config to the array
  };

  return (
    <ListenerContext.Provider value={{ listenerConfigs, saveListenerConfig }}>
      {children}
    </ListenerContext.Provider>
  );
};

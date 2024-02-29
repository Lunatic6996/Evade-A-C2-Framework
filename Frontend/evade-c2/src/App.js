// App.js

import React, { useState } from 'react';
import './App.css';
import NavigationBar from './components/NavigationBar';
import Home from './components/Home';
import Listener from './components/Listener';
import Payloads from './components/Payloads';
import Callbacks from './components/Callbacks';
import Documentation from './components/Document';

function App() {

  console.log(">>>", process.env.REACT_APP_API_KEY)

  const [currentPage, setCurrentPage] = useState('Home');

  const renderPage = () => {
    switch (currentPage) {
      case 'Listener':
        return <Listener />;
      case 'Payloads':
        return <Payloads />;
      case 'Callbacks':
        return <Callbacks />;
      case 'Documentation':
        return <Documentation />;
      default:
        return <Home />;
    }
  };



  return (
    <div className="App">
      <NavigationBar setCurrentPage={setCurrentPage} />
      {renderPage()}
    </div>
  );
}

export default App;

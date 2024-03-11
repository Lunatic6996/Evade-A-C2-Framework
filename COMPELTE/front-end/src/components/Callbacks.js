// Callbacks.js

import React from 'react';

function Callbacks() {
  return (
    <div>
      <p>Welcome to Callbacks!</p>

      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <p>Agents</p>
        <div style={{ display: 'flex', marginBottom: '10px' }}>
          <p style={{ marginRight: '100px' }}>Name</p>
          <p style={{ marginRight: '100px' }}>Protocol</p>
          <p>Last seen</p>
        </div>

        {/* Box with border and Command button to the right */}
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
          <div style={{ border: '2px solid #333', padding: '10px', borderRadius: '5px' }}>
            {/* Content inside the box */}
            <p>Additional content goes here</p>
          </div>
          <button style={{ marginLeft: '10px' }}>Command</button>
        </div>
      </div>
    </div>
  );
}

export default Callbacks;

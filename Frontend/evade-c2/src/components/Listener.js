// Listener.js

import React from 'react';

function Listener() {
  return (
    <div>
      <p>Welcome to Listener!</p>
      <p>You can create three different types of listener here. First TCP, HTTP, and HTTPS</p>

      <form>
        <div>
          <label>
            Protocol:
            <input type="text" name="protocol" />
          </label>
        </div>
        <div>
          <label>
            Local IP:
            <input type="text" name="localIP" />
          </label>
        </div>
        <div>
          <label>
            Port:
            <input type="text" name="port" />
          </label>
        </div>
        <div>
          <button type="submit">Start Listener</button>
        </div>
      </form>
    </div>
  );
}

export default Listener;

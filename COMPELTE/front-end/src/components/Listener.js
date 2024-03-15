import React from 'react';

function Listener() {
  return (
    <div>
      <p>Welcome to Listener!</p>
      <p>You can create three different types of listener here: TCP, HTTP, and HTTPS.</p>

      <form>
        <div>
          <label>
            Protocol:
            <select name="protocol">
              <option value="TCP">TCP</option>
              <option value="HTTP">HTTP</option>
              <option value="HTTPS">HTTPS</option>
            </select>
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

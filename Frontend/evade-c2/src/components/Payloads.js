// Payloads.js

import React from 'react';

function Payloads() {
  return (
    <div>
      <p>Welcome to Payloads!</p>
      <p>Guide to create your first Payload</p>

      <form>
        <div>
          <label>
            Name:
            <input type="text" name="name" />
          </label>
        </div>
        <div>
          <label>
            Lhost:
            <input type="text" name="lhost" />
          </label>
        </div>
        <div>
          <label>
            Lport:
            <input type="text" name="lport" />
          </label>
        </div>
        <div>
          <label>
            Type:
            <input type="text" name="type" />
          </label>
        </div>
        <div>
          <label>
            Protocol:
            <input type="text" name="protocol" />
          </label>
        </div>
        <div>
          <button type="submit">Create</button>
        </div>
      </form>
    </div>
  );
}

export default Payloads;

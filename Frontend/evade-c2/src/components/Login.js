// Login.js
import React, { useState } from 'react';
import './Login.css'; // Assuming you'll create a separate CSS file for styling

const Login = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // Check both username and password against environment variables
    if (username === process.env.REACT_APP_LOGIN_USERNAME && password === process.env.REACT_APP_LOGIN_PASSWORD) {
      onLoginSuccess();
    } else {
      alert('Incorrect username or password');
    }
  };

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit} className="login-form">
        <h2>Login</h2>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;

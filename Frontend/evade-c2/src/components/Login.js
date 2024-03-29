import React, { useState } from 'react';
import './Login.css'; // Ensure this is correctly linked
import logoSrc from '../LOGO.svg';

const Login = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // Authentication logic
    if (username === process.env.REACT_APP_LOGIN_USERNAME && password === process.env.REACT_APP_LOGIN_PASSWORD) {
      onLoginSuccess();
    } else {
      alert('Incorrect username or password');
    }
  };

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit} className="login-form">
        <div className="login-logo-container">
          <img src={logoSrc} alt="Logo" className="login-logo" />
        </div>
        <h2>Login</h2>
        <div className="input-group">
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="input-group">
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="login-button">Login</button>
      </form>
  </div>

  );
};

export default Login;

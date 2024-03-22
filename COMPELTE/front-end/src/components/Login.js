import React, { useState, useEffect } from 'react';
import './Login.css';
import logoSrc from '../LOGO.svg';

const Login = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    const checkLoginStatus = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5002/api/check_login', {
          credentials: 'include', // Ensure cookies are sent with the request
        });
        const data = await response.json();
        if (data.logged_in) {
          onLoginSuccess();
        }
      } catch (error) {
        console.error("Failed to verify login status", error);
        setErrorMessage('Could not verify login status. Please try to login again.');
      }
    };

    checkLoginStatus();
  }, [onLoginSuccess]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage(''); // Reset error message
    try {
      const response = await fetch('http://127.0.0.1:5002/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
        credentials: 'include',
      });
      const data = await response.json();

      if (response.ok) {
        onLoginSuccess();
      } else {
        setErrorMessage(data.message || 'Incorrect username or password.');
      }
    } catch (error) {
      console.error('Login failed:', error);
      setErrorMessage('Network error, login request failed. Please try again.');
    }
  };

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit} className="login-form">
        <div className="login-logo-container">
          <img src={logoSrc} alt="Logo" className="login-logo" />
        </div>
        <h2>Login</h2>
        {errorMessage && <div className="error-message">{errorMessage}</div>}
        <div className="input-group">
          <input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} required />
        </div>
        <div className="input-group">
          <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
        </div>
        <button type="submit" className="login-button">Login</button>
      </form>
    </div>
  );
};

export default Login;

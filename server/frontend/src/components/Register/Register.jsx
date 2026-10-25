import React, { useState } from 'react';
import './Register.css';
import Header from '../Header/Header';

const Register = () => {
  const [formData, setFormData] = useState({
    username: '',
    firstName: '',
    lastName: '',
    email: '',
    password: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((current) => ({ ...current, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setSuccess('');

    if (!formData.username || !formData.email || !formData.password) {
      setError('Please complete the required fields.');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${window.location.origin}/djangoapp/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: formData.username,
          first_name: formData.firstName,
          last_name: formData.lastName,
          email: formData.email,
          password: formData.password,
        }),
      });

      const json = await response.json();
      if (!response.ok) {
        throw new Error(json.error || 'Registration failed.');
      }

      sessionStorage.setItem('username', json.userName || formData.username);
      setSuccess('Registration successful! Redirecting to the home page...');
      window.setTimeout(() => {
        window.location.href = '/';
      }, 1000);
    } catch (err) {
      setError(err.message || 'Registration failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Header />
      <div className="register_container">
        <h2 className="header">Register</h2>
        <form onSubmit={handleSubmit} className="submit_panel">
          <input className="input_field" type="text" name="username" value={formData.username} placeholder="Username" onChange={handleChange} required />
          <input className="input_field" type="text" name="firstName" value={formData.firstName} placeholder="First Name" onChange={handleChange} />
          <input className="input_field" type="text" name="lastName" value={formData.lastName} placeholder="Last Name" onChange={handleChange} />
          <input className="input_field" type="email" name="email" value={formData.email} placeholder="Email" onChange={handleChange} required />
          <input className="input_field" type="password" name="password" value={formData.password} placeholder="Password" onChange={handleChange} required />
          {error && <div className="alert alert-danger">{error}</div>}
          {success && <div className="alert alert-success">{success}</div>}
          <button type="submit" className="submit" disabled={loading}>{loading ? 'Registering...' : 'Register'}</button>
        </form>
      </div>
    </div>
  );
};

export default Register;

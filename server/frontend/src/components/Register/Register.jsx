```jsx
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

    setFormData((current) => ({
      ...current,
      [name]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setSuccess('');

    if (
      !formData.username.trim() ||
      !formData.firstName.trim() ||
      !formData.lastName.trim() ||
      !formData.email.trim() ||
      !formData.password
    ) {
      setError('Please fill in all five fields.');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(
        `${window.location.origin}/djangoapp/register`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: formData.username.trim(),
            first_name: formData.firstName.trim(),
            last_name: formData.lastName.trim(),
            email: formData.email.trim(),
            password: formData.password,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok || data.status >= 400 || data.error) {
        throw new Error(data.error || 'Registration failed. Please try again.');
      }

      sessionStorage.setItem(
        'username',
        data.userName || formData.username
      );

      setSuccess('Registration successful!');

      window.setTimeout(() => {
        window.location.href = '/';
      }, 1000);
    } catch (err) {
      setError(err.message || 'Unable to register. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Header />

      <main className="register_container">
        <h2 className="header">Sign Up</h2>

        <form onSubmit={handleSubmit} className="submit_panel">
          <label htmlFor="username">Username</label>
          <input
            id="username"
            className="input_field"
            type="text"
            name="username"
            value={formData.username}
            placeholder="Enter username"
            onChange={handleChange}
            autoComplete="username"
            required
          />

          <label htmlFor="firstName">First Name</label>
          <input
            id="firstName"
            className="input_field"
            type="text"
            name="firstName"
            value={formData.firstName}
            placeholder="Enter first name"
            onChange={handleChange}
            autoComplete="given-name"
            required
          />

          <label htmlFor="lastName">Last Name</label>
          <input
            id="lastName"
            className="input_field"
            type="text"
            name="lastName"
            value={formData.lastName}
            placeholder="Enter last name"
            onChange={handleChange}
            autoComplete="family-name"
            required
          />

          <label htmlFor="email">Email</label>
          <input
            id="email"
            className="input_field"
            type="email"
            name="email"
            value={formData.email}
            placeholder="Enter email address"
            onChange={handleChange}
            autoComplete="email"
            required
          />

          <label htmlFor="password">Password</label>
          <input
            id="password"
            className="input_field"
            type="password"
            name="password"
            value={formData.password}
            placeholder="Enter password"
            onChange={handleChange}
            autoComplete="new-password"
            required
          />

          {error && (
            <div className="alert alert-danger" role="alert">
              {error}
            </div>
          )}

          {success && (
            <div className="alert alert-success" role="status">
              {success}
            </div>
          )}

          <button
            type="submit"
            className="submit"
            disabled={loading}
          >
            {loading ? 'Registering...' : 'Register'}
          </button>
        </form>
      </main>
    </div>
  );
};

export default Register;
```

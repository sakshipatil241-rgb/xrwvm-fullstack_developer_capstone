import React from 'react';
import { Route, Routes } from 'react-router-dom';
import LoginPanel from './components/Login/Login';
import Dealers from './components/Dealers/Dealers';
import Dealer from './components/Dealers/Dealer';
import PostReview from './components/Dealers/PostReview';
import Register from './components/Register/Register';

function AboutPage() {
  return (
    <div className="container my-4">
      <h1>About Us</h1>
      <p>We help drivers discover the right dealership and share honest reviews.</p>
      <p>Our platform connects inventory, local dealer information, and customer feedback in one place.</p>
    </div>
  );
}

function ContactPage() {
  return (
    <div className="container my-4">
      <h1>Contact Us</h1>
      <p>Email: support@ibm.com</p>
      <p>Phone: +1 (800) 555-0199</p>
      <p>Address: 24 Innovation Way, Austin, TX 78701</p>
    </div>
  );
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<Dealers />} />
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/register" element={<Register />} />
      <Route path="/dealer/:id" element={<Dealer />} />
      <Route path="/postreview/:id" element={<PostReview />} />
      <Route path="/about" element={<AboutPage />} />
      <Route path="/contact" element={<ContactPage />} />
    </Routes>
  );
}

export default App;

// SignUp.js

import React, { useState } from "react";
import { Link } from "react-router-dom";
import axios from 'axios';



const SignUp = () => {

  document.title = "signup";
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");


  const handleSubmit = async (e) => {
    e.preventDefault();
    // console.log("Username:", username);
    // console.log("Email:", email);
    // console.log("Password:", password);
    // Add your sign-up logic here
    try{
      const response = await axios.post('http://127.0.0.1:8000/register', {username, email, password});
      console.log(response)
      // setMessage("User created successfully. Please login.");
      // setUsername('');
      // setEmail('');
      // setPassword('');
    }
    catch (error){
      console.log(error)
      if (error.response){
        console.log(error.response.data.detail);
      }else{
        setMessage("An error occured. Please try again later");
      }
    }
  };

  return (
    <div className="auth-container">
      <form onSubmit={handleSubmit} className="auth-form">
        <h2>Sign Up</h2>
        {/* {message && <p className="auth-message">{message}</p>} Display message */}
        <div className="input-container">
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            className="input-field"
          />
        </div>
        <div className="input-container">
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="input-field"
          />
        </div>
        <div className="input-container">
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="input-field"
          />
        </div>
        <button type="submit" className="auth-button">
          Sign Up
        </button>
        <p className="auth-redirect">
          Already have an account? <Link to="/signin">Sign In</Link>
        </p>
        <p className="auth-redirect">
          <Link to="/">Go back to home page</Link>
        </p>
      </form>
    </div>
  );
};

export default SignUp;

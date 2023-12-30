// SignIn.js
import axios from "axios";
import React, { useState } from "react";
import { Link } from "react-router-dom";

const SignIn = () => {
  document.title = "Signin";
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    // console.log("Username:", username);
    // console.log("Email:", email);
    // console.log("Password:", password);
    // Add your sign-up logic here
    try{
      const formdata = new FormData();
      formdata.append('username', email)
      formdata.append('password', password)
      const response = await axios.post('http://127.0.0.1:8000/login', formdata);
      console.log(response);
      // setUsername('');
      setEmail('');
      setPassword('');
    }
    catch (error){
      console.log('Error: ', error);
    }
  };

  return (
    <div className="auth-container">
      <form onSubmit={handleSubmit} className="auth-form">
        <h2>Sign In</h2>
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
          Sign In
        </button>
        <p className="auth-redirect">
          Don't have an account? <Link to="/signup">Sign Up</Link>
        </p>
        <p className="auth-redirect">
          <Link to="/">Go back to home page</Link>
        </p>
      </form>
    </div>
  );
};

export default SignIn;

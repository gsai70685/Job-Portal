import React from "react";
import { Link } from "react-router-dom";
const Toggle = () => {
  return (
    <div>
      <div className="toggle-page">
        <div className="toggle-links">
          <Link to="/">Home</Link>
          <Link to="/blogs">Blogs</Link>
          <Link to="/jobs">Jobs</Link>
          <Link to="/post">Post a Job</Link>
        </div>
      </div>
    </div>
  );
};

export default Toggle;

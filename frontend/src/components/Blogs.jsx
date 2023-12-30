import React from "react";
import { Link } from "react-router-dom";
import Footer from "./Footer";
import Navbar from "../Navbar";

const Blogs = () => {
  return (
    <div>
      <Navbar />
      <div className="location">
        <span className="span">
          <Link to="/">Home</Link>
        </span>
        <span className="span"> {">"} </span>
        <span className="span">Blogs</span>
      </div>
      <div className="card">
        <div className="rect"></div>
        <div className="blog-content">
          <div className="desc">
            <span> jobs_yoeaay &nbsp; | &nbsp; April 9,2022</span>
            <h2>Top 10 jobs of 2021 in India</h2>
            <p>
              1. Data Scientist A data scientist, without a pinch of doubt, is
              the highest paying jobs across industries and sectors. …
            </p>
            <Link to="/article"> ➡️ Read More</Link>
          </div>
        </div>
      </div>
      <button className="post-btn">
        <Link to="/postblog">Post a Blog</Link>
      </button>

      <Footer />
    </div>
  );
};

export default Blogs;

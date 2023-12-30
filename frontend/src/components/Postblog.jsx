import React from "react";
import { Link } from "react-router-dom";
import Navbar from "../Navbar";
const Postblog = () => {
  return (
    <div>
      <Navbar />
      <div className="location">
        <span className="span">
          <Link to="/">Home</Link>
        </span>
        <span className="span"> {">"} </span>
        <span className="span">Post a Blog</span>
      </div>
      <div className="details">
        <form action="/action" className="form">
          <fieldset className="fieldset">
            <label className="label">Blog Title</label>
            <div className="label-content">
              <input type="text" className="label-input" required></input>
            </div>
          </fieldset>
          <fieldset className="fieldset">
            <label className="label">Description</label>
            <div className="label-content">
              <textarea
                name="jobdescription"
                id="jobdesc"
                rows="10"
                cols="30"
                required
              ></textarea>
            </div>
          </fieldset>
          <input type="submit" value="Upload" className="preview" />
        </form>
      </div>
    </div>
  );
};

export default Postblog;

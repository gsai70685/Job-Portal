import React from "react";
import { Link } from "react-router-dom";
import Footer from "./Footer";
import Navbar from "../Navbar";

const Postajob = () => {
  return (
    <div>
      <Navbar />
      <div className="location">
        <span className="span">
          <Link to="/">Home</Link>
        </span>
        <span className="span"> {">"} </span>
        <span className="span">Post a Job</span>
      </div>
      <div className="details">
        <div className="h1tag">
          <h1>Post a Job</h1>
        </div>
        <form action="/action" className="form">
          <fieldset className="fieldset">
            <label className="label">Have an account?</label>
            <div className="label-content">
              <Link to="/signin">
                <span>Sign in</span>
              </Link>
              &nbsp;&nbsp; If you don't have an account you can create one below
              by entering your email address/username. Your account details will
              be confirmed via email.
            </div>
          </fieldset>
          <fieldset className="fieldset">
            <label className="label">Your email</label>
            <div className="label-content">
              <input
                type="text"
                placeholder="you@yourdomain.com"
                className="label-input"
                required
              ></input>
            </div>
          </fieldset>
          <fieldset className="fieldset">
            <label className="label">Job Title</label>
            <div className="label-content">
              <input type="text" className="label-input" required></input>
            </div>
          </fieldset>
          <fieldset className="fieldset">
            <label className="label">
              Location <span>(optional)</span>{" "}
            </label>
            <div className="label-content">
              <input
                type="text"
                className="label-input"
                placeholder="e.g.'London'"
              ></input>
              <p>Leave this blank if location is not important</p>
            </div>
          </fieldset>
          <fieldset className="fieldset">
            <label className="label">Job Type</label>
            <div className="label-content">
              <select name="job_type" id="job_type">
                <option value="fulltime">Full Time</option>
                <option value="freelance">Freelance</option>
                <option value="internship">Internship</option>
                <option value="parttime">Part Time</option>
                <option value="temporary">Temporary</option>
              </select>
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
          <fieldset className="fieldset">
            <label className="label">Application email/URL</label>
            <div className="label-content">
              <input
                type="text"
                className="label-input"
                placeholder="Enter an email address or website URL"
                required
              ></input>
            </div>
          </fieldset>

          <fieldset className="fieldset">
            <label className="label">
              Salary <span>(optional)</span>{" "}
            </label>
            <div className="label-content">
              <input
                type="text"
                className="label-input"
                placeholder="e.g. USD$20.000"
              ></input>
            </div>
          </fieldset>

          <fieldset className="fieldset">
            <label className="label">
              Important Information: <span>(optional)</span>{" "}
            </label>
            <div className="label-content">
              <input
                type="text"
                className="label-input"
                placeholder="e.g. Work visa required"
              ></input>
            </div>
          </fieldset>

          <fieldset className="fieldset">
            <label className="label">
              Reported To <span>(optional)</span>{" "}
            </label>
            <div className="label-content">
              <input
                type="text"
                className="label-input"
                placeholder="Reported To"
              ></input>
            </div>
          </fieldset>

          <fieldset className="fieldset">
            <label className="label">
              Qualification <span>(optional)</span>{" "}
            </label>
            <div className="label-content">
              <input
                type="text"
                className="label-input"
                placeholder="Qualification"
              ></input>
            </div>
          </fieldset>

          <fieldset className="fieldset">
            <label className="label">
              Skills <span>(optional)</span>{" "}
            </label>
            <div className="label-content">
              <input
                type="text"
                className="label-input"
                placeholder="Skills"
              ></input>
            </div>
          </fieldset>

          <fieldset className="fieldset">
            <label className="label">
              Experience <span>(optional)</span>{" "}
            </label>
            <div className="label-content">
              <input
                type="text"
                className="label-input"
                placeholder="Experience"
              ></input>
            </div>
          </fieldset>
          <h1 className="h1tag2">Company Detalis</h1>
          <fieldset className="fieldset">
            <label className="label">Company name</label>
            <div className="label-content">
              <input
                type="text"
                className="label-input"
                placeholder="Enter the name of the company"
                required
              ></input>
            </div>
          </fieldset>
          <fieldset className="fieldset">
            <label className="label">
              Website <span>(optional)</span>{" "}
            </label>
            <div className="label-content">
              <input
                type="text"
                className="label-input"
                placeholder="http://"
              ></input>
            </div>
          </fieldset>
          <fieldset className="fieldset">
            <label className="label">
              Tagline <span>(optional)</span>{" "}
            </label>
            <div className="label-content">
              <input
                type="text"
                className="label-input"
                placeholder="Briefly describe your company"
              ></input>
            </div>
          </fieldset>
          <fieldset className="fieldset">
            <label className="label">
              Video <span>(optional)</span>{" "}
            </label>
            <div className="label-content">
              <input
                type="text"
                className="label-input"
                placeholder="A link to a video about your company"
              ></input>
            </div>
          </fieldset>
          <fieldset className="fieldset">
            <label className="label">
              Twitter username <span>(optional)</span>{" "}
            </label>
            <div className="label-content">
              <input
                type="text"
                className="label-input"
                placeholder="@yourcompany"
              ></input>
            </div>
          </fieldset>

          <fieldset className="fieldset">
            <label className="label">
              Logo <span>(optional)</span>{" "}
            </label>
            <div className="label-content">
              <input type="file" className="label-upload"></input>
              <p>Maxium file size: 512 MB.</p>
            </div>
          </fieldset>
          <input type="submit" value="Preview" className="preview" />
        </form>
      </div>
      <Footer />
    </div>
  );
};

export default Postajob;

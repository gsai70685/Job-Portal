import React from "react";
import Navbar from "../Navbar";
import { Link } from "react-router-dom";

const Jobs = () => {
  document.title = "Jobs-Jobs by Rivan";
  return (
    <div>
      <Navbar />
      <div className="location">
        <span className="span">
          <Link to="/">Home</Link>
        </span>
        <span className="span"> {">"} </span>
        <span className="span">Jobs</span>
      </div>
      <div className="container">
        <h1>Jobs</h1>
        <div>
          <form action="/search" method="get" class="search-job">
            <div className="search-job-div">
              <div class="search-job-container">
                <input
                  type="text"
                  name="keyword"
                  placeholder="Keywords"
                  className="search-job-input"
                />
                <input
                  type="text"
                  name="location"
                  placeholder="Location "
                  className="search-job-input"
                />
              </div>
              <button className="btn-job">Search Jobs</button>
            </div>
          </form>
        </div>
        <ul className="job_types">
          <li>
            <label htmlFor="job_type_freelance" className="freelance">
              <input
                type="checkbox"
                name="filter_job_type[]"
                value="freelance"
                id="job_type_freelance"
              />
              Freelance
            </label>
          </li>
          <li>
            <label htmlFor="job_type_full-time" className="full-time">
              <input
                type="checkbox"
                name="filter_job_type[]"
                value="full-time"
                id="job_type_full-time"
              />
              Full Time
            </label>
          </li>
          <li>
            <label htmlFor="job_type_internship" className="internship">
              <input
                type="checkbox"
                name="filter_job_type[]"
                value="internship"
                id="job_type_internship"
              />
              Internship
            </label>
          </li>
          <li>
            <label htmlFor="job_type_part-time" className="part-time">
              <input
                type="checkbox"
                name="filter_job_type[]"
                value="part-time"
                id="job_type_part-time"
              />
              Part Time
            </label>
          </li>
          <li>
            <label htmlFor="job_type_temporary" className="temporary">
              <input
                type="checkbox"
                name="filter_job_type[]"
                value="temporary"
                id="job_type_temporary"
              />
              Temporary
            </label>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default Jobs;

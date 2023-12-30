import React from "react";
import photo from "../assets/search.svg";
import Footer from "./Footer";
import Navbar from "../Navbar";

const Home = () => {
  return (
    <div>
      <Navbar />

      <img
        className="img"
        src="https://jobs.rivan.in/wp-content/themes/jobscout/images/banner-image.jpg"
        alt="photo"
      />
      <div className="centered">
        <h1>Aim Higher, Dream Higher</h1>
        <p>New Jobs Every Day</p>
      </div>
      <div className="searchhome">
        <form action="/search" method="get" class="search-form">
          <div class="search-container">
            <input
              type="text"
              name="keyword"
              placeholder="Keyword"
              className="search-input"
            />
            <input
              type="text"
              name="location"
              placeholder="Location "
              className="search-input"
            />
            <button className="btn" value="search">
              <img src={photo} alt="searchicon" />
            </button>
          </div>
        </form>
      </div>

      <Footer />
    </div>
  );
};

export default Home;

import React from "react";
import { Route, Routes } from "react-router-dom";
import Home from "./components/Home";
import Jobs from "./components/Jobs";
import Blogs from "./components/Blogs";
import Postajob from "./components/Postajob";
import Article from "./components/Article";
import Signin from "./components/Signin";
import Signup from "./components/Signup";
import Toggle from "./components/Toggle";
import Postblog from "./components/Postblog";
const App = () => {
  return (
    <div>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/blogs" element={<Blogs />} />
        <Route path="/jobs" element={<Jobs />} />
        <Route path="/post" element={<Postajob />} />
        <Route path="/article" element={<Article />} />
        <Route path="/signin" element={<Signin />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/toggle" element={<Toggle />} />
        <Route path="/postblog" element={<Postblog />} />
      </Routes>
    </div>
  );
};

export default App;

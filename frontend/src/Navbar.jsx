import { Link } from "react-router-dom";
import { FaBars, FaTimes } from "react-icons/fa";
export default function Navbar() {
  return (
    <div>
      <header className="header">
        <div className="logo">
          <h1>
            <Link to="/" className="site-title">
              <h1>Jobs by Rivan</h1>
            </Link>
          </h1>
          <p>Find your Cubical</p>
        </div>

        <div className="Pages">
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/blogs">Blogs</Link>
            </li>
            <li>
              <Link to="/jobs">Jobs</Link>
            </li>
            <li>
              <Link to="/post">Post a Job</Link>
            </li>
          </ul>
        </div>
        <button>
          <Link to="/toggle">
            <FaBars className="toggle" />
          </Link>
        </button>
      </header>
    </div>
  );
}
/*   <h1>
                <Link to="/" className="site-title">
                  <h1>Jobs by Rivan</h1>
                </Link>
              </h1>
              <p>Find your Cubical</p>
            </div>
<ul>
            <Link to="/home">Home</Link>
            <Link to="/blogs">Blogs</Link>
            <Link to="/jobs">Jobs</Link>
            <Link to="/post">Post a Job</Link>
          </ul>
        */

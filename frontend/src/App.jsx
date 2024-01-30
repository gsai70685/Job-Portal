import React, {useState, useEffect} from 'react'
import  {BrowserRouter as Router, Routes, Route, Navigate} from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './components/Home'
import './App.css'
import Login from './components/Login'
import Registeration from './components/Registeration'
import Jobs from './components/Jobs'
import Cookies from 'js-cookie'
import Logout from './components/Logout'
import Account from './components/Account'
import PostJob from './components/PostJob'
import ErrorPage from './components/ErrorPage'
import IndividualJob from './components/IndividualJob'
import Footer from './components/Footer'

const App = () => {
  const [userType, setUserType] = useState('');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true); // New loading state

  useEffect(() => {
    console.log("Auth mounted")
    // Function to check user authentication and user type
    const checkAuthentication = () => {
      const usertype = Cookies.get('role');
      // console.log("usertype", usertype)
      // Perform checks for token and user type (you can implement your custom logic here)
      if (usertype) {
        setUserType(usertype);
        setIsAuthenticated(true);
      } else {
        setUserType('');
        setIsAuthenticated(false);
      }
      setLoading(false); // Set loading to false after setting the user type
    };

    checkAuthentication();
  }, []);

  const handleUserTypeChange = (newUserType) => {
    setUserType(newUserType);
    setIsAuthenticated(true);
  };

  // Function to render protected routes based on user type
  const ProtectedRoute = ({ element: Element, allowedUserTypes, fallback }) => {
    if (!isAuthenticated) {
      // Redirect to login if not authenticated
      return <Navigate to="/signin" />;
    }

    if (allowedUserTypes.includes(userType)) {
      return <Element />;
    } else {
      // Redirect to a fallback page (e.g., home page) if not allowed user type
      return <Navigate to={fallback} />;
    }
  };


  if (loading) {
    // Show a loading state until the user type is determined
    return <div>Loading...</div>;
  }


  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/register" element={<Registeration/>} />
        <Route path="/home" element={<Home/>} />
        <Route path="/" element={<Home/>} />
        <Route path='/postjob' element={<PostJob/>}/>
        <Route path="/signin" element={<Login onUserTypeChange={handleUserTypeChange}/>} />
        <Route path='/jobs/:jobId' element={<IndividualJob/>}/>
        {/* Protected Routes */}
        <Route
          path="/logout"
          element={<ProtectedRoute element={Logout} allowedUserTypes={['User', 'Admin', 'HR']} fallback="/signin" />}
        />
        <Route
          path="/jobs"
          element={<ProtectedRoute element={Jobs} allowedUserTypes={['User', 'HR', 'Admin']} fallback="/signin" />}
        />
        <Route path="/account" element={<ProtectedRoute element={Account} allowedUserTypes={['User', 'HR', 'Admin']} fallback="/signin" />}/>
        {/* If none of the routes matched than we will display pick this route and display our error message */}
        <Route path='*' Component={ErrorPage}/>
      </Routes>
      <Footer/>
    </Router>
  );
}
export default App

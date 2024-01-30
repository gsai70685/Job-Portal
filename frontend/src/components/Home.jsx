import React, { useEffect, useContext, useState} from 'react'
import useCRUD from '../hooks/useCRUD'
import { usejobDataContext } from '../context/JobsContext'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'
import accenture from '../assets/logo/accenture.png'
import wipro from '../assets/logo/wipro.png'
import apple from '../assets/logo/apple.png'
import infosyslimited from '../assets/logo/infosys.png'
import tcs from '../assets/logo/tcs.png'
import bag from '../assets/logo/default.png'
import banner from '../assets/banner.jpg';
import { Link } from 'react-router-dom'

const Home = () => {
  const navigate = useNavigate();
  const {demoJobs, setDemoJobs} = usejobDataContext();
  const { fetchData, dataCrud } = useCRUD("jobs/home");
  const [searchRequest, setSearchRequest] = useState(false);
  const [responseData, setResponseData] = useState(null);
  const [searchedParameters, setSearchedParameters] = useState({
    keyword:"",
    location:""
  })

  useEffect(() => {
    // Once the page loads it will automatically call this function and get the demo jobs
    // and add them to the datacrud
    if (!demoJobs){
      fetchData();
    }
    console.log(demoJobs)
  }, [])

  useEffect(() => {
    // Once there is change iin the state of the datacrud than this will automatically run
    // and set the data in the context
    if (dataCrud){
      setDemoJobs(dataCrud)
    }
  }, [dataCrud]);

  const handleInputChange = (e) =>{
    // Once there is change in the input (that user types then this function will be called )
    const {name, value} = e.target;
    setSearchedParameters({
      ...searchedParameters,
      [name]:value
    })
  }

  useEffect(()=>{
    if(searchRequest){
      setDemoJobs(responseData)
    }
  },[responseData])

  const transformCompanyName = (company) => {
    // Convert to lowercase and remove spaces
    return company.toLowerCase().replace(/\s/g, '');
  };

  const getCompanyLogo = (companyName) => {
    // Use the transformed company name to dynamically import the corresponding logo
    switch (companyName) {
      case 'infosyslimited':
        return infosyslimited;
      case 'accenture':
        return accenture;
      case 'wipro':
        return wipro;
      case 'apple':
        return apple;
      case 'tcs':
        return tcs;
      default:
        // Return a default logo or handle other cases as needed
        return bag;
    }
  };

  const handleFormSubmit = async (e) =>{
    e.preventDefault();
    try {
      // const response = await axios.post("http://127.0.0.1:8000/jobs/all", searchedParameters, {withCredentials:true})
      const response = await axios.post("http://194.135.93.37:8100/jobs/all", searchedParameters, {withCredentials:true})
      if(response.data?.jobs){
        setSearchRequest(true);
        setResponseData(response.data.jobs)
      }
    } catch (error) {
      if(error.response?.status === 400 || error.response?.status === 401){
        navigate("/signin");
        // console.error("There was an error while making request")
        alert("You need to login to use this feature !!")
      }
    }
  }

  return (
    <div className='container max-w-[100vw] flex flex-col bg-center max-h-[80%] space-y-1'>
      <div className='container max-w-[100%] relative'>
        {/* <img className='w-[100%] h-[90vh] md:h-[80vh] object-cover' src="https://jobs.rivan.in/wp-content/themes/jobscout/images/banner-image.jpg" alt="Job-Banner" /> */}
        <img className=' w-[100%] h-[90vh] md:h-[40%] lg:h-[550px] object-cover' src={banner} alt="Job-Banner" />
          <h1 className='absolute  text-3xl md:text-4xl lg:text-5xl font-bold text-white top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2'>Aim Higher, Dream Higher</h1>
          <h1 className='absolute top-[50%] lg:top-[50%] md:top-[60%]  left-1/2 -translate-x-1/2 -translate-y-1/2 text-xl md:text2xl lg:text-xl text-white font-semibold'>New Jobs Every Day</h1>
          <div className='container max-w-[100%] mx-auto absolute top-[75%] md:top-[80%] lg:top-[65%] left-1/2 -translate-x-1/2 -translate-y-1/2 '>
            <form className='flex flex-col md:flex-row items-center justify-center' onSubmit={handleFormSubmit}>
                <input type="text" placeholder='Keyword' name='keyword' className='p-3 md:p-4 lg:p-4 w-[90%] md:w-[25%] rounded-md md:rounded-l-md lg:rounded-l-md lg:rounded-r-none mb-2 md:mb-0 text-md md:text-lg lg:text-lg' onChange={handleInputChange}/>
                <input type="text" placeholder='Location' name='location' className='p-3 md:p-4 lg:p-4 w-[90%] md:w-[25%] rounded-md md:rounded-r-md lg:rounded-r-md lg:rounded-l-none mb-2 md:mb-0 text-md md:text-lg lg:text-lg border-0 md:border-l-2 lg:border-l-3' onChange={handleInputChange}/>
                <button type='submit' className='p-3 md:p-4 lg:p-4 bg-[#000030] text-white rounded-sm w-[90%] md:w-[10%] text-md md:text-lg lg:text-lg'>Search</button>
            </form>
        </div>
      </div>
        <div className='container flex flex-col p-2 md:p-8 lg:p-10 max-w-[100%] mx-auto text-center bg-gray-50 items-center justify-center'>
        <div className='container flex mx-auto max-w-[100%] items-center space-x-3 md:space-x-12 lg:space-x-16 justify-center my-10 border shadow-md p-2 rounded-lg'>
          <img src={wipro} alt="" className='w-[2rem] basis-1/6 md:basis-1/12 lg:basis-1/12' />
          <img src={apple} alt="" className='w-[2rem] basis-1/6 md:basis-1/12 lg:basis-1/12' />
          <img src={tcs} alt="" className='w-[2rem] basis-1/6 md:basis-1/12 lg:basis-1/12' />
          <img src={accenture} alt="" className='w-[2rem] basis-1/6 md:basis-1/12 lg:basis-1/12' />
          <img src={infosyslimited} alt="" className='w-[2rem] basis-1/6 md:basis-1/12 lg:basis-1/12' />
        </div>
          <div className='container flex flex-col space-y-6 mx-auto max-w-[100%] text-center mt-8 md:mt-18 lg:mt-20'>
              {demoJobs && demoJobs.length > 0?(
                demoJobs.map(job =>(
                  <Link to={`/jobs/${job._id}`} key={job._id}>
                    <div className='flex flex-row hover:bg-white hover:cursor-pointer border rounded-md mb-3 items-center text-center p-2 md:py-4 lg:py-4'>
                      <div className='flex flex-col basis-1/2 md:basis-[60%] items-start text-wrap'>
                        <div className='flex text-[#000030] font-bold text-sm md:text-md lg:text-lg  space-x-0 md:space-x-2 lg:space-x-3'>
                          <img src={getCompanyLogo(transformCompanyName(job.company))} alt="company logo" className='hidden md:block lg:block  md:w-[3rem] lg:w-[3rem] h-[35px] text-sm font-normal'/>
                        <h1 className=' text-start'> {job.job_title}</h1>
                        </div>
                        <h1 className='text-gray-700 text-sm font-semibold ml-0 md:ml-[4rem] lg:ml-[4rem]'>{job.job_type}</h1>
                      </div>
                      <h1 className='p-3 md:p-2 lg:p-3 text-gray-500 font-semibold text-sm md:text-[1rem] lg:text-[1rem]  text-start items-start basis-1/4 md:basis-[20%]'>{job.location}</h1>
                        <div className='flex flex-col p-2 font-semibold text-center  text-gray-800 items-center space-y-1 border-2 border-blue-950 rounded-lg basis-1/4 md:basis-[20%]'>
                          <h1 className='text-sm md:text-md lg:text-md text-[#000030] '>{job.company}</h1>
                          <p className='text-gray-500 text-sm md:text-md lg:text-md'>{job.date_posted}</p>
                        </div>
                    </div>
                  </Link>
                ))
              ):null}
          </div>
        </div>
    </div>
  )
}

export default Home

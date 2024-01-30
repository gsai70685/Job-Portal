import React, { useEffect, useState, CSSProperties } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'
import Cookies from 'js-cookie'
import { useAggregateContext } from '../context/AggregateDataContext'
import { useSearchContext } from '../context/currentSearchContext'
import {ClipLoader} from 'react-spinners';
import accenture from '../assets/logo/accenture.png'
import wipro from '../assets/logo/wipro.png'
import apple from '../assets/logo/apple.png'
import infosyslimited from '../assets/logo/infosys.png'
import tcs from '../assets/logo/tcs.png'
import Pagination from '../helper/Pagination'

const Jobs = () => {

    // Here we aee over writing the css for the spinners
    const override = {
    display: "block",
    margin: "0 auto",
    borderColor: "red"}


    // To navigate to different routes if there is some error
    const navigate = useNavigate();
    // This will store the search data of the user
    const [searchData, setSearchData] = React.useState({
        keyword: "",
        location:"",
        filters:[]
    })
    // These are from our context so that we can transfer the data to it and use it later
    // instead of making request again and again
    const {filteredJobs, lastJobID, setFilteredJobs, setLastJobID,
      firstID,  setFIrstID} = useAggregateContext();
    // Here this context will help to store the last search parameters so that we pass only that while getting the future or the last pages
    const {setPrevQuery, prevQuery} = useSearchContext();
    const [searchRequest, setSearchRequest] = useState(null);
    // using this to store the data and update the filtered data accordingly
    const [responseData, setResponseData] = useState(null);
    // using this to store the last job if for the pagination purpose
    const [lastJob, setLastJob] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    // see if there is any change in the input box and than update in the search data object accordingly
    const handleInputChange = (e) =>{
        const {name, value} = e.target;
        setSearchData({
            ...searchData,
            [name]:value
        });
    }

    const handleFilterChange = (e) => {
      const { name, checked } = e.target;
      setSearchData((prevSearchData) => ({
        ...prevSearchData,
        filters: checked
          ? [...prevSearchData.filters, name] // Add filter if checked
          : prevSearchData.filters.filter((filter) => filter !== name), // Remove filter if unchecked
      }));
    };

    // This will keep an eye on the the reponseData so whenever there is a request made and as we get the
    // data it will update the filteredjobdata context
    useEffect(()=>{
        if(searchRequest && responseData && responseData.length > 0){
            setFilteredJobs(responseData);
            setLastJobID(lastJob);
        }
        if(lastJobID && lastJob === ""){
          setLastJobID(null)
        }
    },[responseData])

    // This function willl set the searched query in the context so that we can use them when it is needed
    const setCurrentQuery = ()=>{
      setPrevQuery(searchData);
    }

    const handleFirstJob =(jobvalue) =>{
      if(!firstID || prevQuery !==searchData){
        // console.log(jobvalue["_id"], "this is the value of the first job id")
        setFIrstID(jobvalue["_id"]);
      }
    };

    // whenever the user submits the form this will send the request to the backend and retrieve the data
    const handleFormSubmit = async (e) =>{
        e.preventDefault();
        setIsLoading(true);
        try {
            const response = await axios.post("http://194.135.93.37:8100/jobs/all", searchData, {withCredentials:true});
            // const response = await axios.post("http://127.0.0.1:8000/jobs/all", searchData, {withCredentials:true});
            if(response.data?.jobs){
                setSearchRequest(true)
                setResponseData(response.data.jobs);
                console.log(response.data)
            }
            if(response.data?.jobs && response.data.jobs.length > 0) handleFirstJob(response.data.jobs[0])
            if(response.data?.last_job_id && response.data.jobs.length === 50){
              setLastJob(response.data.last_job_id);
            }else{
              setLastJob(null);
            }

        } catch (error) {
            if(error.response?.status === 400 || error.response?.status === 401){
                Cookies.remove("role");
                navigate('/signin')
            }
            else{
                console.error("Error while scraping the data: ", error);
            }
        }finally{
          setCurrentQuery();
          setIsLoading(false);
        }
    }

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
            return null;
        }
      };

  return (
    <div className='container max-w-[100%] mx-auto flex flex-col p-2 md:p-4 lg:p-4'>
      <div className='container flex flex-col mx-auto w-[90%] items-start text-start'>
        <h1 className='text-md md:text-lg lg:text-lg text-left'><Link to="/" className='text-[#000030]  font-semibold'>Home</Link>&gt; Jobs</h1>
        <h1 className='text-2xl md:text-3xl lg:text-[2.1rem] font-semibold mt-8 md:mt-15'>Jobs</h1>
      </div>
      <div className='container flex flex-col mx-auto p-3 bg-gray-200 mt-8 w-[90%]'>
        <form className='flex flex-col space-y-2 lg:space-y-3 ' onSubmit={handleFormSubmit}>
            <div className='flex justify-between space-x-2'>
              <input type="text"
                  name='keyword'
                  id='keyword'
                  onChange={handleInputChange}
                  placeholder='Keywords'
                  className='w-[48%] p-2 md:p-3 lg:p-3 rounded-md  text-lg md:text-lg lg:text-lg text-gray-800'
                  />
                <input type="text"
                  name='location'
                  id='location'
                  onChange={handleInputChange}
                  placeholder='Location'
                  className='w-[48%] p-2 md:p-3 lg:p-3 rounded-md  text-lg md:text-lg lg:text-lg text-gray-800'
                />
            </div>
                  <button type='submit' className='bg-[#000030] text-white p-2 md:p-3 lg:p-3 text-lg md:text-lg lg:text-lg font-semibold hover:bg-white hover:text-[#000030] border hover:border-blue-950 rounded-md'>Search Jobs</button>
        </form>
      </div>
        <div className='container flex flex-wrap items-center space-x-3 md:space-x-4 lg:space-x-5 mx-auto p-2 bg-gray-100 w-[90%]'>
            <div className="flex items-center space-x-2">
                <input type="checkbox" checked={searchData.filters.includes("freelance")} name="freelance" value="True" id="freelance" className='transform scale-105 md:scale-105 lg:scale-105' onChange={handleFilterChange} />
                <label htmlFor="freelance" className='text-sm md:text-lg lg:text-lg'>Freelance</label>
            </div>

            <div className="flex items-center space-x-2">
                <input type="checkbox" checked={searchData.filters.includes("temporary")} name="temporary" value="True" id="temporary" className='transform scale-105 md:scale-105 lg:scale-105' onChange={handleFilterChange} />
                <label htmlFor="temporary" className='text-sm md:text-lg lg:text-lg'>Temporary</label>
            </div>

            <div className="flex items-center space-x-2">
                <input type="checkbox" checked={searchData.filters.includes("full time")} name="full time" value="True" id="fulltime" className='transform scale-105 md:scale-105 lg:scale-105' onChange={handleFilterChange} />
                <label htmlFor="fulltime" className='text-sm md:text-lg lg:text-lg'>Full-time</label>
            </div>

            <div className="flex items-center space-x-2">
                <input type="checkbox" checked={searchData.filters.includes("internship")} name="internship" value="True" id="internship" className='transform scale-105 md:scale-105 lg:scale-105' onChange={handleFilterChange} />
                <label htmlFor="internship" className='text-sm md:text-lg lg:text-lg'>Internship</label>
            </div>

            <div className="flex items-center space-x-2">
                <input type="checkbox" checked={searchData.filters.includes("part time")} name="part time" value="True" id="parttime" className='transform scale-105 md:scale-105 lg:scale-105' onChange={handleFilterChange} />
                <label htmlFor="parttime" className='text-sm md:text-lg lg:text-lg'>Part-time</label>
            </div>
            <div className="flex items-center space-x-2">
                <input type="checkbox" checked={searchData.filters.includes("others")} name="others" value="True" id="others" className='transform scale-105 md:scale-105 lg:scale-105' onChange={handleFilterChange} />
                <label htmlFor="others" className='text-sm md:text-lg lg:text-lg'>Others</label>
            </div>
        </div>

        <div className='container flex flex-col py-10 w-[90%] mx-auto text-center  items-center justify-between'>
          {isLoading ? (
            <div className='loading-spinner'>
              <ClipLoader css={override} size={80} color={'#123abc'} loading={isLoading}/>
            </div>
          ):null}
            <div className='container flex flex-col space-y-6 mx-auto w-[100%] text-center'>
              {filteredJobs && filteredJobs.length > 0?(
                filteredJobs.map(job =>(
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
              ): searchRequest ? (<p className='text-sm text-gray-600 font-semibold'>No jobs available for the given filter..</p>):null}
            </div>
          <Pagination/>
        </div>
    </div>
  )
}

export default Jobs

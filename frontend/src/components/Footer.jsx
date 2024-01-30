import React from 'react'

const Footer = () => {
  return (
    <div className='conatiner flex flex-col w-[100vw] bg-[#000030] text-white items-start mt-10 px-5 py-3'>
        <div className='conatiner max-w-[100%] flex flex-col'>
            <h1 className='text-lg font-normal'>Be Future Ready</h1>
            <p className='text-gray-500 text-sm'>Get exclusive latest job updates straight to your inbox</p>
            <div className='mt-3'>
                <input type="search" placeholder='Email address' className='px-2 py-2 w-[80%] h-[2.4rem] bg-[#000030] text-gray-500 border border-gray-500 text-sm'/>
                <button className='text-black bg-white rounded-sm items-center w-[20%] h-[2.4rem]'>Go</button>
            </div>
        </div>
        <div className='container mx-auto w-[100%] items-center text-center mt-3'>
            <p className='text-sm'>&copy; 2024 Rivan solutions. All Rights Reserved</p>
        </div>
    </div>
  )
}

export default Footer

import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import JobContextProvider from './context/JobsContext.jsx'
import AccountContextProvider from './context/AccountDataContext.jsx'
import AggregateContextProvider from './context/AggregateDataContext.jsx'
import SearchContextProvider from './context/currentSearchContext.jsx'
import IndividualJobContextProvider from './context/IndividualJobPageContext.jsx'

ReactDOM.createRoot(document.getElementById('root')).render(
  <IndividualJobContextProvider>
    <AccountContextProvider>
      <JobContextProvider>
        <SearchContextProvider>
        <AggregateContextProvider>
          <App />
        </AggregateContextProvider>
        </SearchContextProvider>
      </JobContextProvider>
    </AccountContextProvider>
  </IndividualJobContextProvider>
)

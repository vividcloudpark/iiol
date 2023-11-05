import React from 'react'
import "./AppLayout.scss"
import AppHeader from "./AppHeader"

export default function AppLayout({ children }) {

  return (
    <div className='app'>
        <AppHeader/>
        <div className='contents'>
            { children }

            
        </div>
        <div className='footer'>Cloudpark | 2023</div>
    </div>
  )
}

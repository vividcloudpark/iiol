import React from 'react'
import "./AppLayout.scss"
import AppHeader from "./AppHeader"

export default function AppLayout({ children }) {

  return (
    <div className='app'>
        <AppHeader/>
        <div className='sidebar'>Sidebar</div>
        <div className='contents'>
            { children }

            
        </div>
        <div className='footer'>Footer</div>
    </div>
  )
}

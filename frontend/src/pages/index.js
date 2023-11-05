import React from 'react';
import AppLayout from 'components/AppLayout';


import {  Routes, Route } from "react-router-dom";
import About from "./About.js"
import AccountRoutes from "./accounts"
import Barcode from "./Barcode";


export default function Root() {

  return (
    <AppLayout>
      <Routes>
        <Route path ="/" element={<About/>} />
        <Route path ="/about" element={<About/>} />
        <Route path ="/barcode" element={<Barcode/>} />
        <Route path ={"/accounts/*"} element={<AccountRoutes/>} />
        
        
      </Routes>

  
      
    </AppLayout>
  )
}

import React from 'react'

import Profile from "./Profile"
import Login from "./Login"
import { Routes, Route } from "react-router-dom"


export default function AccountsRoute() {
  return (
    <Routes>
        <Route path="/profile" element={<Profile/>} />
        <Route path="/login" element={<Login/>} />
    </Routes>

  )
}

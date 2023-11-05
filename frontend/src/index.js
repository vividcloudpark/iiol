import React from 'react';
import ReactDOM from 'react-dom/client';

import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
  RouterProvider,
  BrowserRouter,
} from "react-router-dom";
import './index.css';
import Root from "pages";
import About from "pages";







ReactDOM.createRoot(document.getElementById('root')).render(
  <BrowserRouter>
    <Root/>
  </BrowserRouter>
);

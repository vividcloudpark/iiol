import React from 'react';
import ReactDOM from 'react-dom/client';

import {
  BrowserRouter,
} from "react-router-dom";
import './index.css';
import Root from "pages";







ReactDOM.createRoot(document.getElementById('root')).render(
  <BrowserRouter>
    <Root/>
  </BrowserRouter>
);

import React, { useEffect, useState } from 'react';
import Axios from "axios";
import Mybookwish from './Mybookwish';

const apiUrl = "https://thecloudpark.xyz/dev/mybookwishlist/api/mylist/?format=json"


function Mybookwishlist() {
  const [mybookwishList, setMybookwishlist] = useState([]);
  const [mybookwishListGroup, setMybookwishlistGroup] = useState([]);

  useEffect(() => {
    const authenticationToken =  "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk4MDQwMzUxLCJpYXQiOjE2OTgwMzkxNTEsImp0aSI6IjQ1YjEzZjg1ZTI3MjQ5MGI5MTdmZGIxMDdhZDI3MjVlIiwidXNlcl9pZCI6MX0.xKZ7Mk-dLs4zqSmWTFigOGF72Mxz70JQAw4ky4uHRhI";
      
    Axios.get(apiUrl, {
      headers: {
        Authorization: 'Bearer ' + authenticationToken,
      }
    })
    .then(response => {
      console.log("loaded response: ", response);
      setMybookwishlist(response.data.result_data.data);
      setMybookwishlistGroup(response.data.result_data.groupname);
    })
    .catch(error=>{
      console.log("erro", error);
    })

    console.log("mounted!")
    
  }, []);
  


  return (
    
    <div>
      <h2>mybookwishlist</h2>
      <div>
        {mybookwishList.map(mybookwish => {
          
          return (
            <Mybookwish mybookwish={mybookwish} key={mybookwish.isbn13} />
          )
        })}
      </div>
    </div>
    
  )
}


export default Mybookwishlist;
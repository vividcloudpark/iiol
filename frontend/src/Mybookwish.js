import React from 'react'

export default function Mybookwish({mybookwish}) {
    return (
        <div id ={mybookwish.isbn13} className="card mb-2 group-pk-{ mybookwish.groupPk}">

        <div className="card-header">
            
            { mybookwish.groupname }
            
            
            

            <blockquote className="blockquote text-left">
                
                <p>{ mybookwish.book.bookname }</p>


            </blockquote>
        </div>
        </div>
  )
}

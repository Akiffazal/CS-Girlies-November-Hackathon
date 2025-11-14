import React from 'react'
import FileUpload from '../components/FileUpload'

export default function Home(){
  return (
    <div>
      <div className="card" style={{marginBottom:16}}>
        <h2 style={{margin:0}}>Welcome to AskYourBook</h2>
        <p style={{color:'#6b7280'}}>Upload a PDF textbook and ask questions directly from its content.</p>
      </div>
      <FileUpload />
    </div>
  )
}

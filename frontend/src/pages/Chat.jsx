import React from 'react'
import ChatBox from '../components/ChatBox'
import PdfPreview from '../components/PdfPreview'

export default function Chat(){
  // For MVP we won't manage uploaded file state across routes.
  return (
    <div>
      <div className="card" style={{marginBottom:16}}>
        <h3 style={{margin:0}}>AskYourBook — Chat</h3>
        <p style={{color:'#6b7280'}}>Type any question about the indexed book.</p>
      </div>
      <ChatBox />
    </div>
  )
}

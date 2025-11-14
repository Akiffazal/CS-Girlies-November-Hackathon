import React from 'react'

export default function PdfPreview({ filename }){
  if(!filename) return null
  return (
    <div style={{fontSize:13, color:'#374151', marginTop:8}}>Uploaded: <strong>{filename}</strong></div>
  )
}

import React from 'react'

export default function Navbar(){
  return (
    <div className="card header" style={{marginBottom:16}}>
      <div style={{display:'flex', alignItems:'center', gap:12}}>
        <div style={{width:44, height:44, borderRadius:10, background:'#eef2ff', display:'flex', alignItems:'center', justifyContent:'center', fontWeight:700, color:'#4f46e5'}}>AYB</div>
        <div>
          <div style={{fontWeight:700}}>AskYourBook</div>
          <div style={{fontSize:12, color:'#6b7280'}}>Upload a book and ask questions</div>
        </div>
      </div>
      <div>
        <a href="#" target="_blank" rel="noreferrer" style={{fontSize:12, color:'#111827'}}>Repo</a>
      </div>
    </div>
  )
}

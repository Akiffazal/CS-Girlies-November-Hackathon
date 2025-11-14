import React, {useState} from 'react'
import { useUpload } from '../hooks/useApi'
import Loader from './Loader'

export default function FileUpload(){
  const [file, setFile] = useState(null)
  const { upload, loading, message } = useUpload()

  const onUpload = async ()=>{
    if(!file) return alert('Choose a PDF file')
    await upload(file)
  }

  return (
    <div className="card" style={{marginBottom:16}}>
      <div style={{display:'flex', gap:12, alignItems:'center'}}>
        <input className="input" type="file" accept="application/pdf" onChange={e=>setFile(e.target.files[0])} />
        <button className="btn" onClick={onUpload} disabled={loading}>{loading ? <Loader/> : 'Upload & Index'}</button>
      </div>
      <div style={{marginTop:10}}>
        <div style={{fontSize:13, color:'#6b7280'}}>{message}</div>
      </div>
    </div>
  )
}

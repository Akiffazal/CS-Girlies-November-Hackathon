import { useState } from 'react'
import api from '../services/api'

export function useUpload(){
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')

  const upload = async (file) => {
    setLoading(true)
    setMessage('')
    try{
      const fd = new FormData()
      fd.append('file', file)
      const res = await api.post('/upload', fd)
      setMessage(res.data.message || 'Indexed')
    }catch(e){
      console.error(e)
      setMessage('Upload failed')
    }finally{ setLoading(false) }
  }

  return { upload, loading, message }
}

export function useAsk(){
  const [loading, setLoading] = useState(false)
  const ask = async (question) => {
    setLoading(true)
    try{
      const res = await api.post('/ask', { question, top_k: 4 })
      return res.data
    }catch(e){
      console.error(e)
      return { answer: 'Error: could not fetch answer.', citations: [] }
    }finally{ setLoading(false) }
  }
  return { ask, loading }
}

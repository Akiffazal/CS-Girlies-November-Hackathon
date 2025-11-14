import React, {useState} from 'react'
import { useAsk } from '../hooks/useApi'
import Loader from './Loader'
import { shortText } from '../utils/helpers'

export default function ChatBox(){
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState([])
  const { ask, loading } = useAsk()

  const onAsk = async () =>{
    if(!question) return
    const userMsg = { type:'user', text: question }
    setMessages(prev => [...prev, userMsg])
    setQuestion('')
    const res = await ask(question)
    const botMsg = { type:'bot', text: res.answer, citations: res.citations || [] }
    setMessages(prev => [...prev, botMsg])
  }

  return (
    <div className="card">
      <div style={{marginBottom:12}}>
        <input className="input" placeholder="Ask a question about the uploaded book" value={question} onChange={e=>setQuestion(e.target.value)} style={{width:'70%'}} />
        <button className="btn" onClick={onAsk} style={{marginLeft:10}} disabled={loading}>{loading ? <Loader/> : 'Ask'}</button>
      </div>

      <div style={{marginTop:8}}>
        {messages.map((m,i)=> (
          <div key={i} className="chat-message" style={{background: m.type==='user' ? '#eef2ff' : '#f1f5f9'}}>
            <div style={{fontSize:12, fontWeight:600}}>{m.type==='user' ? 'You' : 'AskYourBook'}</div>
            <div style={{marginTop:6}}>{m.text}</div>
            {m.citations && m.citations.length>0 && (
              <div style={{marginTop:6}}>
                {m.citations.map((c,ci)=> (
                  <div key={ci} className="citation">Citation: page {c.page} — {shortText(c.text,120)}</div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

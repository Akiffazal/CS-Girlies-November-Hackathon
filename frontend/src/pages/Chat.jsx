// src/pages/Chat.jsx
import React, { useState, useRef, useEffect } from 'react'
import { useAsk } from '../hooks/useApi'
import Loader from '../components/Loader'

export default function Chat() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const { ask, loading: askLoading } = useAsk()
  const messagesEndRef = useRef(null)
  const [loading, setLoading] = useState(false)

  // Scroll to bottom whenever messages update
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!input.trim()) return

    // Add user message
    const newMessage = { role: 'user', content: input }
    setMessages((prev) => [...prev, newMessage])
    setInput('')

    setLoading(true)
    try {
      const res = await ask(input)
      const botMessage = { role: 'bot', content: res.answer }
      setMessages((prev) => [...prev, botMessage])
    } catch (err) {
      console.error(err)
      const errorMessage = { role: 'bot', content: 'Something went wrong!' }
      setMessages((prev) => [...prev, errorMessage])
    }
    setLoading(false)
  }

  // Format content with proper markdown-like rendering
  const formatContent = (text) => {
    return text
      .replace(/<br\s*\/?>/g, '\n')
      .replace(/\|[-\s|]+\|/g, '')
      .replace(/^\s*\|\s*/gm, '')
      .replace(/\s*\|\s*$/gm, '')
      .replace(/\n{3,}/g, '\n\n')
      .trim()
  }

  const renderMessage = (content) => {
    const formatted = formatContent(content)
    const parts = []
    const lines = formatted.split('\n')
    
    lines.forEach((line, idx) => {
      // Numbered lists
      if (/^\d+\.\s/.test(line)) {
        parts.push(<div key={idx} style={{marginLeft: '8px', marginTop: '4px'}}>{line}</div>)
      }
      // Bullet points
      else if (/^[•\-*]\s/.test(line)) {
        parts.push(<div key={idx} style={{marginLeft: '8px', marginTop: '4px'}}>• {line.replace(/^[•\-*]\s/, '')}</div>)
      }
      // Headers (lines ending with :)
      else if (line.endsWith(':') && line.length < 80) {
        parts.push(<div key={idx} style={{fontWeight: '600', marginTop: '12px', marginBottom: '4px', color: '#1e293b'}}>{line}</div>)
      }
      // Regular text
      else if (line.trim()) {
        // Handle bold text **text**
        const boldProcessed = line.split(/\*\*([^*]+)\*\*/g).map((part, i) => 
          i % 2 === 1 ? <strong key={i}>{part}</strong> : part
        )
        parts.push(<div key={idx} style={{marginTop: '4px'}}>{boldProcessed}</div>)
      }
      // Empty line for spacing
      else {
        parts.push(<div key={idx} style={{height: '8px'}} />)
      }
    })
    
    return parts
  }

  return (
    <div className="card" style={{display:'flex', flexDirection:'column', height:'500px', marginTop: '16px'}}>
      <h3 style={{margin: '0 0 16px 0', fontSize: '18px', fontWeight: '600', color: '#1e293b'}}>Chat</h3>
      {/* Messages */}
      <div style={{flex:1, overflowY:'auto', marginBottom:'12px', display: 'flex', flexDirection: 'column', gap: '4px'}}>
        {messages.length === 0 && (
          <div style={{textAlign: 'center', color: '#94a3b8', marginTop: '40px', fontSize: '14px'}}>
            Ask a question about your uploaded document...
          </div>
        )}
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={msg.role === 'user' ? 'chat-message chat-user' : 'chat-message chat-bot'}
            style={{
              lineHeight: '1.7', 
              fontSize: '14px',
              wordWrap: 'break-word'
            }}
          >
            {msg.role === 'user' ? msg.content : renderMessage(msg.content)}
          </div>
        ))}
        {loading && (
          <div className="chat-message chat-bot" style={{display: 'flex', alignItems: 'center', gap: '8px'}}>
            <Loader size={16} /> Thinking...
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} style={{display:'flex', gap:'10px', borderTop: '1px solid #e2e8f0', paddingTop: '12px'}}>
        <input
          type="text"
          className="input"
          style={{flex:1, fontSize: '14px', padding: '12px 14px'}}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question about your document..."
          disabled={loading}
        />
        <button
          type="submit"
          className="btn"
          disabled={loading || !input.trim()}
          style={{minWidth: '80px', fontWeight: '500', opacity: (loading || !input.trim()) ? 0.5 : 1}}
        >
          {loading ? <Loader size={16} /> : 'Send'}
        </button>
      </form>
    </div>
  )
}

import React from 'react'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Chat from './pages/Chat'

export default function App() {
  return (
    <div className="container">
      <Navbar />
      <Home />
      <Chat />
    </div>
  )
}

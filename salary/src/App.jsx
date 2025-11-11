import { useState } from 'react'
import './App.css'
import Start from './Start'
import Submitted from './Submitted'

function App() {
  const [count] = useState(0)

  // Simple path-based rendering: if path is /start render Start page
  const path = typeof window !== 'undefined' ? window.location.pathname : '/'
  if (path === '/start' || path.startsWith('/start')) {
    return <Start />
  }

  if (path === '/submitted' || path.startsWith('/submitted')) {
    return <Submitted />
  }

  return (
    <main className="hero">
      <div className="hero-inner">
        <h1 className="hero-title">Your Personal Salary Assistant</h1>
        {/* use an anchor so clicking navigates to /start (will reload index and render Start) */}
        <a className="cta" href="/start">Get started</a>
      </div>
    </main>
  )
}

export default App

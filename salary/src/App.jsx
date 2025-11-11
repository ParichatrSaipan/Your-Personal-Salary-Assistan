import { useState } from 'react'
import './App.css'

function App() {
  const [count] = useState(0)

  return (
    <main className="hero">
      <div className="hero-inner">
        <h1 className="hero-title">Your Personal Salary Assistant</h1>
        <button className="cta">Get started</button>
      </div>
    </main>
  )
}

export default App

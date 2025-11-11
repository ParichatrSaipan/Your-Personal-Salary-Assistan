import './App.css'

export default function Start() {
  return (
    <main className="hero start-hero">
      <div className="hero-inner">
        <h1 className="hero-title">Welcome — Start Page</h1>
        <p style={{color: 'rgba(255,255,255,0.95)'}}>This is the new page that opens when you click Get started.</p>
        <a className="cta" href="/">Go back</a>
      </div>
    </main>
  )
}

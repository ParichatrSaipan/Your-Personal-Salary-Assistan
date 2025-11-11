import './App.css'

export default function Submitted() {
  // static example value for now; we can populate this from state or props later
  const amount = '45,000'
  const unit = 'USD/YEAR'

  return (
  <main className="hero start-hero submitted-hero">
      <div className="hero-inner">
        <h1 className="hero-title">Your Personal Salary Assistant</h1>

        <div className="result-panel">
          <h2 className="result-title">Predicted annual salary</h2>

          <div className="result-amount">{amount}</div>
          <div className="result-currency">{unit}</div>

        </div>
      </div>
    </main>
  )
}

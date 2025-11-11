import './App.css'

export default function Start() {
  function handleBack() {
    // go back to previous page
    if (typeof window !== 'undefined') window.history.back()
  }

  function handleNext() {
    // For now just navigate to /submitted. In future we can validate and post data.
    if (typeof window !== 'undefined') window.location.pathname = '/submitted'
  }

  return (
    <main className="hero start-hero">
      <div className="hero-inner">
        <h1 className="hero-title">Your Personal Salary Assistant</h1>
        <div className="panel">

          <label className="field-label">Job title or position name</label>
          <input className="text-input"/>

          <label className="field-label">Level of experience</label>
          <input className="text-input"/>

          <label className="field-label">Required years of work experience</label>
          <input className="text-input"/>

          <label className="field-label">Type of employment</label>
          <input className="text-input"/>

          <label className="field-label">Proportion of remote work</label>
          <input className="text-input" />

          <label className="field-label">Company size</label>
          <input className="text-input" />

          <label className="field-label">Country where the company is located</label>
          <input className="text-input" />

          <label className="field-label">Industry sector of the company</label>
          <input className="text-input" />
          
          <label className="field-label">Required education level</label>
          <input className="text-input" />


          <div className="panel-actions">
            <button className="btn btn-back" type="button" onClick={handleBack}>Back</button>
            <button className="btn btn-next" type="button" onClick={handleNext}>Submit</button>
          </div>
        </div>
      </div>
    </main>
  )
}

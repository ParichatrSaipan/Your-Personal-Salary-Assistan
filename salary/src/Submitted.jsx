import './App.css'
import { useState, useEffect } from 'react'

export default function Submitted() {
  const [predictionData, setPredictionData] = useState(null)

  useEffect(() => {
    // Retrieve prediction data from sessionStorage
    const storedData = sessionStorage.getItem('salaryPrediction')
    if (storedData) {
      const data = JSON.parse(storedData)
      setPredictionData(data)
    }
  }, [])

  // Format number with commas
  const formatSalary = (num) => {
    return new Intl.NumberFormat('en-US', {
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(num)
  }

  const amount = predictionData
    ? formatSalary(predictionData.predictedSalary)
    : '45,000'
  const unit = predictionData?.currency
    ? `${predictionData.currency}/${predictionData.period.toUpperCase()}`
    : 'USD/YEAR'

  return (
    <main className="hero start-hero submitted-hero">
      <div className="hero-inner">
        <h1 className="hero-title">Your Personal Salary Assistant</h1>

        <div className="result-panel" style={{
          margin: '2rem auto',
          display: 'block'
        }}>
          <h2 className="result-title">Predicted annual salary</h2>

          <div className="result-amount">{amount}</div>
          <div className="result-currency">{unit}</div>

          {/* {predictionData && predictionData.input && (
            <div style={{
              marginTop: '2rem',
              padding: '1rem',
              background: '#f5f5f5',
              borderRadius: '8px',
              textAlign: 'left',
              fontSize: '0.9rem'
            }}>
              <h3 style={{ marginTop: 0 }}>Based on your inputs:</h3>
              <ul style={{ listStyle: 'none', padding: 0 }}>
                <li><strong>Job Title:</strong> {predictionData.input.jobTitle}</li>
                <li><strong>Experience Level:</strong> {predictionData.input.experienceLevel}</li>
                <li><strong>Years of Experience:</strong> {predictionData.input.yearsExperience}</li>
                <li><strong>Employment Type:</strong> {predictionData.input.employmentType}</li>
                <li><strong>Remote Work:</strong> {predictionData.input.remoteWork}%</li>
                <li><strong>Company Size:</strong> {predictionData.input.companySize}</li>
                <li><strong>Country:</strong> {predictionData.input.country}</li>
                <li><strong>Industry:</strong> {predictionData.input.industry}</li>
                <li><strong>Education:</strong> {predictionData.input.education}</li>
              </ul>
            </div>
          )} */}

        </div>

        <div style={{
          display: 'flex',
          justifyContent: 'center',
          marginTop: '2rem'
        }}>
          <a href="/start" className="btn btn-back">Try Again</a>
        </div>
      </div>
    </main>
  )
}

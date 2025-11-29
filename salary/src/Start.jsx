import './App.css'
import { useState } from 'react'

export default function Start() {
  const [formData, setFormData] = useState({
    jobTitle: '',
    experienceLevel: '',
    yearsExperience: '',
    employmentType: '',
    remoteWork: '',
    companySize: '',
    country: '',
    industry: '',
    education: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  function handleBack() {
    // go back to previous page
    if (typeof window !== 'undefined') window.history.back()
  }

  function handleChange(e) {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
    setError('')
  }

  async function handleNext() {
    // Validate all fields are filled
    const emptyFields = Object.entries(formData)
      .filter(([_, value]) => !value)
      .map(([key, _]) => key)

    if (emptyFields.length > 0) {
      setError('Please fill in all fields before submitting')
      return
    }

    setLoading(true)
    setError('')

    try {
      // Call the API (relative path works since frontend and backend are on same domain)
      const response = await fetch('/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      })

      const data = await response.json()

      if (data.success) {
        // Store the prediction result in sessionStorage
        sessionStorage.setItem('salaryPrediction', JSON.stringify(data))
        // Navigate to submitted page
        if (typeof window !== 'undefined') window.location.pathname = '/submitted'
      } else {
        setError(data.error || 'Failed to get prediction')
      }
    } catch (err) {
      setError('Failed to connect to server. Make sure the backend is running.')
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="hero start-hero">
      <div className="hero-inner">
        <h1 className="hero-title">Your Personal Salary Assistant</h1>
        <div className="panel">

          <label className="field-label">Job title or position name</label>
          <select className="text-input" name="jobTitle" value={formData.jobTitle} onChange={handleChange}>
            <option value="">Select a job title</option>
            <option value="AI Architect">AI Architect</option>
            <option value="AI Consultant">AI Consultant</option>
            <option value="AI Product Manager">AI Product Manager</option>
            <option value="AI Research Scientist">AI Research Scientist</option>
            <option value="AI Software Engineer">AI Software Engineer</option>
            <option value="AI Specialist">AI Specialist</option>
            <option value="Autonomous Systems Engineer">Autonomous Systems Engineer</option>
            <option value="Computer Vision Engineer">Computer Vision Engineer</option>
            <option value="Data Analyst">Data Analyst</option>
            <option value="Data Engineer">Data Engineer</option>
            <option value="Data Scientist">Data Scientist</option>
            <option value="Deep Learning Engineer">Deep Learning Engineer</option>
            <option value="Head of AI">Head of AI</option>
            <option value="ML Ops Engineer">ML Ops Engineer</option>
            <option value="Machine Learning Engineer">Machine Learning Engineer</option>
            <option value="Machine Learning Researcher">Machine Learning Researcher</option>
            <option value="NLP Engineer">NLP Engineer</option>
            <option value="Principal Data Scientist">Principal Data Scientist</option>
            <option value="Research Scientist">Research Scientist</option>
            <option value="Robotics Engineer">Robotics Engineer</option>
          </select>

          <label className="field-label">Level of experience</label>
          <select className="text-input" name="experienceLevel" value={formData.experienceLevel} onChange={handleChange}>
            <option value="">Select experience level</option>
            <option value="EN">Entry Level (EN)</option>
            <option value="MI">Mid Level (MI)</option>
            <option value="SE">Senior (SE)</option>
            <option value="EX">Executive (EX)</option>
          </select>

          <label className="field-label">Required years of work experience</label>
          <select className="text-input" name="yearsExperience" value={formData.yearsExperience} onChange={handleChange}>
            <option value="">Select years of experience</option>
            <option value="0-1">0-1 years</option>
            <option value="1-3">1-3 years</option>
            <option value="3-5">3-5 years</option>
            <option value="5-7">5-7 years</option>
            <option value="7-10">7-10 years</option>
            <option value="10+">10+ years</option>
          </select>

          <label className="field-label">Type of employment</label>
          <select className="text-input" name="employmentType" value={formData.employmentType} onChange={handleChange}>
            <option value="">Select employment type</option>
            <option value="FT">Full Time (FT)</option>
            <option value="PT">Part Time (PT)</option>
            <option value="CT">Contract (CT)</option>
            <option value="FL">Freelance (FL)</option>
          </select>

          <label className="field-label">Proportion of remote work</label>
          <select className="text-input" name="remoteWork" value={formData.remoteWork} onChange={handleChange}>
            <option value="">Select remote work proportion</option>
            <option value="0">0% (On-site)</option>
            <option value="50">50% (Hybrid)</option>
            <option value="100">100% (Remote)</option>
          </select>

          <label className="field-label">Company size</label>
          <select className="text-input" name="companySize" value={formData.companySize} onChange={handleChange}>
            <option value="">Select company size</option>
            <option value="S">Small - less than 50 employees (S)</option>
            <option value="M">Medium - 50-250 employees (M)</option>
            <option value="L">Large - more than 250 employees (L)</option>
          </select>

          <label className="field-label">Country where the company is located</label>
          <select className="text-input" name="country" value={formData.country} onChange={handleChange}>
            <option value="">Select a country</option>
            <option value="Australia">Australia</option>
            <option value="Austria">Austria</option>
            <option value="Canada">Canada</option>
            <option value="China">China</option>
            <option value="Denmark">Denmark</option>
            <option value="Finland">Finland</option>
            <option value="France">France</option>
            <option value="Germany">Germany</option>
            <option value="India">India</option>
            <option value="Ireland">Ireland</option>
            <option value="Israel">Israel</option>
            <option value="Japan">Japan</option>
            <option value="Netherlands">Netherlands</option>
            <option value="Norway">Norway</option>
            <option value="Singapore">Singapore</option>
            <option value="South Korea">South Korea</option>
            <option value="Sweden">Sweden</option>
            <option value="Switzerland">Switzerland</option>
            <option value="United Kingdom">United Kingdom</option>
            <option value="United States">United States</option>
          </select>

          <label className="field-label">Industry sector of the company</label>
          <select className="text-input" name="industry" value={formData.industry} onChange={handleChange}>
            <option value="">Select an industry</option>
            <option value="Automotive">Automotive</option>
            <option value="Consulting">Consulting</option>
            <option value="Education">Education</option>
            <option value="Energy">Energy</option>
            <option value="Finance">Finance</option>
            <option value="Gaming">Gaming</option>
            <option value="Government">Government</option>
            <option value="Healthcare">Healthcare</option>
            <option value="Manufacturing">Manufacturing</option>
            <option value="Media">Media</option>
            <option value="Real Estate">Real Estate</option>
            <option value="Retail">Retail</option>
            <option value="Technology">Technology</option>
            <option value="Telecommunications">Telecommunications</option>
            <option value="Transportation">Transportation</option>
          </select>

          <label className="field-label">Required education level</label>
          <select className="text-input" name="education" value={formData.education} onChange={handleChange}>
            <option value="">Select education level</option>
            <option value="High School">High School</option>
            <option value="Bachelor">Bachelor's Degree</option>
            <option value="Master">Master's Degree</option>
            <option value="PhD">PhD</option>
          </select>

          {error && <div style={{ color: 'red', marginTop: '1rem' }}>{error}</div>}

          <div className="panel-actions">
            <button className="btn btn-back" type="button" onClick={handleBack}>Back</button>
            <button className="btn btn-next" type="button" onClick={handleNext} disabled={loading}>
              {loading ? 'Processing...' : 'Submit'}
            </button>
          </div>
        </div>
      </div>
    </main>
  )
}

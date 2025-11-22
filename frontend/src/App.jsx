import { useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setAnswer('')

    try {
      // Send the question to our FastAPI backend
      const response = await axios.post('http://127.0.0.1:8000/ask', {
        question: question
      })
      
      // Update the state with the answer from the AI
      setAnswer(response.data.answer)
    } catch (error) {
      console.error("Error fetching answer:", error)
      setAnswer("Sorry, something went wrong. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <header>
        <h1>🎓 AI Course Advisor</h1>
        <p>University of Melbourne • Computer Science</p>
      </header>

      <main>
        <form onSubmit={handleSubmit} className="search-box">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask about a subject (e.g., 'What is COMP10001?')"
            disabled={loading}
          />
          <button type="submit" disabled={loading || !question}>
            {loading ? 'Thinking...' : 'Ask AI'}
          </button>
        </form>

        {answer && (
          <div className="result-card">
            <h3>AI Answer:</h3>
            <p>{answer}</p>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
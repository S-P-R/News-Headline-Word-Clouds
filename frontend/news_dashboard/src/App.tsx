import { useEffect, useState } from 'react'
import './styles/App.css'
import WordCloud from './components/WordCloud'
import FilterMenu from './components/FilterMenu'

  

function App() {
  const [wordFreqs, setWordFreqs] = useState([]);

  return (
    <div>
    <p> News Headline Dashboard </p>
    <FilterMenu setWordFreqs={setWordFreqs}/>
    {<WordCloud words={wordFreqs}/>}
    </div>
  )
}


export default App

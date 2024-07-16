import './styles/App.css'
import { useState } from 'react'
import { createTheme, ThemeProvider } from '@mui/material/styles';

import WordCloud from './components/WordCloud'
import FilterMenu from './components/FilterMenu'
import Navbar from './components/NavBar';

const theme = createTheme({
  palette: {
    primary: {
      main: '#800020', 
    },
  },
  typography: {
    fontFamily: 'Times New Roman',
  }
});

function App() {
  const [wordFreqs, setWordFreqs] = useState([]);
  return (
    <ThemeProvider theme={theme}>
      <Navbar/>
      <div className='content'>
        <FilterMenu setWordFreqs={setWordFreqs}/>
        <WordCloud words={wordFreqs}/>
      </div>
    </ThemeProvider>
  )
}


export default App

import './styles/App.css'
import { useState, useContext } from 'react'
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { WordCount } from './types.tsx'


import WordCloud from './components/WordCloud'
import FilterMenu from './components/FilterMenu'
import Navbar from './components/NavBar';
import ErrorDisplay from './components/ErrorDisplay.tsx';
import { ErrorProvider, ErrorContext } from './contexts/ErrorContext.tsx'

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
  const [wordFreqs, setWordFreqs] = useState<WordCount []>([]);
  const { errors } = useContext(ErrorContext);

  let mainContent = <div className='content working-content'>
                      <FilterMenu setWordFreqs={setWordFreqs}/>
                      <WordCloud words={wordFreqs}/>
                    </div>
  
  if (errors.length > 0){
   mainContent = <div className='content error-content'> <ErrorDisplay/> </div>
  }

  return (
    <ThemeProvider theme={theme}>
        <Navbar/>
        {mainContent}
    </ThemeProvider>
  )
}


export default App

import '../styles/FilterMenu.css'
import { useEffect, useState, useContext } from 'react'
import Button from '@mui/material/Button'
import SourcePicker from './SourcePicker'
import DateRangePicker from './DateRangePicker'
import { ErrorContext } from '../contexts/ErrorContext';
import { Dayjs } from 'dayjs'
import { WordCount } from '../types.tsx'
import stopwords_list from '../utils/stopwords.tsx'

/* List of words that will not be used to create the wordcloud  */
let stopwords = new Set<string> (stopwords_list)

interface FilterMenuProps {
    setWordFreqs: React.Dispatch<React.SetStateAction<WordCount []>>
}

/**
 * FilterMenu
 * 
 * Allows user to filter the headlines that are used to create the word cloud
 * and handles retrieving headlines that match these filters from the API
 *
 */
const FilterMenu = ({setWordFreqs} :  FilterMenuProps) => {    
    const { errors, setErrors } = useContext(ErrorContext);
  
    const [gotSources, setGotSources] = useState<boolean>(false)
    const [selectedSources, setSelectedSources] = useState<string[]>([])
    const [gotDates, setGotDates] = useState<boolean>(false)
    const [startDate, setStartDate] = useState<Dayjs | null>(null)
    const [endDate, setEndDate] = useState<Dayjs | null>(null)
    
    /* 
     * Retrieves headlines from the API and counts the frequency of each
     * non-stopword word that appears in these headlines 
     */
    async function getWordFreqs(sourcesToFetch : string []) {
        try {
            let URL = `${import.meta.env.VITE_API_URL}/api/headlines?$filter=(`
            for (let i = 0; i < sourcesToFetch.length; i++){
                URL += "source eq '" + sourcesToFetch[i] + "'"
                if (i != sourcesToFetch.length - 1){
                    URL += ' or '
                }
            }

            URL += ") and date ge '" + startDate?.format('YYYY-MM-DD') + "'"
            URL += "and date le '" + endDate?.format('YYYY-MM-DD') + "'"
            const response = await fetch(URL); 
            const data = await response.json();
            if (data.length == 0){
                throw new Error("No Headlines")
            }

            let wordFreqs = new Map<string, number>();
            for (const headlineInfo of data){
                let headlineWords = headlineInfo.text.split(' ')
                for (let word of headlineWords){
                    word = word.replace(/^[^\w\s]+|[^\w\s]+$/g, '') /* remove leading & trailing punctuation */
                    if (word.length > 2 && !stopwords.has(word.toLowerCase())){
                    if (wordFreqs.has(word)) {
                        wordFreqs.set(word, wordFreqs.get(word)! + 1);
                    } else {
                        wordFreqs.set(word, 1);
                    }
                    }
                }
            }

            /* Only display most frequently occuring words */
            let toDisplay: WordCount[] = Array.from(wordFreqs.entries(), ([word, count]) => ({ word, count }))
            toDisplay.sort((a, b) => b.count - a.count);
            toDisplay = toDisplay.slice(0, 400)
            setWordFreqs(toDisplay)
      } catch (e) {
            if (e.message == "Failed to fetch"){
            setErrors([...errors, `The /headlines route of the news headline API
                                    used by this page couldn't be reached`])
            } else if (e.message == "No Headlines"){
            setErrors([...errors, `No headlines match the given filters`])
            } else {
            setErrors([...errors, `A problem occured when retrieving the headlines 
                                    used to build the wordcloud from the API`])
            } 
      }
    }

      /* 
       * Generate initial wordcloud after all necessary values have been 
       * initialized. Afterwards, wordclouds will only be generated when the 
       * user clicks the 'Generate' button 
       * */
    useEffect(() => {
        if (gotSources && gotDates){
            getWordFreqs(selectedSources)
        }
    }, [gotSources, gotDates]);


    return (
        <div className='filter-menu'>
            <DateRangePicker startDate={startDate} setStartDate={setStartDate} 
                             endDate={endDate} setEndDate={setEndDate} setGotDates={setGotDates} />
            <SourcePicker selectedSources={selectedSources} setSelectedSources={setSelectedSources} 
                          setGotSources={setGotSources} />
            <Button variant='contained' onClick={() => {getWordFreqs(selectedSources)}} 
                    disabled={selectedSources.length == 0 || !startDate || !endDate || startDate > endDate}>
            Generate Wordcloud
            </Button>
        </div>
    )
}

export default FilterMenu;
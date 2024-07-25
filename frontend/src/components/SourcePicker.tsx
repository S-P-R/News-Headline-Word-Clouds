import { useEffect, useState, useContext } from 'react'
import FormControl from '@mui/material/FormControl'
import FormGroup from '@mui/material/FormGroup'
import FormControlLabel from '@mui/material/FormControlLabel'
import Checkbox from '@mui/material/Checkbox'
import { ErrorContext } from '../contexts/ErrorContext';

interface SourcePickerProps {
    selectedSources: string []
    setSelectedSources: React.Dispatch<React.SetStateAction<string []>>
    setGotSources:  React.Dispatch<React.SetStateAction<boolean>>
  }

/**
 * SourcePicker
 * 
 * Allows user to specify the set of sources headlines used to create the 
 * wordcloud must come from 
 *
 */
const SourcePicker = ({selectedSources, setSelectedSources, setGotSources} :  SourcePickerProps) => {    
    const [sources, setSources] = useState([])
    const { errors, setErrors } = useContext(ErrorContext);

    useEffect(() => {
        async function setUp() {
        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/api/sources`); 
            if (!response.ok){
                throw new Error()
            }
            const data = await response.json();
            
            const source_names = data.map((source_info : any) => source_info.name)
            setSources(source_names)
            setSelectedSources(source_names)
        } catch (e) {
            if (e.message == "Failed to fetch"){
                setErrors([...errors, `The /sources route of the news headline API used
                                        by this page couldn't be reached`])
            } else {
                setErrors([...errors, `A problem occured when retrieving the sources that 
                                        can be filtered on from the API`])
            } 
        }
        }
      setUp()
    }, []);

    /* Guarantee that gotSources is only set to true after selectedSources has been initialized */
    useEffect(() => {
        if (selectedSources.length != 0){
            setGotSources(true)
        }
    }, [selectedSources])

    const handleSourceChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.checked){
            setSelectedSources([...selectedSources, event.target.value])
        } else {
            setSelectedSources(selectedSources.filter((s : string) => s !== event.target.value))
        }
    };
    
    return (
        <FormControl
            required={true}
            component="fieldset"
            sx={{ m: 3 }}
            variant="standard"
            >
            <FormGroup>
                {sources.map((source)=> {
                    return <FormControlLabel control={<Checkbox defaultChecked value={source}
                                                                onChange={handleSourceChange}/>} 
                                             key={source} label={source}/>
                })}
            </FormGroup>
      </FormControl>
    )
}

export default SourcePicker;
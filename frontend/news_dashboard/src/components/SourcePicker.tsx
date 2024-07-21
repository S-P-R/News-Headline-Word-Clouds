import { useEffect, useState } from 'react'
import FormLabel from '@mui/material/FormLabel'
import FormControl from '@mui/material/FormControl'
import FormGroup from '@mui/material/FormGroup'
import FormControlLabel from '@mui/material/FormControlLabel'
import Checkbox from '@mui/material/Checkbox'

interface SourcePickerProps {
    selectedSources: string []
    setSelectedSources: React.Dispatch<React.SetStateAction<string []>> /* TODO: change to actual type */
    setGotSources:  React.Dispatch<React.SetStateAction<boolean>>
  }

const SourcePicker = ({selectedSources, setSelectedSources, setGotSources} :  SourcePickerProps) => {    
    const [sources, setSources] = useState([])

    useEffect(() => {
      async function setUp() {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/api/sources`); 
        const data = await response.json();
        const source_names = data.map((source_info : any) => source_info.name)
        setSources(source_names)
        setSelectedSources(source_names)
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
              return <FormControlLabel control={<Checkbox  defaultChecked value={source} onChange={handleSourceChange}/>} 
                                       key={source} label={source}/>
            })}
            </FormGroup>
      </FormControl>
    )
}

export default SourcePicker;
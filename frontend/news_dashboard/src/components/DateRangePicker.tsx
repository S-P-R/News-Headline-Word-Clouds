import { useEffect, useState } from 'react'
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import { DatePicker } from '@mui/x-date-pickers';
import dayjs from 'dayjs';
import { Dayjs } from 'dayjs'
import utc from 'dayjs/plugin/utc';

dayjs.extend(utc)

interface DateRangePickerProps {
  startDate: Dayjs
  setStartDate: React.Dispatch<React.SetStateAction<Dayjs>>
  endDate: Dayjs
  setEndDate: React.Dispatch<React.SetStateAction<Dayjs>>
  setGotDates: React.Dispatch<React.SetStateAction<boolean>>
}

const DateRangePicker = ({startDate, setStartDate, endDate, setEndDate, setGotDates} : DateRangePickerProps) => {    
  const [dates, setDates] = useState(new Set()) /* dates with headlines associated with them */

  /* Convert dates to standard format */
  const formatDate = (date: Dayjs) => {return dayjs(date).utc().format('YYYY-MM-DD')}

  useEffect(() => {
    async function setUp() {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/dates?$orderby=date desc`); 
      const data = await response.json();
      const dateSet = new Set(data.map((dateInfo : any) => formatDate(dateInfo.date)))
      setDates(dateSet)

      setStartDate(dayjs(formatDate(data[0].date)))
      setEndDate(dayjs(formatDate(data[0].date)))
    }
    setUp()
  }, []);

  /* 
   * Guarantee that gotDates is only set to true after startDate and 
   * endDate have been initialized 
   */
  useEffect(() => {
    if (startDate && endDate){
      setGotDates(true)
    }
  }, [startDate, endDate]);
  

  const disableDates = (day: Dayjs) => {
    return !dates.has(formatDate(day))
  }

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs} >
      {/* TODO: switch to mobile date picker on small screen size */}
      <p>Start Date</p>
      <DatePicker shouldDisableDate={disableDates} value={startDate} onChange={(newValue) => setStartDate(newValue)}/>
      <p>End Date</p>
      <DatePicker shouldDisableDate={disableDates} value={endDate} onChange={(newValue) => setEndDate(newValue)}/>

    
    </LocalizationProvider>
  )
}

export default DateRangePicker;
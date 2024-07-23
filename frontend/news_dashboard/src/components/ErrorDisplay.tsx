import '../styles/ErrorDisplay.css'
import { useContext } from 'react';
import { ErrorContext } from '../contexts/ErrorContext';

const ErrorDisplay = () => {
    const { errors } = useContext(ErrorContext);
    return (
        <div className='error-display'> 
            <h3>Something went wrong &#128532;:</h3>
            {errors.map((e : string) => <p key={e}>{e}</p>)}
            <img className="error-image" src={'/elmo_fire.jpg'} alt="Comedic image of Elmo in flames"/>
        </div>
    )
}

export default ErrorDisplay
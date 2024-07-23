import { createContext, useState, ReactNode } from 'react';

type errorInfo = {
    errors: string[]
    setErrors: React.Dispatch<React.SetStateAction<string []>>
}

/* setErrors is initialized with a dummy value. Actual value is set by ErrorProvider */
const ErrorContext = createContext<errorInfo>({errors: [], setErrors: () => {}});

/**
 * ErrorProvider
 * 
 * Simplifies the tracking of errors experienced by child components 
 *
 */
const ErrorProvider = ({ children } : { children: ReactNode }) => {
    const [errors, setErrors] = useState<string []> ([])

    return (
        <ErrorContext.Provider value={{errors, setErrors}}>
            {children}
        </ErrorContext.Provider>
    )
}

export {
    ErrorProvider,
    ErrorContext,
}
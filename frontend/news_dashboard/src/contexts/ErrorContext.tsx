import { createContext, useState, useEffect, ReactNode } from 'react';

type errorInfo = {
    errors: string[]
    // setErrors: React.Dispatch<React.SetStateAction<string []>>
    setErrors: any
}

const ErrorContext = createContext<errorInfo>({errors: [], setErrors: () => {}});


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
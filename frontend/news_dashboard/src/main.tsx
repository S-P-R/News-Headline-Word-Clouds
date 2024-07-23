import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import { ErrorProvider } from './contexts/ErrorContext.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
    <ErrorProvider>
        <App/>
    </ErrorProvider>
)
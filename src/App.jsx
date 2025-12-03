import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { Dropdown } from 'primereact/dropdown';


function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <input type='search' className='search-bar'/>
    </>
  )
}

export default App

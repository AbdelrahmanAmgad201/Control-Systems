import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import ChsEqn from './ChsEqn/ChsEqn'
function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <ChsEqn></ChsEqn>
      
    </>
  )
}

export default App

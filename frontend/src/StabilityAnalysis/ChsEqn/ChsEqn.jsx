import { useState } from 'react';
import './ChsEqn.css';

function ChsEqn() {
  const [order, setOrder] = useState(1);
  const [coefficients, setCoefficients] = useState({});
  const [savedValues, setSavedValues] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleOrderChange = (e) => {
    const newOrder = Math.max(0, parseInt(e.target.value));
    setOrder(newOrder);
  };

  const handleCoefficientChange = (index, value) => {
    setCoefficients(prev => ({
      ...prev,
      [index]: value
    }));
  };

  

  const solveEquation = async () => {
   
    const values = Array.from({ length: order + 1 }, (_, i) => 
      parseFloat(coefficients[i]) || 0
    );
    setSavedValues(values);
    
   
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://127.0.0.1:5000/solve_characteristic_equation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          coeffs: values,
          order: order
        }),
      });
      
      if (!response.ok) {
        throw new Error(`Server responded with status: ${response.status}`);
      }
      
      const data = await response.json();
      setResult(data);
      console.log('API Response:', data);
    } catch (err) {
      setError(err.message);
      console.error('Error solving equation:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="card">
        <div className="order-label">Order of the equation:</div>
        <input 
          type="number" 
          min={0} 
          defaultValue={1} 
          onChange={handleOrderChange}
          className="order-input"
        />
        <span className="current-order">Current order: {order}</span>
      </div>

      <div className="equation-container">
        <div className="divs-container">
          {Array.from({ length: order + 1 }).map((_, index) => (
            <div key={index} className="term-container">
              <input
                className="coeff"
                type="text"
                defaultValue={0}
                placeholder="Coefficient"
                onChange={(e) => handleCoefficientChange(index, e.target.value)}
              />
              <span className="variable">S<sup>{order - index}</sup></span>
              {index < order && <span className="plus">+</span>}
            </div>
          ))}
        </div>

        <div className="button-container">
          
          <button 
            onClick={solveEquation} 
            className="solve-button"
            disabled={loading}
          >
            {loading ? 'Solving...' : 'Solve Equation'}
          </button>
        </div>

        {error && (
          <div className="error-message">
            Error: {error}
          </div>
        )}

        

        {result && (
          <div className="result-container">
            <h3>Stability Result:</h3>
            <p className={result.message.includes("stable") ? "stable-message" : "unstable-message"}>
              {result.message}
            </p>
            
            {result.poles && result.poles.length > 0 && (
              <div className="poles-section">
                <h4>Unstable Poles:</h4>
                <ul>
                  {result.poles.map((pole, i) => (
                    <li key={i}>{typeof pole === 'object' ? 
                      `${pole.real.toFixed(4)} ${pole.imag >= 0 ? '+' : ''}${pole.imag.toFixed(4)}i` : 
                      pole.toFixed(4)}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            
            {result.matrix && (
              <div className="matrix-section">
                <h4>Routh Array:</h4>
                <div className="routh-matrix">
                  {result.matrix.map((row, i) => (
                    <div key={i} className="matrix-row">
                      <span className="row-label">Row {order - i}:</span>
                      {row.map((val, j) => (
                        <span key={j} className="matrix-cell">
                           
                           {val.toFixed(3) }
                        </span>
                      ))}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default ChsEqn;
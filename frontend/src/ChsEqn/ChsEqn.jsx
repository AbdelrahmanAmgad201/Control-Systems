import { useState } from 'react';
import './ChsEqn.css';

function ChsEqn() {
  const [order, setOrder] = useState(1);
  const [coefficients, setCoefficients] = useState({});
  const [savedValues, setSavedValues] = useState(null);

  const handleOrderChange = (e) => {
    const newOrder = Math.max(0, parseInt(e.target.value) );
    setOrder(newOrder);
  };

  const handleCoefficientChange = (index, value) => {
    setCoefficients(prev => ({
      ...prev,
      [index]: value
    }));
    console.log(coefficients)
  };

  const saveValues = () => {
    const values = Array.from({ length: order +1}, (_, i) => coefficients[i] || '');
    setSavedValues(values);
    console.log('Saved values:', values);
    alert(`Values saved: ${values.join(', ')}`);
  };

  return (
    <div className="app-container">
      <div className="card">
        <div className="order-label">Order of the equation:</div>
        <span className="current-order">Order of the equation: </span>
        <input 
          type="number" 
          min={0} 
          defaultValue={1} 
          onChange={handleOrderChange}
          className="order-input"
        />
      </div>

      <div className="equation-container">
        <div className="divs-container">
          {Array.from({ length: order+1 }).map((_, index) => (
            <div key={index} className="term-container">
              <input
                className="coeff"
                type="text"
                defaultValue={0}
                placeholder="Coefficient"
                onChange={(e) => handleCoefficientChange(index, e.target.value)}
              />
              <span className="variable">S<sup>{index}</sup></span>
              {index < order  && <span className="plus">+</span>}
            </div>
          ))}
        </div>

        {(
          <button onClick={saveValues} className="save-button">
            Save Coefficients
          </button>
        )}

        {savedValues && (
          <div className="saved-values">
            <h3>Saved Values:</h3>
            <ul>
              {savedValues.map((value, i) => (
                <li key={i}>S<sup>{i }</sup>: {value}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default ChsEqn;
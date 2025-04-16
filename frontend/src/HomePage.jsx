import React from 'react';
import { Link } from 'react-router-dom';

function HomePage() {
  return (
    <div className="home-container" style={{ 
      display: 'flex', 
      flexDirection: 'column', 
      alignItems: 'center',
      justifyContent: 'center',
      height: '100vh',
      backgroundColor: '#f5f5f5'
    }}>
      <h1 style={{ marginBottom: '2rem', color: '#333' }}>Analysis Applications</h1>
      <div style={{ display: 'flex', gap: '2rem' }}>
        <Link to="/stability-analysis">
          <button style={{
            padding: '1rem 2rem',
            fontSize: '1.2rem',
            backgroundColor: '#4a90e2',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
          }}>
            Stability Analysis
          </button>
        </Link>
        <Link to="/signal-graph-analysis">
          <button style={{
            padding: '1rem 2rem',
            fontSize: '1.2rem',
            backgroundColor: '#50c878',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
          }}>
            Signal Graph Analysis
          </button>
        </Link>
      </div>
    </div>
  );
}

export default HomePage;
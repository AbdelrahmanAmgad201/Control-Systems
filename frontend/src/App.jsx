import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import StabilityAnalysis from './StabilityAnalysis/StabilityAnalysis';
import SignalGraphAnalysis from './SignalGraphAnalysis/SignalGraphAnalysis';
import HomePage from './HomePage';
import './styles/App.css'

function App() {
  return (
    <Router>
      <div className="main-app-container">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/stability-analysis" element={<StabilityAnalysis />} />
          <Route path="/signal-graph-analysis" element={<SignalGraphAnalysis />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
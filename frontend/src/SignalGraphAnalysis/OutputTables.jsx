import { useState, useEffect } from 'react';
import './styles/OutputTables.css';

function Tables({ edgeData, setShowTables }) {
  const [apiResults, setApiResults] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [transferFunction, setTransferFunction] = useState('');

  useEffect(() => {
    const fetchResults = async () => {
      // Reset states
      setLoading(true);
      setError(null);
      
      try {
        console.log("Sending edge data to API:", edgeData);

        // Prepare the request body
        const requestBody = {
          edges: edgeData
        };

        const apiUrl = 'http://localhost:5000/solve';
        const response = await fetch(apiUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody),
        });
        
        if (!response.ok) {
          throw new Error(`API returned error status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log("API response:", data);
        
        if (!data.success && data.error) {
          throw new Error(data.error);
        }
        
        setApiResults(data);
        setTransferFunction(`Transfer Function: ${data.result}`);
        
      } catch (err) {
        console.error('API request failed:', err);
        setError(err.message || 'Failed to fetch results from API');
      } finally {
        setLoading(false);
      }
    };

    // Call the fetch function
    if (edgeData && edgeData.length > 0) {
      fetchResults();
    } else {
      setLoading(false);
      setError('No edge data available to process');
    }
  }, [edgeData]);

  // Helper function to format node paths as strings
  const formatNodePath = (nodePath) => {
    return nodePath.join(' → ');
  };

  // Helper function to format loop paths
  const formatLoopPath = (loopPath) => {
    if (Array.isArray(loopPath)) {
      return loopPath.join(' → ');
    }
    return loopPath;
  };

  return (
    <div className="floating-table-overlay">
      <div className="floating-table">
        <div className="floating-table-header">
          <h2>Signal Flow Graph Results</h2>
          <button 
            className="close-button"
            onClick={() => setShowTables(false)}
          >
            ✕
          </button>
        </div>
        
        {/* Loading indicator */}
        {loading && (
          <div className="loading-indicator">
            <p>Processing your signal flow graph...</p>
          </div>
        )}
        
        {/* Error message */}
        {error && (
          <div className="error-message">
            <h3>Error</h3>
            <p>{error}</p>
          </div>
        )}
        
        {/* API Results */}
        {!loading && !error && apiResults && (
          <div className="api-results">
            {/* Display Transfer Function */}
            {apiResults.result && (
              <div className="transfer-function">
                <h3>Transfer Function</h3>
                <div className="function-display">
                  {apiResults.result}
                </div>
              </div>
            )}

            {/* Display Delta Value */}
            {apiResults.delta !== undefined && (
              <div className="delta-value">
                <h3>Delta (Δ)</h3>
                <div className="value-display">
                  {apiResults.delta}
                </div>
              </div>
            )}
            
            {/* Display Forward Paths */}
            {apiResults.Forward_paths_nodes && apiResults.Forward_paths_gains && (
              <div className="result-table">
                <h3>Forward Paths</h3>
                <div className="table-wrapper">
                  <table>
                    <thead>
                      <tr>
                        <th>Path</th>
                        <th>Gain</th>
                      </tr>
                    </thead>
                    <tbody>
                      {apiResults.Forward_paths_nodes.map((path, index) => (
                        <tr key={`path-${index}`}>
                          <td>{formatNodePath(path)}</td>
                          <td>{apiResults.Forward_paths_gains[index]}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Display Individual Loops */}
            {apiResults.loop_pairs && apiResults.loop_pairs[0] && apiResults.loop_pairs_gains && apiResults.loop_pairs_gains[0] && (
              <div className="result-table">
                <h3>Individual Loops</h3>
                <div className="table-wrapper">
                  <table>
                    <thead>
                      <tr>
                        <th>Loop</th>
                        <th>Gain</th>
                      </tr>
                    </thead>
                    <tbody>
                      {apiResults.loop_pairs[0].map((loop, index) => (
                        <tr key={`loop-${index}`}>
                          <td>{formatLoopPath(loop[0])}</td>
                          <td>{apiResults.loop_pairs_gains[0][index]}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Display 2 Non-Touching Loops */}
            {apiResults.loop_pairs && apiResults.loop_pairs[1] && apiResults.loop_pairs_gains && apiResults.loop_pairs_gains[1] && (
              <div className="result-table">
                <h3>2 Non-Touching Loops</h3>
                <div className="table-wrapper">
                  <table>
                    <thead>
                      <tr>
                        <th>Loops</th>
                        <th>Gain</th>
                      </tr>
                    </thead>
                    <tbody>
                      {apiResults.loop_pairs[1].map((loopPair, index) => (
                        <tr key={`2loops-${index}`}>
                          <td>
                            {loopPair.map((loop, i) => (
                              <span key={`loop-${index}-${i}`}>
                                {formatLoopPath(loop)}
                                {i < loopPair.length - 1 ? ' & ' : ''}
                              </span>
                            ))}
                          </td>
                          <td>{apiResults.loop_pairs_gains[1][index]}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Display 3 Non-Touching Loops */}
            {apiResults.loop_pairs && apiResults.loop_pairs[2] && apiResults.loop_pairs_gains && apiResults.loop_pairs_gains[2] && (
              <div className="result-table">
                <h3>3 Non-Touching Loops</h3>
                <div className="table-wrapper">
                  <table>
                    <thead>
                      <tr>
                        <th>Loops</th>
                        <th>Gain</th>
                      </tr>
                    </thead>
                    <tbody>
                      {apiResults.loop_pairs[2].map((loopTriple, index) => (
                        <tr key={`3loops-${index}`}>
                          <td>
                            {loopTriple.map((loop, i) => (
                              <span key={`loop-${index}-${i}`}>
                                {formatLoopPath(loop)}
                                {i < loopTriple.length - 1 ? ' & ' : ''}
                              </span>
                            ))}
                          </td>
                          <td>{apiResults.loop_pairs_gains[2][index]}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Display 4 Non-Touching Loops (if available) */}
            {apiResults.loop_pairs && apiResults.loop_pairs[3] && apiResults.loop_pairs_gains && apiResults.loop_pairs_gains[3] && (
              <div className="result-table">
                <h3>4 Non-Touching Loops</h3>
                <div className="table-wrapper">
                  <table>
                    <thead>
                      <tr>
                        <th>Loops</th>
                        <th>Gain</th>
                      </tr>
                    </thead>
                    <tbody>
                      {apiResults.loop_pairs[3].map((loopQuad, index) => (
                        <tr key={`4loops-${index}`}>
                          <td>
                            {loopQuad.map((loop, i) => (
                              <span key={`loop-${index}-${i}`}>
                                {formatLoopPath(loop)}
                                {i < loopQuad.length - 1 ? ' & ' : ''}
                              </span>
                            ))}
                          </td>
                          <td>{apiResults.loop_pairs_gains[3][index]}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Display Deltas (for each forward path) */}
            {apiResults.deltas && apiResults.deltas.length > 0 && (
              <div className="result-table">
                <h3>Delta Values for Each Forward Path</h3>
                <div className="table-wrapper">
                  <table>
                    <thead>
                      <tr>
                        <th>Path</th>
                        <th>Delta Value</th>
                      </tr>
                    </thead>
                    <tbody>
                      {apiResults.deltas.map((delta, index) => (
                        <tr key={`delta-${index}`}>
                          <td>Path {index + 1}</td>
                          <td>{delta}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}
        
        {/* Show a message when no results are available */}
        {!loading && !error && (!apiResults) && (
          <div className="no-results">
            <p>No results available. Please check your graph configuration.</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Tables;
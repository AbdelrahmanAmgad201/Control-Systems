import { useState, useCallback, useRef } from 'react';
import { 
  ReactFlow,
  useNodesState, 
  useEdgesState, 
  addEdge, 
  Background, 
  BackgroundVariant, 
  Controls 
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import './styles/App.css';
import './styles/SpecialButtons.css'
import Node from './CustomNode';
import CustomEdge from './CustomEdge';
import Tables from './OutputTables';
import { Link } from 'react-router-dom';

const initialNodes = [];
const initialEdges = [];
const nodeTypes = { customNode: Node };
const edgeTypes = { customEdge: CustomEdge };

function SignalGraphAnalysis() {
  const reactFlowWrapper = useRef(null);
  const [reactFlowInstance, setReactFlowInstance] = useState(null);
  const idCounter = useRef(0);
  const functionCounter = useRef(1);
  const edgeIdCounter = useRef(0);
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [showTables, setShowTables] = useState(false);
  const [functionValues, setFunctionValues] = useState({});
  const [edgeData, setEdgeData] = useState([]);

  // Default edge options - explicitly set type to customEdge
  const defaultEdgeOptions = { 
    animated: false,
    type: 'customEdge'
  };

  // Always return true to allow multiple connections
  const isValidConnection = useCallback(() => {
    return true;
  }, []);

  const onConnect = useCallback(
    (params) => {
      const edgeId = `e${edgeIdCounter.current}`;
      edgeIdCounter.current += 1;
      
      const functionId = `g${functionCounter.current}`;
      functionCounter.current += 1;
      
      const newEdge = {
        ...params,
        id: edgeId,
        type: 'customEdge',
        data: { 
          functionId
        }
      };
      
      // Add the edge manually rather than using addEdge
      setEdges(eds => [...eds, newEdge]);
      
      // Initialize the function value
      setFunctionValues(prev => ({
        ...prev,
        [functionId]: '1' // Default to 1
      }));
    },
    [edges, setEdges]
  );

  const onDragStart = (event, nodeType) => {
    event.dataTransfer.setData('application/reactflow', nodeType);
    event.dataTransfer.effectAllowed = 'move';
  };

  const onDragOver = useCallback((event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onDrop = useCallback(
    (event) => {
      event.preventDefault();

      const reactFlowBounds = reactFlowWrapper.current.getBoundingClientRect();
      const type = event.dataTransfer.getData('application/reactflow');

      // Check if we have valid data
      if (typeof type === 'undefined' || !type) {
        return;
      }

      const position = reactFlowInstance.screenToFlowPosition({
        x: event.clientX - reactFlowBounds.left,
        y: event.clientY - reactFlowBounds.top,
      });

      const newNode = {
        id: `${idCounter.current}`,
        type: 'customNode',
        position: position,
        data: {name: `N${idCounter.current}`},
      };

      idCounter.current += 1;
      setNodes((nds) => nds.concat(newNode));
    },
    [reactFlowInstance, setNodes]
  );

  const handleFunctionValueChange = (functionId, value) => {
    // Ensure the value is a number (or empty string that will be treated as the default)
    if (value === '' || !isNaN(value)) {
      setFunctionValues(prev => ({
        ...prev,
        [functionId]: value
      }));
    }
  };

  const clearGraph = () => {
    setEdges([]);
    setNodes([]);
    idCounter.current = 0;
    functionCounter.current = 1;
    edgeIdCounter.current = 0;
    setFunctionValues({});
  };

  // Function to create edge data array in the format {from, to, gain}
  const createEdgeDataArray = () => {
    const edgeDataArray = edges.map(edge => {
      // Convert to number or default to 1
      const numValue = functionValues[edge.data?.functionId] === '' ? 
        1 : 
        Number(functionValues[edge.data?.functionId] || 1);
        
      return {
        from: `N${edge.source}`,
        to: `N${edge.target}`,
        gain: numValue
      };
    });
    
    return edgeDataArray;
  };

  const handleShowTables = () => {
    const edgeDataArray = createEdgeDataArray();
    setEdgeData(edgeDataArray);
    setShowTables(true);
  };

  return (
    <div className="full-screen-container">      
      {/* Actual App Container */}
      <div className="signal-app-container">
        {/* Buttons */}
        <div className="button-bar">
          <div className="top-left-button">
            <button
              onDragStart={(event) => onDragStart(event, 'customNode')}
              draggable
              id='add-node-btn'
            >
              <span>
                <svg
                  height="24"
                  width="24"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path d="M0 0h24v24H0z" fill="none"></path>
                  <path d="M11 11V5h2v6h6v2h-6v6h-2v-6H5v-2z" fill="currentColor"></path>
                </svg>
                Node
              </span>
            </button>
          </div>

          <div className="bottom-right-buttons">
            <button onClick={clearGraph} id='clear-btn'>
              <span className="text">Clear</span>
              <span>Sure?</span>
            </button>
            <button onClick={handleShowTables} id='analyse-btn'>
              <span className="button-content">Analyse</span>
            </button>
          </div>
        </div>

        {/* Graph Container */}
        <div className="graph-container" ref={reactFlowWrapper}>
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onInit={setReactFlowInstance}
            onDrop={onDrop}
            onDragOver={onDragOver}
            nodeTypes={nodeTypes}
            edgeTypes={edgeTypes}
            defaultEdgeOptions={defaultEdgeOptions}
            isValidConnection={isValidConnection}
            connectOnClick={false}
            fitView
          >
            <Background color="#aaa" variant={BackgroundVariant.Dots} />
            <Controls />
          </ReactFlow>
        </div>

        {/* Function Values Table - Always below ReactFlow */}
        <div className="function-values-table">
          <h2>Branches Gains</h2>
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Function</th>
                  <th>Value</th>
                </tr>
              </thead>
              <tbody>
                {edges.length > 0 ? (
                  edges.map((edge) => {
                    const functionId = edge.data?.functionId;
                    return functionId ? (
                      <tr key={edge.id}>
                        <td>{functionId}</td>
                        <td>
                          <input
                            type="number"
                            value={functionValues[functionId] || ''}
                            onChange={(e) => handleFunctionValueChange(functionId, e.target.value)}
                            placeholder="1"
                            step="any" // Allows decimal values
                          />
                        </td>
                      </tr>
                    ) : null;
                  })
                ) : (
                  <tr>
                    <td colSpan="2">No functions defined yet. Connect nodes to create functions.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Floating Tables Modal - Separate from function values */}
        {showTables && (
          <Tables edgeData={edgeData} setShowTables={setShowTables} />
        )}
      </div>
    </div>
  );
}

export default SignalGraphAnalysis;
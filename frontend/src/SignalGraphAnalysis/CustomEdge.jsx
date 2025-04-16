import { EdgeLabelRenderer, useReactFlow } from '@xyflow/react';
import { useState, useCallback, useEffect } from 'react';
import './styles/Edge.css';

function CustomEdge({ id, sourceX, sourceY, targetX, targetY, data, selected }) {
    const [controlPoint, setControlPoint] = useState({});

    const reactFlowInstance = useReactFlow();
    const functionId = data?.functionId || 'g?';

    // Update control point when source or target positions change
    useEffect(() => {
        // Guard against undefined or NaN values
        if (!sourceX || !sourceY || !targetX || !targetY || 
            isNaN(sourceX) || isNaN(sourceY) || isNaN(targetX) || isNaN(targetY)) {
            return;
        }

        if (data?.controlPoint && 
            !isNaN(data.controlPoint.x) && 
            !isNaN(data.controlPoint.y)) {
            setControlPoint(data.controlPoint);
        } else {
            // Set default control point if none exists or values are invalid
            setControlPoint({
                x: (sourceX + targetX) / 2,
                y: (sourceY + targetY) / 2 - 30,
            });
        }
    }, [sourceX, sourceY, targetX, targetY, data]);

    const calculateEdgePath = () => {
        if (isNaN(sourceX) || isNaN(sourceY) || isNaN(targetX) || isNaN(targetY) ||
            isNaN(controlPoint.x) || isNaN(controlPoint.y)) {
            return `M ${sourceX},${sourceY} L ${targetX},${targetY}`;
        }
        
        return `M ${sourceX},${sourceY} Q ${controlPoint.x},${controlPoint.y} ${targetX},${targetY}`;
    };

    const edgePath = calculateEdgePath();

    // Calculate position for arrowhead - with safety checks
    const calculateArrowPath = () => {
        // Verify all values are valid
        if (isNaN(sourceX) || isNaN(sourceY) || isNaN(targetX) || isNaN(targetY) ||
            isNaN(controlPoint.x) || isNaN(controlPoint.y)) {
            return '';
        }

        // Get a point along the quadratic curve that's close to the target
        const t = 0.9; // Position at 90% along the curve (close to target)
        const arrowX = (1-t)*(1-t)*sourceX + 2*(1-t)*t*controlPoint.x + t*t*targetX;
        const arrowY = (1-t)*(1-t)*sourceY + 2*(1-t)*t*controlPoint.y + t*t*targetY;
        
        // Calculate angle for the arrowhead
        const dx = targetX - arrowX;
        const dy = targetY - arrowY;
        const angle = Math.atan2(dy, dx);
        
        // Arrow dimensions
        const arrowLength = 6;
        const arrowWidth = 3;
    
        // Calculate arrow points
        const arrowPoint1X = arrowX - arrowLength * Math.cos(angle - Math.PI/6);
        const arrowPoint1Y = arrowY - arrowLength * Math.sin(angle - Math.PI/6);
        const arrowPoint2X = arrowX - arrowLength * Math.cos(angle + Math.PI/6);
        const arrowPoint2Y = arrowY - arrowLength * Math.sin(angle + Math.PI/6);
    
        // Create arrowhead path
        return `M ${arrowX},${arrowY} L ${arrowPoint1X},${arrowPoint1Y} L ${arrowPoint2X},${arrowPoint2Y} Z`;
    };

    const arrowPath = calculateArrowPath();

    // Calculate label position exactly on the path
    // Use the quadratic Bezier formula to find a point at t=0.5 (middle of the curve)
    const calculateLabelPosition = () => {
        if (isNaN(sourceX) || isNaN(sourceY) || isNaN(targetX) || isNaN(targetY) ||
            isNaN(controlPoint.x) || isNaN(controlPoint.y)) {
            return {
                x: (sourceX + targetX) / 2,
                y: (sourceY + targetY) / 2
            };
        }
        
        // t = 0.5 gives us exactly the middle point of the quadratic Bezier curve
        const t = 0.5;
        const x = (1-t)*(1-t)*sourceX + 2*(1-t)*t*controlPoint.x + t*t*targetX;
        const y = (1-t)*(1-t)*sourceY + 2*(1-t)*t*controlPoint.y + t*t*targetY;
        
        return { x, y };
    };

    const labelPosition = calculateLabelPosition();

    const onDragStart = useCallback((event) => {
        event.stopPropagation();
        document.addEventListener('mousemove', onDrag);
        document.addEventListener('mouseup', onDragEnd);
    }, []);

    const onDrag = useCallback((event) => {
        const reactFlowBounds = reactFlowInstance.screenToFlowPosition({
            x: event.clientX,
            y: event.clientY
        });

        const newControlPoint = {
            x: reactFlowBounds.x,
            y: reactFlowBounds.y
        };

        setControlPoint(newControlPoint);

        reactFlowInstance.setEdges((edges) =>
            edges.map((edge) =>
                edge.id === id
                    ? { ...edge, data: { ...edge.data, controlPoint: newControlPoint } }
                    : edge
            )
        );
    }, [id, reactFlowInstance]);

    const onDragEnd = useCallback(() => {
        document.removeEventListener('mousemove', onDrag);
        document.removeEventListener('mouseup', onDragEnd);
    }, [onDrag]);

    return (
        <>
            {/* Main edge path */}
            <path
                id={id}
                className={`react-flow__edge-path ${selected ? 'selected' : ''} path`}
                d={edgePath}
                stroke="#555"
                fill="none"
            />
            
            {/* Arrow head - only render if we have a valid path */}
            {arrowPath && (
                <path
                    className={`react-flow__edge-path ${selected ? 'selected' : ''} arrow`}
                    d={arrowPath}
                    stroke="#555"
                    fill="#555"
                />
            )}

            <EdgeLabelRenderer>
                {/* Control Point */}
                {selected && (
                    <div
                        className="control-point selected"
                        style={{
                            transform: `translate(-50%, -50%) translate(${controlPoint.x}px,${controlPoint.y}px)`
                        }}
                        onMouseDown={onDragStart}
                    />
                )}
                
                {/* Function ID Label - positioned exactly on the Bezier curve */}
                <div
                    className="edge-label"
                    style={{
                        transform: `translate(-50%, -50%) translate(${labelPosition.x}px, ${labelPosition.y-10}px)`,
                    }}
                >
                    {functionId}
                </div>
            </EdgeLabelRenderer>
        </>
    );
}

export default CustomEdge;
import { Handle, Position } from '@xyflow/react';
import './styles/Node.css';

function Node({ data }) {
  return (
    <>
        <Handle type="target" position={Position.Left} className='handle' />
        <div className="circle">
          <div>{data.name}</div>
        </div>
        <Handle type="source" position={Position.Right} className='handle' />
    </>
  );
}

export default Node;
import React from 'react';
import { motion } from 'framer-motion';

const AgentCard = ({ agent, onClick, isSelected }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'text-vibrant-green';
      case 'idle':
        return 'text-golden-yellow';
      case 'error':
        return 'text-red-500';
      default:
        return 'text-gray-500';
    }
  };

  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      className={`
        w-full cursor-pointer relative overflow-hidden
        bg-black lcars-panel min-h-[200px]
        transition-all duration-300 ease-in-out
        ${isSelected ? 'ring-2 ring-electric-blue shadow-lg shadow-electric-blue/30' : ''}
      `}
    >
      <div className="lcars-header">
        <div className="lcars-elbow bg-electric-blue"></div>
        <div className="flex-grow bg-gray-900/90 p-4 overflow-hidden">
          <div className="flex items-center justify-between space-x-2">
            <h3 className="text-lg font-bold font-mono text-electric-blue tracking-wider uppercase truncate">
              {agent.name}
            </h3>
            <span className={`lcars-status ${getStatusColor(agent.status)} whitespace-nowrap text-sm px-2 py-1 rounded-full bg-gray-800/50`}>
              {agent.status}
            </span>
          </div>
        </div>
      </div>
      
      <div className="lcars-metrics grid grid-cols-2 gap-4 p-4">
        <div className="lcars-metric flex flex-col items-center justify-center bg-gray-1000/50 rounded-lg p-3">
          <p className="text-xs text-electric-blue mb-1 font-mono uppercase tracking-wider truncate w-full text-center">Tasks</p>
          <p className="text-xl font-mono text-electric-blue glow-text tabular-nums">{agent.metrics.tasks}</p>
        </div>
        <div className="lcars-metric flex flex-col items-center justify-center bg-gray-1000/50 rounded-lg p-3">
          <p className="text-xs text-electric-blue mb-1 font-mono uppercase tracking-wider truncate w-full text-center">Success</p>
          <p className="text-xl font-mono text-vibrant-green glow-text tabular-nums">{agent.metrics.success}%</p>
        </div>
      </div>

      <div className="lcars-description p-4 text-sm text-gray-400 truncate">
        {agent.description || 'Specialized agent for handling specific tasks and operations.'}
      </div>
    </motion.div>
  );
};

export default AgentCard;
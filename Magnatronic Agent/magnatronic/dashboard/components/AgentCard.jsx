import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

const AgentCard = ({ agent }) => { // Remove status and metrics props
  const [isExpanded, setIsExpanded] = useState(false);

  // Dynamic background gradient based on agent type
  const getGradient = (type) => {
    const gradients = {
      research: 'from-blue-900/80 to-blue-700/60',
      creative: 'from-purple-900/80 to-purple-700/60',
      visual: 'from-green-900/80 to-green-700/60',
      code: 'from-red-900/80 to-red-700/60'
    };
    return gradients[type] || 'from-gray-900/80 to-gray-700/60';
  };

  return (
    <div
      className={`
        relative overflow-hidden rounded-lg p-6
        bg-gradient-to-br ${getGradient(agent.type)}
        border border-opacity-20 border-white/20
        backdrop-blur-sm
        transform transition-all duration-300 ease-in-out
        hover:scale-[1.02] hover:shadow-[0_0_30px_rgba(255,255,255,0.1)]
        ${isExpanded ? 'h-96' : 'h-48'}
      `}
    >
      {/* Matrix code rain effect */}
      <div className="absolute inset-0 bg-matrix-code opacity-5 animate-matrix-rain"></div>

      {/* Agent Status Indicator with enhanced glow */}
      <div className="flex items-center justify-between mb-4 relative z-10">
        <h3 className="text-xl font-bold text-white font-mono">{agent.name}</h3>
        <div className="flex items-center space-x-2">
          <div
            className={`
              h-3 w-3 rounded-full
              ${agent.status === 'active' ? 'bg-green-400 animate-pulse shadow-lg shadow-green-500/50' : 'bg-red-400'} // Use agent.status from API
            `}
          />
          <span className="text-sm text-white/80 font-mono">{agent.status}</span> // Use agent.status from API
        </div>
      </div>

      {/* Metrics Display with glassmorphism effect */}
      <div className="grid grid-cols-2 gap-4 mb-4 relative z-10">
        {Object.entries(agent.metrics || {}).map(([key, value]) => { // Use agent.metrics from API and fallback to empty object
          let displayValue = value;
          let displayKey = key;

          if (key === 'cpu_usage') {
            displayKey = 'CPU Usage';
            displayValue = `${value}%`;
          } else if (key === 'memory_usage') {
            displayKey = 'Memory Usage';
            displayValue = `${(value / (1024 * 1024)).toFixed(2)} MB`; // Convert bytes to MB
          } else if (key === 'task_completion_rate') {
            displayKey = 'Task Completion';
            displayValue = `${value}%`;
          } else if (key === 'response_time') {
            displayKey = 'Response Time';
            displayValue = `${value}s`;
          }

          return (
            <div
              key={key}
              className="
                bg-black/20 rounded p-2
                border border-white/10
                backdrop-blur-sm
                hover:bg-black/30
                transition-all duration-300
              "
            >
              <div className="text-xs text-white/60 font-mono">{displayKey}</div>
              <div className="text-lg font-mono text-white">{displayValue}</div>
            </div>
          );
        })}
      </div>

      {/* Expand/Collapse Button with glow effect */}
      {/* ... (rest of the component remains unchanged) */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="
          absolute bottom-4 right-4
          text-white/60 hover:text-white
          font-mono text-sm
          px-3 py-1 rounded
          bg-white/5 hover:bg-white/10
          border border-white/10
          transition-all duration-300
          hover:shadow-[0_0_15px_rgba(255,255,255,0.1)]
        "
      >
        {isExpanded ? 'Show Less' : 'Show More'}
      </button>

      {/* Expanded Content with fade-in effect */}
      {isExpanded && (
        <div className="mt-4 space-y-4 animate-fade-in relative z-10">
          <div className="
            bg-black/30 rounded-lg p-4
            border border-white/10
            backdrop-blur-sm
          ">
            <h4 className="text-sm font-semibold text-white/80 mb-2 font-mono">Current Tasks</h4>
            <ul className="space-y-2">
              {agent.tasks?.map((task, index) => (
                <li key={index} className="text-sm text-white/60 font-mono">{task}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

AgentCard.propTypes = {
  agent: PropTypes.shape({
    name: PropTypes.string.required,
    type: PropTypes.string.required,
    tasks: PropTypes.arrayOf(PropTypes.string)
  }).isRequired,
  // status: PropTypes.oneOf(['active', 'inactive']).isRequired, // Removed status prop
  // metrics: PropTypes.object.isRequired // Removed metrics prop
};

export default AgentCard;
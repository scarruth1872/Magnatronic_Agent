import React, { useState } from 'react';
import PropTypes from 'prop-types';

const AgentControlPanel = ({ agent, onTaskSubmit, onAgentToggle }) => {
  const [taskInput, setTaskInput] = useState('');
  const [selectedMode, setSelectedMode] = useState('standard');

  const getControlTheme = (type) => {
    const themes = {
      research: 'border-blue-500 focus:ring-blue-500',
      creative: 'border-purple-500 focus:ring-purple-500',
      visual: 'border-green-500 focus:ring-green-500',
      code: 'border-red-500 focus:ring-red-500'
    };
    return themes[type] || 'border-gray-500 focus:ring-gray-500';
  };

  const handleTaskSubmit = (e) => {
    e.preventDefault();
    if (taskInput.trim()) {
      onTaskSubmit({
        type: agent.type,
        mode: selectedMode,
        description: taskInput
      });
      setTaskInput('');
    }
  };

  return (
    <div className="bg-black/40 rounded-lg p-6 backdrop-blur-sm border border-white/10 relative overflow-hidden">
      {/* Matrix-inspired background effect */}
      <div className="absolute inset-0 bg-grid-white/[0.02] bg-[size:20px_20px] animate-matrix-flow"></div>
      
      {/* Mode Selection with enhanced styling */}
      <div className="mb-6 relative z-10">
        <h4 className="text-white/80 text-sm font-semibold mb-3 font-mono tracking-wider">Operation Mode</h4>
        <div className="grid grid-cols-3 gap-2">
          {['standard', 'advanced', 'experimental'].map(mode => (
            <button
              key={mode}
              onClick={() => setSelectedMode(mode)}
              className={`
                px-4 py-2 rounded text-sm font-medium font-mono
                ${selectedMode === mode
                  ? `bg-white/10 text-white border border-${agent.type === 'research' ? 'blue' : agent.type === 'creative' ? 'purple' : agent.type === 'visual' ? 'green' : 'red'}-500/50`
                  : 'bg-transparent text-white/60 hover:bg-white/5 border border-white/5'}
                transition-all duration-300 hover:scale-[1.02]
                hover:shadow-[0_0_15px_rgba(255,255,255,0.1)]
              `}
            >
              {mode.charAt(0).toUpperCase() + mode.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Task Input with dynamic glow effect */}
      <form onSubmit={handleTaskSubmit} className="mb-6 relative z-10">
        <div className="relative group">
          <input
            type="text"
            value={taskInput}
            onChange={(e) => setTaskInput(e.target.value)}
            placeholder={`Enter task for ${agent.name}...`}
            className={`
              w-full bg-black/30 rounded-lg px-4 py-3
              text-white placeholder-white/40 font-mono
              border ${getControlTheme(agent.type)}
              focus:outline-none focus:ring-2
              transition-all duration-300
              group-hover:shadow-[0_0_20px_rgba(255,255,255,0.1)]
            `}
          />
          <button
            type="submit"
            className={`
              absolute right-2 top-1/2 transform -translate-y-1/2
              px-4 py-1 rounded-md
              bg-white/10 hover:bg-white/20
              text-white/80 hover:text-white
              text-sm font-medium font-mono
              transition-all duration-300
              hover:shadow-[0_0_15px_rgba(255,255,255,0.2)]
            `}
          >
            Submit
          </button>
        </div>
      </form>

      {/* Quick Actions with enhanced hover effects */}
      <div className="grid grid-cols-2 gap-4 relative z-10">
        <button
          onClick={() => onAgentToggle()}
          className="
            px-4 py-2 rounded-lg
            bg-white/5 hover:bg-white/10
            text-white/80 hover:text-white
            text-sm font-medium font-mono
            transition-all duration-300
            hover:scale-[1.02]
            hover:shadow-[0_0_15px_rgba(255,255,255,0.1)]
            border border-white/5
          "
        >
          Toggle Agent
        </button>
        <button
          className="
            px-4 py-2 rounded-lg
            bg-white/5 hover:bg-white/10
            text-white/80 hover:text-white
            text-sm font-medium font-mono
            transition-all duration-300
            hover:scale-[1.02]
            hover:shadow-[0_0_15px_rgba(255,255,255,0.1)]
            border border-white/5
          "
        >
          View Logs
        </button>
      </div>
    </div>
  );
};

AgentControlPanel.propTypes = {
  agent: PropTypes.shape({
    name: PropTypes.string.isRequired,
    type: PropTypes.string.isRequired
  }).isRequired,
  onTaskSubmit: PropTypes.func.isRequired,
  onAgentToggle: PropTypes.func.isRequired
};

export default AgentControlPanel;
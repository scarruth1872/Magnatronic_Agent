import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { ArrowLeftIcon } from '@heroicons/react/outline';

const AgentPage = ({ agent, onBack }) => {
  const [agentData, setAgentData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAgentData = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(`/api/agents/${agent.id}/performance`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setAgentData(data);
      } catch (error) {
        console.error("Could not fetch agent data:", error);
        setError(error);
      } finally {
        setLoading(false);
      }
    };

    fetchAgentData();
  }, [agent.id]);

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

  if (loading) {
    return <div>Loading agent data...</div>; // Basic loading indicator
  }

  if (error) {
    return <div>Error loading agent data: {error.message}</div>; // Basic error display
  }

  if (!agentData) {
    return <div>No agent data available.</div>;
  }


  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="min-h-screen matrix-bg bg-black text-gray-100 p-6"
    >
      <div className="max-w-7xl mx-auto">
        {/* Header with LCARS-inspired design */}
        <div className="lcars-header flex items-center mb-8 bg-gray-900 rounded-lg overflow-hidden">
          <div className="lcars-elbow bg-[#FFCC00] w-16 h-16 rounded-tr-2xl"></div>
          <div className="flex-grow flex items-center p-4 bg-gray-900">
            <button
              onClick={onBack}
              className="mr-4 p-2 rounded-full hover:bg-gray-800 text-[#0066FF] transition-all"
            >
              <ArrowLeftIcon className="w-6 h-6" />
            </button>
            <h1 className="text-3xl font-bold font-inter text-[#0066FF]">{agentData.agent.name}</h1>
            <span className={`ml-4 px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(agentData.agent.status)}`}>
              {agentData.agent.status}
            </span>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Metrics Panel */}
          <div className="lcars-panel bg-gray-900 rounded-lg overflow-hidden">
            <div className="lcars-header flex items-center">
              <div className="lcars-elbow bg-[#0066FF] w-12 h-12 rounded-tr-2xl"></div>
              <h2 className="text-xl font-semibold text-[#0066FF] p-4">Performance Metrics</h2>
            </div>
            <div className="p-6 space-y-4">
              <div className="bg-gray-800 p-4 rounded-lg border-l-4 border-[#0066FF] flex justify-between items-center">
                <p className="text-sm text-gray-400 font-medium">Total Tasks</p>
                <p className="text-2xl font-mono text-[#0066FF] tabular-nums">{agentData.task_stats.total_assigned}</p>
              </div>
              <div className="bg-gray-800 p-4 rounded-lg border-l-4 border-[#FFCC00] flex justify-between items-center">
                <p className="text-sm text-gray-400 font-medium">Success Rate</p>
                <p className="text-2xl font-mono text-vibrant-green tabular-nums">{agentData.current_metrics.task_completion_rate}%</p>
              </div>
            </div>
          </div>

          {/* Controls Panel */}
          <div className="lcars-panel bg-gray-900 rounded-lg overflow-hidden lg:col-span-2">
            <div className="lcars-header flex items-center">
              <div className="lcars-elbow bg-[#FFCC00] w-12 h-12 rounded-tr-2xl"></div>
              <h2 className="text-xl font-semibold text-[#0066FF] p-4">Agent Controls</h2>
            </div>
            <div className="p-6">
              <div className="grid grid-cols-2 gap-4">
                <button className="p-4 bg-gray-800 rounded-lg hover:bg-gray-700 hover:shadow-lg hover:shadow-[#0066FF]/20 text-[#0066FF] font-medium transition-all">
                  Start Task
                </button>
                <button className="p-4 bg-gray-800 rounded-lg hover:bg-gray-700 hover:shadow-lg hover:shadow-[#0066FF]/20 text-[#0066FF] font-medium transition-all">
                  Stop Task
                </button>
                <button className="p-4 bg-gray-800 rounded-lg hover:bg-gray-700 hover:shadow-lg hover:shadow-[#0066FF]/20 text-[#0066FF] font-medium transition-all">
                  View Logs
                </button>
                <button className="p-4 bg-gray-800 rounded-lg hover:bg-gray-700 hover:shadow-lg hover:shadow-[#0066FF]/20 text-[#0066FF] font-medium transition-all">
                  Configure
                </button>
              </div>
            </div>
          </div>

          {/* Status Panel */}
          <div className="lcars-panel bg-gray-900 rounded-lg overflow-hidden lg:col-span-3">
            <div className="lcars-header flex items-center">
              <div className="lcars-elbow bg-[#0066FF] w-12 h-12 rounded-tr-2xl"></div>
              <h2 className="text-xl font-semibold text-[#0066FF] p-4">Current Status</h2>
            </div>
            <div className="p-6">
              <div className="bg-gray-800 p-4 rounded-lg font-mono text-sm border-l-4 border-[#FFCC00]">
                <p className="text-gray-400">Agent Type: <span className="text-[#0066FF]">{agentData.agent.type}</span></p>
                <p className="text-gray-400 mt-2">Last Active: <span className="text-[#0066FF]">{(new Date(agentData.agent.last_heartbeat)).toLocaleTimeString()}</span></p>
                <p className="text-gray-400 mt-2">Current Task: <span className="text-vibrant-green">Processing data...</span></p> {/* Hardcoded task - needs to be dynamic */}
              </div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default AgentPage;
import React, { useState, useEffect } from 'react';
import AgentCard from '../components/AgentCard';
import AgentControlPanel from '../components/AgentControlPanel';

const AgentDashboard = () => {
  const [agents, setAgents] = useState([]);
  const [systemMetrics, setSystemMetrics] = useState({}); // Add systemMetrics state

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await fetch('/api/system/metrics');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setAgents(data.agents); // Update agents state with API data
        setSystemMetrics(data); // Update systemMetrics state
      } catch (error) {
        console.error("Could not fetch system metrics:", error);
      }
    };

    fetchMetrics();
  }, []);

  const [selectedAgent, setSelectedAgent] = useState(null);

  const handleTaskSubmit = (task) => {
    console.log('Submitting task:', task);
  };

  const handleAgentToggle = (agentId) => {
    console.log('Toggling agent:', agentId);
  };

  return (
    <div className="min-h-screen bg-black text-white relative overflow-hidden">
      {/* Matrix-inspired animated background */}
      <div className="fixed inset-0 bg-[url('/matrix-bg.png')] opacity-10 pointer-events-none animate-matrix-rain"></div>
      <div className="fixed inset-0 bg-gradient-to-br from-black via-black/95 to-black/90"></div>
      
      <div className="relative z-10 container mx-auto px-4 py-8">
        {/* Header with glowing effect */}
        <div className="mb-12 text-center">
          <h1 className="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-500 via-cyan-400 to-green-500 animate-glow">
            Agent Command Center
          </h1>
          <p className="mt-4 text-lg text-white/60 font-mono">
            Multi-Agent System Control Interface
          </p>
        </div>

        {/* Agent Grid with enhanced layout */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          {agents.map((agent, index) => (
            <AgentCard
              key={index}
              agent={agent}
              status="active"
              metrics={agent.metrics}
              onClick={() => setSelectedAgent(agent)}
            />
          ))}
        </div>

        {/* Control Panel with smooth transition */}
        {selectedAgent && (
          <div className="mt-8 transform transition-all duration-500 ease-in-out">
            <h2 className="text-2xl font-semibold mb-6 font-mono text-white/90 flex items-center">
              <span className="inline-block w-3 h-3 rounded-full bg-green-500 mr-3 animate-pulse"></span>
              {selectedAgent.name} Control Interface
            </h2>
            <AgentControlPanel
              agent={selectedAgent}
              onTaskSubmit={handleTaskSubmit}
              onAgentToggle={() => handleAgentToggle(selectedAgent.id)}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default AgentDashboard;
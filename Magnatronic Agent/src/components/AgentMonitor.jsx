import React, { useState, useEffect } from 'react';
import '../styles/global.css';

const AgentMonitor = () => {
  const [agents, setAgents] = useState([]);
  const [systemMetrics, setSystemMetrics] = useState(null);
  const [wsStatus, setWsStatus] = useState('connecting');
  const ws = React.useRef(null);

  useEffect(() => {
    // Initialize WebSocket connection
    ws.current = new WebSocket('ws://localhost:8000/ws');

    ws.current.onopen = () => {
      setWsStatus('connected');
      console.log('WebSocket Connected');
    };

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'system_metrics') {
        setSystemMetrics(data.data);
        setAgents(data.data.agents);
      } else if (data.type === 'agent_status') {
        setAgents(prev => prev.map(agent =>
          agent.id === data.agent_id ? { ...agent, ...data.data } : agent
        ));
      }
    };

    ws.current.onclose = () => {
      setWsStatus('disconnected');
      console.log('WebSocket Disconnected');
    };

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, []);

  return (
    <div className="matrix-bg p-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* System Status */}
        <div className="matrix-card glow-blue">
          <h2 className="text-xl font-fira mb-4 text-accent-blue">
            System Status
            <span className={`ml-2 inline-block w-2 h-2 rounded-full ${wsStatus === 'connected' ? 'bg-accent-green' : 'bg-red-500'} animate-pulse`}></span>
          </h2>
          {systemMetrics && (
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-secondary-bg p-4 rounded-lg">
                <p className="text-sm text-gray-400">Active Agents</p>
                <p className="text-2xl text-accent-blue">{systemMetrics.active_agents}</p>
              </div>
              <div className="bg-secondary-bg p-4 rounded-lg">
                <p className="text-sm text-gray-400">System Load</p>
                <p className="text-2xl text-accent-green">{systemMetrics.system_load.cpu}%</p>
              </div>
            </div>
          )}
        </div>

        {/* Agent List */}
        <div className="matrix-card glow-blue">
          <h2 className="text-xl font-fira mb-4 text-accent-blue">Active Agents</h2>
          <div className="space-y-4">
            {agents.map(agent => (
              <div key={agent.id} className="bg-secondary-bg p-4 rounded-lg hover:glow-green transition-all duration-300">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="text-lg font-fira text-accent-blue">{agent.name}</h3>
                    <p className="text-sm text-gray-400">{agent.type}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-gray-400">CPU: {agent.metrics.cpu_usage}%</p>
                    <p className="text-sm text-gray-400">Memory: {Math.round(agent.metrics.memory_usage / 1024 / 1024)}MB</p>
                  </div>
                </div>
                <div className="mt-2">
                  <p className="text-xs text-gray-500">Tasks:</p>
                  <div className="text-sm text-accent-green">
                    {agent.tasks.join(', ')}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AgentMonitor;
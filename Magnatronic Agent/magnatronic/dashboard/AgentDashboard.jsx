import React, { useState, useEffect } from 'react';
import { UsersIcon as HiOutlineUsers, ChartBarIcon as HiOutlineChartBar, CogIcon as HiOutlineCog } from '@heroicons/react/outline';
import './global.css';
import AgentCard from './AgentCard';
import AgentPage from './AgentPage';

const LoadingSpinner = () => (
  <div className="loading-container">
    <div className="code-stream-loader">
      <div className="stream-line"></div>
    </div>
  </div>
);

const AgentDashboard = () => {
  // Add matrix background effect
  React.useEffect(() => {
    const matrixBg = document.createElement('div');
    matrixBg.className = 'matrix-bg';
    document.body.appendChild(matrixBg);
    return () => document.body.removeChild(matrixBg);
  }, []);

  const [agents, setAgents] = useState([]);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        setLoading(true);
        const mockAgents = [
          { id: 1, name: 'Automation Agent', status: 'active', type: 'automation', metrics: { tasks: 45, success: 92 } },
          { id: 2, name: 'NLP Agent', status: 'idle', type: 'nlp', metrics: { tasks: 30, success: 88 } },
          { id: 3, name: 'Visual Agent', status: 'active', type: 'visual', metrics: { tasks: 25, success: 95 } },
          { id: 4, name: 'Research Agent', status: 'active', type: 'research', metrics: { tasks: 38, success: 90 } },
          { id: 5, name: 'Knowledge Agent', status: 'error', type: 'knowledge', metrics: { tasks: 15, success: 75 } },
          { id: 6, name: 'Healthcare Agent', status: 'active', type: 'healthcare', metrics: { tasks: 42, success: 94 } },
          { id: 7, name: 'Finance Agent', status: 'active', type: 'finance', metrics: { tasks: 56, success: 91 } },
          { id: 8, name: 'Legal Agent', status: 'idle', type: 'legal', metrics: { tasks: 28, success: 87 } },
          { id: 9, name: 'Marketing Agent', status: 'active', type: 'marketing', metrics: { tasks: 35, success: 89 } },
          { id: 10, name: 'IT Agent', status: 'active', type: 'it', metrics: { tasks: 48, success: 93 } },
          { id: 11, name: 'Manufacturing Agent', status: 'active', type: 'manufacturing', metrics: { tasks: 52, success: 90 } },
          { id: 12, name: 'Smart Cities Agent', status: 'idle', type: 'smart_cities', metrics: { tasks: 22, success: 85 } },
          { id: 13, name: 'Energy Utilities Agent', status: 'active', type: 'energy', metrics: { tasks: 39, success: 92 } },
          { id: 14, name: 'Media Entertainment Agent', status: 'active', type: 'media', metrics: { tasks: 44, success: 88 } },
          { id: 15, name: 'Retail Agent', status: 'active', type: 'retail', metrics: { tasks: 63, success: 91 } },
          { id: 16, name: 'Education Agent', status: 'idle', type: 'education', metrics: { tasks: 31, success: 89 } },
          { id: 17, name: 'Monitoring Agent', status: 'active', type: 'monitoring', metrics: { tasks: 72, success: 95 } },
          { id: 18, name: 'Collaboration Agent', status: 'active', type: 'collaboration', metrics: { tasks: 58, success: 93 } },
          { id: 19, name: 'Personalization Agent', status: 'active', type: 'personalization', metrics: { tasks: 41, success: 90 } },
          { id: 20, name: 'Sentiment Analysis Agent', status: 'idle', type: 'sentiment', metrics: { tasks: 33, success: 87 } },
          { id: 21, name: 'Voice Interaction Agent', status: 'active', type: 'voice', metrics: { tasks: 47, success: 91 } },
          { id: 22, name: 'Code Execution Agent', status: 'active', type: 'code', metrics: { tasks: 65, success: 94 } },
          { id: 23, name: 'Data Visualization Agent', status: 'idle', type: 'visualization', metrics: { tasks: 29, success: 88 } },
          { id: 24, name: 'Symbology Agent', status: 'active', type: 'symbology', metrics: { tasks: 36, success: 92 } }
        ];
        setAgents(mockAgents);
      } catch (error) {
        console.error('Error fetching agents:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchAgents();
  }, []);

  if (selectedAgent) {
    return <AgentPage agent={selectedAgent} onBack={() => setSelectedAgent(null)} />;
  }

  return (
    <div className="min-h-screen bg-black text-gray-100 relative z-10">
      {/* Header with LCARS-inspired design */}
      <header className="bg-secondary-bg/90 backdrop-blur-sm shadow-lg py-4 px-6 sticky top-0 z-20">
        <div className="max-w-8xl mx-auto flex items-center gap-6">
          <div className="lcars-elbow bg-accent"></div>
          <div className="flex-grow flex flex-col md:flex-row justify-between items-center gap-6">
            <h1 className="text-4xl font-bold font-mono text-electric-blue glow-text truncate">
              Agent Dashboard
            </h1>
            <nav className="flex flex-wrap justify-center gap-4">
              <button
                onClick={() => setActiveTab('overview')}
                className={`btn-nav whitespace-nowrap ${activeTab === 'overview' ? 'bg-accent text-black' : ''}`}
              >
                <HiOutlineChartBar className="inline-block w-5 h-5 mr-2" />
                Overview
              </button>
              <button
                onClick={() => setActiveTab('agents')}
                className={`btn-nav whitespace-nowrap ${activeTab === 'agents' ? 'bg-accent text-black' : ''}`}
              >
                <HiOutlineUsers className="inline-block w-5 h-5 mr-2" />
                Agents
              </button>
              <button
                onClick={() => setActiveTab('settings')}
                className={`btn-nav whitespace-nowrap ${activeTab === 'settings' ? 'bg-accent text-black' : ''}`}
              >
                <HiOutlineCog className="inline-block w-5 h-5 mr-2" />
                Settings
              </button>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8">
        {loading ? (
          <LoadingSpinner />
        ) : (
          <div className="agent-grid">
            {agents.map(agent => (
              <AgentCard
                key={agent.id}
                agent={agent}
                onClick={() => setSelectedAgent(agent)}
                isSelected={selectedAgent?.id === agent.id}
              />
            ))}
          </div>
        )}
      </main>
    </div>
  );
};

export default AgentDashboard;
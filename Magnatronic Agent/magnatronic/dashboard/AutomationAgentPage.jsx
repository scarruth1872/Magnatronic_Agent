import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { ArrowLeftIcon } from '@heroicons/react/outline';
import { Line, Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const AutomationAgentPage = ({ agent, onBack }) => {
  const [taskData, setTaskData] = useState({
    labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
    datasets: [{
      label: 'Tasks Completed',
      data: [12, 19, 3, 5, 2, 3],
      borderColor: '#0066FF',
      backgroundColor: 'rgba(0, 102, 255, 0.2)',
      tension: 0.4
    }]
  });

  const [workflowData, setWorkflowData] = useState({
    labels: ['Scheduled', 'Running', 'Completed', 'Failed'],
    datasets: [{
      label: 'Workflow Status',
      data: [4, 2, 15, 1],
      backgroundColor: [
        '#FFCC00',
        '#0066FF',
        '#00FF00',
        '#FF0000'
      ]
    }]
  });

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'text-vibrant-green';
      case 'idle': return 'text-golden-yellow';
      case 'error': return 'text-red-500';
      default: return 'text-gray-500';
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="min-h-screen matrix-bg bg-black text-gray-100 p-6"
    >
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center mb-8">
          <button
            onClick={onBack}
            className="mr-4 p-2 rounded-full bg-gray-800 hover:bg-gray-700 text-electric-blue"
          >
            <ArrowLeftIcon className="w-6 h-6" />
          </button>
          <h1 className="text-3xl font-bold font-inter text-electric-blue">Automation Agent</h1>
          <span className={`ml-4 px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(agent.status)}`}>
            {agent.status}
          </span>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Task Monitoring */}
          <div className="lcars-panel bg-gray-900 lg:col-span-2">
            <div className="lcars-header">
              <div className="lcars-elbow"></div>
              <h2 className="text-xl font-semibold text-electric-blue p-4">Task Monitoring</h2>
            </div>
            <div className="p-6">
              <Line
                data={taskData}
                options={{
                  responsive: true,
                  plugins: {
                    legend: { display: false },
                    title: { display: false }
                  },
                  scales: {
                    y: {
                      grid: { color: 'rgba(255, 255, 255, 0.1)' },
                      ticks: { color: '#888' }
                    },
                    x: {
                      grid: { color: 'rgba(255, 255, 255, 0.1)' },
                      ticks: { color: '#888' }
                    }
                  }
                }}
              />
            </div>
          </div>

          {/* Metrics Panel */}
          <div className="panel bg-gray-900 rounded-lg p-6 shadow-lg overflow-hidden">
            <h2 className="text-xl font-semibold text-electric-blue mb-4 text-left truncate">Performance Metrics</h2>
            <div className="space-y-4">
              <div className="bg-gray-800 p-4 rounded-lg flex justify-between items-center overflow-hidden">
                <p className="text-sm text-gray-400 font-medium truncate mr-2">Active Workflows</p>
                <p className="text-2xl font-mono text-electric-blue tabular-nums shrink-0">{agent.metrics?.activeWorkflows || 0}</p>
              </div>
              <div className="bg-gray-800 p-4 rounded-lg flex justify-between items-center overflow-hidden">
                <p className="text-sm text-gray-400 font-medium truncate mr-2">Success Rate</p>
                <p className="text-2xl font-mono text-vibrant-green tabular-nums shrink-0">{agent.metrics?.success || 0}%</p>
              </div>
              <div className="bg-gray-800 p-4 rounded-lg flex justify-between items-center overflow-hidden">
                <p className="text-sm text-gray-400 font-medium truncate mr-2">Tasks Queued</p>
                <p className="text-2xl font-mono text-golden-yellow tabular-nums shrink-0">{agent.metrics?.queuedTasks || 0}</p>
              </div>
            </div>
          </div>

          {/* Workflow Status */}
          <div className="lcars-panel bg-gray-900 lg:col-span-2">
            <div className="lcars-header">
              <div className="lcars-elbow"></div>
              <h2 className="text-xl font-semibold text-electric-blue p-4">Workflow Status</h2>
            </div>
            <div className="p-6">
              <Bar
                data={workflowData}
                options={{
                  responsive: true,
                  plugins: {
                    legend: { display: false },
                    title: { display: false }
                  },
                  scales: {
                    y: {
                      grid: { color: 'rgba(255, 255, 255, 0.1)' },
                      ticks: { color: '#888' }
                    },
                    x: {
                      grid: { color: 'rgba(255, 255, 255, 0.1)' },
                      ticks: { color: '#888' }
                    }
                  }
                }}
              />
            </div>
          </div>

          {/* Controls Panel */}
          <div className="panel bg-gray-900 rounded-lg p-6 shadow-lg">
            <h2 className="text-xl font-semibold text-electric-blue mb-4">Agent Controls</h2>
            <div className="grid grid-cols-1 gap-4">
              <button className="p-4 bg-gray-800 rounded-lg hover:glow-border text-electric-blue font-medium transition-all">
                Schedule Task
              </button>
              <button className="p-4 bg-gray-800 rounded-lg hover:glow-border text-electric-blue font-medium transition-all">
                Optimize Workflow
              </button>
              <button className="p-4 bg-gray-800 rounded-lg hover:glow-border text-electric-blue font-medium transition-all">
                View Task Queue
              </button>
              <button className="p-4 bg-gray-800 rounded-lg hover:glow-border text-electric-blue font-medium transition-all">
                Configure Automation
              </button>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default AutomationAgentPage;
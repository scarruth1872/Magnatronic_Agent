import React from 'react';
import './styles/global.css';
import AgentMonitor from './components/AgentMonitor';

function App() {
  return (
    <div className="min-h-screen bg-primary-bg">
      <header className="py-6 px-4 border-b border-accent-blue/20">
        <h1 className="text-4xl font-fira text-accent-blue text-center glow-blue">Magnatronic Agent System</h1>
      </header>
      <main className="container mx-auto px-4 py-8">
        <AgentMonitor />
      </main>
    </div>
  );
}

export default App;
    {
      id: 'Agent-001',
      status: 'active',
      task: 'Processing data',
      metrics: {
        cpu: '45%',
        memory: '128MB',
        tasks: '3/5'
      }
    },
    {
      id: 'Agent-002',
      status: 'active',
      task: 'Monitoring system',
      metrics: {
        cpu: '32%',
        memory: '96MB',
        tasks: '2/5'
      }
    }
  ]);

  return (
    <div className="matrix-bg min-h-screen">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl glow-text mb-8 text-center">Magnatronic Agent System</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Enhanced API Status Section */}
          <div className="card backdrop-blur-sm bg-black/30 p-6 rounded-lg border border-electric-blue/20">
            <h2 className="heading text-xl mb-4 flex items-center">
              <span className="inline-block w-2 h-2 rounded-full bg-green-500 mr-2 animate-pulse"></span>
              System Status
            </h2>
            <div className="status-panel grid grid-cols-2 gap-4">
              <div className="status-item active bg-electric-blue/10 p-4 rounded-lg">
                <span className="code-text block mb-2">{systemMetrics.status}</span>
                <div className="text-sm text-gray-400">System operational</div>
                <div className="text-xs text-gray-500 mt-2">Uptime: {systemMetrics.uptime}</div>
              </div>
              <div className="status-item bg-electric-blue/10 p-4 rounded-lg">
                <span className="code-text block mb-2">Response Time</span>
                <div className="text-sm text-gray-400">{systemMetrics.responseTime}</div>
                <div className="text-xs text-gray-500 mt-2">Last update: {new Date(systemMetrics.lastUpdate).toLocaleTimeString()}</div>
              </div>
            </div>
          </div>

          {/* Enhanced Active Agents Section */}
          <div className="card backdrop-blur-sm bg-black/30 p-6 rounded-lg border border-electric-blue/20">
            <h2 className="heading text-xl mb-4">Active Agents</h2>
            <div className="agent-list space-y-4">
              {agents.map(agent => (
                <div key={agent.id} className="agent-item bg-electric-blue/10 p-4 rounded-lg hover:bg-electric-blue/20 transition-all duration-300">
                  <div className="flex justify-between items-start">
                    <div>
                      <div className="code-text text-lg mb-1">{agent.id}</div>
                      <div className="text-sm text-gray-400">{agent.task}</div>
                    </div>
                    <div className="text-right">
                      <div className="text-xs text-gray-500 mb-1">Resources</div>
                      <div className="text-sm text-gray-400">CPU: {agent.metrics.cpu}</div>
                      <div className="text-sm text-gray-400">Memory: {agent.metrics.memory}</div>
                      <div className="text-sm text-gray-400">Tasks: {agent.metrics.tasks}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
      {/* Content from Magnatronic agent.md will be inserted here */}
      <div className="markdown-content"> {/* Added container for markdown content */}
        <h1>Magnatronic Agent</h1>
        <p>Here's a concise summary of the functionalities of each agent:</p>
        <ol>
          <li>Research Agent
            <p><b>Function:</b> Fetch, filter, and summarize real-time web information.</p>
            <p><b>Capabilities:</b></p>
            <ul>
              <li>Search for data on demand.</li>
              <li>Summarize large datasets into actionable insights.</li>
              <li>Evaluate and rank sources for credibility.</li>
            </ul>
            <p><b>Tools:</b></p>
            <ul>
              <li>Web tool for information retrieval.</li>
              <li>NLP models for summarization and analysis.</li>
            </ul>
          </li>
          <li>Creative Agent
            <p><b>Function:</b> Generate creative content.</p>
            <p><b>Capabilities:</b></p>
            <ul>
              <li>Compose articles, scripts, and marketing material.</li>
              <li>Brainstorm innovative solutions.</li>
              <li>Adapt writing style based on user preferences.</li>
            </ul>
            <p><b>Tools:</b></p>
            <ul>
              <li>Content generation engines (e.g., GPT).</li>
              <li>Brainstorming modules.</li>
            </ul>
          </li>
          <li>Visual Agent
            <p><b>Function:</b> Generate images and visual content.</p>
            <p><b>Capabilities:</b></p>
            <ul>
              <li>Produce AI-generated art and designs.</li>
              <li>Create visuals for branding and presentations.</li>
              <li>Interpret prompts contextually.</li>
            </ul>
            <p><b>Tools:</b></p>
            <ul>
              <li>Generative AI image tools (e.g., DALL·E).</li>
              <li>Style transfer and post-processing pipelines.</li>
            </ul>
          </li>
          <li>Code Execution Agent
            <p><b>Function:</b> Execute Python code and perform calculations.</p>
            <p><b>Capabilities:</b></p>
            <ul>
              <li>Run scripts and analyze outputs.</li>
              <li>Debug and optimize code snippets.</li>
              <li>Perform computational tasks.</li>
            </ul>
            <p><b>Tools:</b></p>
            <ul>
              <li>Python execution environment with data analysis and ML libraries.</li>
              <li>Secure sandbox environment.</li>
            </ul>
          </li>
          <li>Knowledge Agent
            <p><b>Function:</b> Provide accurate answers to questions.</p>
            <p><b>Capabilities:</b></p>
            <ul>
              <li>Access internal knowledge database.</li>
              <li>Provide concise and verified answers.</li>
              <li>Use logical reasoning for problem-solving.</li>
            </ul>
            <p><b>Tools:</b></p>
            <ul>
              <li>Internal knowledge base with semantic search.</li>
              <li>Reasoning algorithms for fact-checking.</li>
            </ul>
          </li>
          <li>Symbology Agent
            <p><b>Function:</b> Optimize and represent complex systems.</p>
            <p><b>Capabilities:</b></p>
            <ul>
              <li>Create symbolic representations of systems.</li>
              <li>Optimize agent communication using symbology.</li>
              <li>Monitor system performance.</li>
            </ul>
            <p><b>Tools:</b></p>
            <ul>
              <li>Symbol registry for symbolic language.</li>
              <li>Multi-agent communication protocols.</li>
            </ul>
          </li>
          <li>Monitoring Agent
            <p><b>Function:</b> Oversee the multi-agent system.</p>
            <p><b>Capabilities:</b></p>
            <ul>
              <li>Monitor agent performance in real time.</li>
              <li>Provide insights into agent activities and system health.</li>
              <li>Detect and resolve conflicts.</li>
            </ul>
            <p><b>Tools:</b></p>
            <ul>
              <li>Dashboard with visualization tools.</li>
              <li>Logging and alerting systems.</li>
            </ul>
          </li>
        </ol>
        <h2>Inter-Agent Communication</h2>
        <p><b>To ensure collaboration:</b></p>
        <ul>
          <li>Message Passing Interface (MPI): Real-time data exchange.</li>
          <li>Shared Knowledge Base: Consistent information access.</li>
          <li>Task Queues: Dynamic task delegation and management.</li>
        </ul>
        <h2>Implementation Framework</h2>
        <p>[Placeholder: Details on the implementation framework will be added here.]</p>
      </div>
    </div>
  );
}

export default App;
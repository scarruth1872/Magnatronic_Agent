import React, { useState, useEffect } from 'react';
import { ArrowLeftIcon } from '@heroicons/react/outline';

const NLPAgentPage = ({ onBack }) => {
  const [inputText, setInputText] = useState('');
  const [targetLanguage, setTargetLanguage] = useState('es');
  const [result, setResult] = useState('');
  const [activeTab, setActiveTab] = useState('translate');
  const [metrics, setMetrics] = useState({
    requestCount: 0,
    errorCount: 0,
    avgProcessingTime: 0
  });

  // Fetch performance metrics
  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await fetch('/api/nlp/metrics');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
          throw new TypeError('Expected JSON response but received ' + contentType);
        }
        const data = await response.json();
        if (!data || typeof data !== 'object') {
          throw new TypeError('Invalid response format');
        }
        if (!('requestCount' in data && 'errorCount' in data && 'avgProcessingTime' in data)) {
          throw new TypeError('Missing required metrics fields');
        }
        setMetrics(data);
      } catch (error) {
        console.error('Error fetching metrics:', error.message);
        // Set error state and display user-friendly message
        setMetrics({
          requestCount: 0,
          errorCount: 0,
          avgProcessingTime: 0,
          error: `Failed to fetch metrics: ${error.message}`
        });
      }
    };

    // Initial fetch and set up interval
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 5000);

    return () => clearInterval(interval);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    // TODO: Implement API calls to NLP agent
    try {
      const response = await fetch('/api/nlp', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          action: activeTab,
          text: inputText,
          targetLanguage: targetLanguage,
        }),
      });
      const data = await response.json();
      setResult(data.result);
    } catch (error) {
      console.error('Error:', error);
      setResult('An error occurred while processing your request.');
    }
  };

  const languageOptions = [
    { value: 'es', label: 'Spanish' },
    { value: 'fr', label: 'French' },
    { value: 'de', label: 'German' },
    { value: 'it', label: 'Italian' },
    { value: 'pt', label: 'Portuguese' },
  ];

  return (
    <div className="min-h-screen matrix-bg bg-black text-gray-100 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="flex items-center mb-8">
          <button
            onClick={onBack}
            className="mr-4 p-2 rounded-full hover:bg-gray-800 transition-colors"
          >
            <ArrowLeftIcon className="h-6 w-6 text-electric-blue" />
          </button>
          <h1 className="text-3xl font-bold font-inter text-electric-blue transition-glow">
            NLP Agent Interface
          </h1>
        </div>

        {/* Tabs */}
        <div className="flex space-x-4 mb-6">
          {['translate', 'analyze', 'summarize'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`${
                activeTab === tab
                  ? 'bg-electric-blue text-black'
                  : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
              } px-4 py-2 rounded-md transition-all duration-200 capitalize`}
            >
              {tab}
            </button>
          ))}
        </div>

        {/* Main Content */}
        <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">
                Input Text
              </label>
              <textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                className="w-full h-32 bg-gray-800 text-gray-100 rounded-md p-3 border border-gray-700 focus:border-electric-blue focus:ring-1 focus:ring-electric-blue transition-all duration-200"
                placeholder={`Enter text to ${activeTab}...`}
              />
            </div>

            {activeTab === 'translate' && (
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2">
                  Target Language
                </label>
                <select
                  value={targetLanguage}
                  onChange={(e) => setTargetLanguage(e.target.value)}
                  className="w-full bg-gray-800 text-gray-100 rounded-md p-3 border border-gray-700 focus:border-electric-blue focus:ring-1 focus:ring-electric-blue transition-all duration-200"
                >
                  {languageOptions.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </div>
            )}

            <button
              type="submit"
              className="w-full bg-electric-blue text-black py-3 rounded-md hover:bg-blue-400 transition-colors duration-200 font-medium"
            >
              Process
            </button>
          </form>

          {result && (
            <div className="mt-6">
              <h3 className="text-lg font-medium text-gray-300 mb-2">Result:</h3>
              <div className="bg-gray-800 rounded-md p-4 border border-gray-700">
                <pre className="text-gray-100 whitespace-pre-wrap font-mono">
                  {result}
                </pre>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default NLPAgentPage;
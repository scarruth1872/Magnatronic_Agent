import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen matrix-bg bg-black text-gray-100 p-6 flex items-center justify-center">
          <div className="bg-gray-900 rounded-lg p-6 border border-electric-blue max-w-2xl w-full">
            <h2 className="text-2xl font-bold text-electric-blue mb-4">System Malfunction Detected</h2>
            <p className="text-gray-300 mb-4">An error has occurred in the Matrix. Our agents are working to resolve the issue.</p>
            <pre className="bg-gray-800 p-4 rounded-md overflow-auto text-sm text-red-400">
              {this.state.error && this.state.error.toString()}
            </pre>
            <button
              onClick={() => window.location.reload()}
              className="mt-4 bg-electric-blue text-black px-4 py-2 rounded-md hover:bg-blue-400 transition-colors duration-200"
            >
              Reload System
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
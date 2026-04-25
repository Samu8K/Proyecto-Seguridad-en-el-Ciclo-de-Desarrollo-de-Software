import React, { useEffect, useState } from 'react';
import { useWebSocket } from './hooks/useWebSocket';
import FindingsTable from './components/FindingsTable';
import MetricsChart from './components/MetricsChart';
import axios from 'axios';
import toast, { Toaster } from 'react-hot-toast';

function App() {
  const [findings, setFindings] = useState([]);
  const [metrics, setMetrics] = useState({ total: 0, open: 0, in_progress: 0, resolved: 0, by_severity: {} });
  const { lastMessage } = useWebSocket('ws://localhost:8000/ws');

  useEffect(() => {
    // Fetch initial data
    const fetchData = async () => {
      try {
        const [metricsRes, findingsRes] = await Promise.all([
          axios.get('/api/metrics/dashboard'),
          axios.get('/api/metrics/findings?limit=20')
        ]);
        setMetrics(metricsRes.data);
        setFindings(findingsRes.data);
      } catch (err) {
        toast.error('Failed to load data');
      }
    };
    fetchData();
  }, []);

  useEffect(() => {
    if (lastMessage && lastMessage.type === 'NEW_FINDING') {
      setFindings(prev => [lastMessage.data, ...prev]);
      toast.success('New vulnerability detected');
      // Optionally refresh metrics
      axios.get('/api/metrics/dashboard').then(res => setMetrics(res.data));
    }
  }, [lastMessage]);

  return (
    <div className="min-h-screen bg-gray-100">
      <Toaster position="top-right" />
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-900">🛡️ ASPM - Vulnerability Management</h1>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {/* Metrics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-white p-4 rounded-lg shadow">
            <p className="text-sm text-gray-500">Total Findings</p>
            <p className="text-2xl font-bold">{metrics.total}</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow">
            <p className="text-sm text-red-500">Open</p>
            <p className="text-2xl font-bold">{metrics.open}</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow">
            <p className="text-sm text-yellow-500">In Progress</p>
            <p className="text-2xl font-bold">{metrics.in_progress}</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow">
            <p className="text-sm text-green-500">Resolved</p>
            <p className="text-2xl font-bold">{metrics.resolved}</p>
          </div>
        </div>

        {/* Chart and Table */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          <div className="lg:col-span-1">
            <MetricsChart data={metrics} />
          </div>
          <div className="lg:col-span-2">
            <div className="bg-white p-4 rounded-lg shadow">
              <h3 className="text-lg font-semibold mb-2">Latest Findings</h3>
              <FindingsTable findings={findings} />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;

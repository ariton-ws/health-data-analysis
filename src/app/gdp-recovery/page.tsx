'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  BarChart, Bar, ScatterChart, Scatter, PieChart, Pie, Cell
} from 'recharts';

export default function GDPRecoveryPage() {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedChart, setSelectedChart] = useState('overview');
  const [filterLevel, setFilterLevel] = useState('all');
  const [showReport, setShowReport] = useState(false);

  useEffect(() => {
    fetch('/api/gdp-recovery-data')
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data)) {
          // Filter out rows with too many null values
          const filteredData = data.filter(row => {
            const nullCount = Object.values(row).filter(val => val === null).length;
            return nullCount < 3; // Keep rows with less than 3 null values
          });
          setData(filteredData);
        } else {
          setError('Invalid data format');
        }
        setLoading(false);
      })
      .catch(() => {
        setError('Failed to load data');
        setLoading(false);
      });
  }, []);

  const filteredData = data.filter(row => {
    if (filterLevel === 'all') return true;
    return row.Development_Level === filterLevel;
  });

  const validData = filteredData.filter(row => 
    row.REF_AREA != null && 
    (row.GDP_Growth_2020 != null || row.GDP_Growth_2021 != null || row.Recovery_Speed != null)
  );

  const chartData = validData.map(row => ({
    ...row,
    Country: row.REF_AREA,
    GDPGrowth2020: typeof row.GDP_Growth_2020 === 'number' ? row.GDP_Growth_2020 : null,
    GDPGrowth2021: typeof row.GDP_Growth_2021 === 'number' ? row.GDP_Growth_2021 : null,
    RecoveryRate: typeof row.Recovery_Speed === 'number' ? row.Recovery_Speed : null,
    DevelopmentLevel: row.Development_Level || 'N/A'
  }));

  const developmentLevels = [...new Set(data.map(row => row.Development_Level).filter(Boolean))];

  // Helper function to safely format numbers
  const formatNumber = (value: any, decimals: number = 2) => {
    if (value === null || value === undefined || value === 'N/A') return 'N/A';
    if (typeof value === 'number') return value.toFixed(decimals);
    return 'N/A';
  };

  if (loading) return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
      <div className="text-xl text-gray-800">Loading GDP Recovery Analysis...</div>
    </div>
  );
  
  if (error) return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
      <div className="text-center">
        <div className="text-red-600 text-6xl mb-4">⚠️</div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Error Loading Data</h2>
        <p className="text-gray-700 mb-4">{error}</p>
        <button 
          onClick={() => window.location.reload()}
          className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
        >
          Try Again
        </button>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <Link href="/" className="text-blue-700 hover:underline mb-4 inline-block font-medium">
          ← Back to Home
        </Link>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold text-gray-900 mb-2">GDP Recovery Analysis</h1>
          <p className="text-gray-700">Economic recovery patterns post-COVID-19 pandemic</p>
        </motion.div>

        {/* Data Summary */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-xl shadow-lg p-6 mb-8"
        >
          <h2 className="text-2xl font-semibold mb-4 text-gray-900">Data Overview</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
              <div className="text-2xl font-bold text-blue-700">{validData.length}</div>
              <div className="text-sm text-gray-700">Countries with Data</div>
            </div>
            <div className="bg-green-50 p-4 rounded-lg border border-green-200">
              <div className="text-2xl font-bold text-green-700">
                {validData.filter(row => row.GDPGrowth2020 !== null && row.GDPGrowth2020 !== 'N/A').length}
              </div>
              <div className="text-sm text-gray-700">Countries with 2020 Data</div>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg border border-purple-200">
              <div className="text-2xl font-bold text-purple-700">
                {validData.filter(row => row.GDPGrowth2021 !== null && row.GDPGrowth2021 !== 'N/A').length}
              </div>
              <div className="text-sm text-gray-700">Countries with 2021 Data</div>
            </div>
            <div className="bg-orange-50 p-4 rounded-lg border border-orange-200">
              <div className="text-2xl font-bold text-orange-700">
                {developmentLevels.length}
              </div>
              <div className="text-sm text-gray-700">Development Levels</div>
            </div>
          </div>
        </motion.div>

        {/* Controls */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-xl shadow-lg p-6 mb-8"
        >
          <h2 className="text-2xl font-semibold mb-4 text-gray-900">Analysis Controls</h2>
          <div className="flex flex-wrap gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Development Level</label>
              <select
                value={filterLevel}
                onChange={(e) => setFilterLevel(e.target.value)}
                className="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white text-gray-900"
              >
                <option value="all">All Levels</option>
                {developmentLevels.map(level => (
                  <option key={level} value={level}>{level}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Chart Type</label>
              <select
                value={selectedChart}
                onChange={(e) => setSelectedChart(e.target.value)}
                className="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white text-gray-900"
              >
                <option value="overview">GDP Growth Overview</option>
                <option value="recovery">Recovery Rate Analysis</option>
                <option value="comparison">2020 vs 2021 Comparison</option>
                <option value="top">Top Recovery Countries</option>
              </select>
            </div>
            <div className="flex items-end">
              <button
                onClick={() => setShowReport(!showReport)}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
              >
                {showReport ? 'Hide Report' : 'Show Report'}
              </button>
            </div>
          </div>
        </motion.div>

        {/* Report Section */}
        {showReport && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-white rounded-xl shadow-lg p-6 mb-8"
          >
            <h2 className="text-2xl font-semibold mb-4 text-gray-900">Analysis Report</h2>
            <div className="prose prose-gray max-w-none">
              <h3 className="text-xl font-semibold text-gray-800 mb-3">Key Findings</h3>
              <ul className="list-disc pl-6 text-gray-700 space-y-2">
                <li>Average GDP growth in 2020: {formatNumber(validData.reduce((sum, row) => sum + (row.GDPGrowth2020 || 0), 0) / validData.filter(row => row.GDPGrowth2020).length, 2)}%</li>
                <li>Average GDP growth in 2021: {formatNumber(validData.reduce((sum, row) => sum + (row.GDPGrowth2021 || 0), 0) / validData.filter(row => row.GDPGrowth2021).length, 2)}%</li>
                <li>Countries analyzed: {validData.length}</li>
                <li>Development levels represented: {developmentLevels.length}</li>
              </ul>
              
              <h3 className="text-xl font-semibold text-gray-800 mb-3 mt-6">Recovery Patterns</h3>
              <p className="text-gray-700 mb-4">
                The analysis reveals varying recovery patterns across different development levels. 
                Countries with lower initial GDP levels often showed stronger recovery rates, 
                while developed economies experienced more gradual rebounds.
              </p>
              
              <h3 className="text-xl font-semibold text-gray-800 mb-3">Methodology</h3>
              <p className="text-gray-700">
                This analysis uses World Bank GDP growth data from 2020-2021 to assess 
                economic recovery patterns following the COVID-19 pandemic. Recovery rates 
                are calculated as the difference between 2021 and 2020 growth rates.
              </p>
            </div>
          </motion.div>
        )}

        {/* Charts */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white rounded-xl shadow-lg p-6 mb-8"
        >
          <h2 className="text-2xl font-semibold mb-4 text-gray-900">Visualizations</h2>
          
          {selectedChart === 'overview' && (
            <div className="h-96">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData.filter(row => 
                  row.GDPGrowth2020 !== null && row.GDPGrowth2021 !== null
                ).slice(0, 20)}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis dataKey="Country" stroke="#374151" />
                  <YAxis stroke="#374151" />
                  <Tooltip 
                    formatter={(value, name) => [
                      typeof value === 'number' ? formatNumber(value, 2) : value,
                      name
                    ]}
                    contentStyle={{ backgroundColor: 'white', border: '1px solid #e5e7eb' }}
                  />
                  <Legend />
                  <Bar dataKey="GDPGrowth2020" fill="#ef4444" name="GDP Growth 2020" />
                  <Bar dataKey="GDPGrowth2021" fill="#10b981" name="GDP Growth 2021" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}

          {selectedChart === 'recovery' && (
            <div className="h-96">
              <ResponsiveContainer width="100%" height="100%">
                <ScatterChart data={chartData.filter(row => 
                  row.RecoveryRate !== 'N/A' && typeof row.RecoveryRate === 'number'
                )}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis 
                    dataKey="GDPGrowth2020" 
                    name="GDP Growth 2020"
                    type="number"
                    stroke="#374151"
                  />
                  <YAxis 
                    dataKey="RecoveryRate" 
                    name="Recovery Rate"
                    type="number"
                    stroke="#374151"
                  />
                  <Tooltip 
                    formatter={(value, name) => [
                      typeof value === 'number' ? formatNumber(value, 2) : value,
                      name
                    ]}
                    contentStyle={{ backgroundColor: 'white', border: '1px solid #e5e7eb' }}
                  />
                  <Legend />
                  <Scatter 
                    dataKey="RecoveryRate" 
                    fill="#3b82f6" 
                    name="Recovery Rate vs 2020 Growth"
                  />
                </ScatterChart>
              </ResponsiveContainer>
            </div>
          )}

          {selectedChart === 'comparison' && (
            <div className="h-96">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData.filter(row => 
                  row.GDPGrowth2020 !== null && row.GDPGrowth2021 !== null
                ).slice(0, 30)}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis dataKey="Country" stroke="#374151" />
                  <YAxis stroke="#374151" />
                  <Tooltip 
                    formatter={(value, name) => [
                      typeof value === 'number' ? formatNumber(value, 2) : value,
                      name
                    ]}
                    contentStyle={{ backgroundColor: 'white', border: '1px solid #e5e7eb' }}
                  />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="GDPGrowth2020" 
                    stroke="#ef4444" 
                    strokeWidth={2}
                    dot={{ fill: '#ef4444', strokeWidth: 2, r: 4 }}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="GDPGrowth2021" 
                    stroke="#10b981" 
                    strokeWidth={2}
                    dot={{ fill: '#10b981', strokeWidth: 2, r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}

          {selectedChart === 'top' && (
            <div className="h-96">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData
                  .filter(row => row.RecoveryRate !== 'N/A' && typeof row.RecoveryRate === 'number')
                  .sort((a, b) => (b.RecoveryRate || 0) - (a.RecoveryRate || 0))
                  .slice(0, 15)
                }>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis dataKey="Country" stroke="#374151" />
                  <YAxis stroke="#374151" />
                  <Tooltip 
                    formatter={(value, name) => [
                      typeof value === 'number' ? formatNumber(value, 2) : value,
                      name
                    ]}
                    contentStyle={{ backgroundColor: 'white', border: '1px solid #e5e7eb' }}
                  />
                  <Legend />
                  <Bar 
                    dataKey="RecoveryRate" 
                    fill="#8b5cf6" 
                    name="Recovery Rate (%)"
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}
        </motion.div>

        {/* Data Table */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-white rounded-xl shadow-lg p-6"
        >
          <h2 className="text-2xl font-semibold mb-4 text-gray-900">Data Table</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Country</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">GDP Growth 2020</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">GDP Growth 2021</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Recovery Rate</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Development Level</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {chartData.slice(0, 10).map((row, index) => (
                  <tr key={index} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{row.Country}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                      {formatNumber(row.GDPGrowth2020, 2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                      {formatNumber(row.GDPGrowth2021, 2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                      {formatNumber(row.RecoveryRate, 2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                      {row.DevelopmentLevel || 'N/A'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="mt-4 text-sm text-gray-600">
            Showing first 10 rows of {chartData.length} total countries
          </div>
        </motion.div>
      </div>
    </div>
  );
} 
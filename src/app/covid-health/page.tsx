'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  BarChart, Bar, ScatterChart, Scatter, PieChart, Pie, Cell
} from 'recharts';

export default function CovidHealthPage() {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedChart, setSelectedChart] = useState('scatter');
  const [filterRegion, setFilterRegion] = useState('all');

  useEffect(() => {
    fetch('/api/covid-health-data')
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
    if (filterRegion === 'all') return true;
    return row.Development_Level === filterRegion;
  });

  const validData = filteredData.filter(row => 
    row.REF_AREA != null && 
    (row.Total_Cases != null || row.Total_Deaths != null || row.Case_Fatality_Rate != null)
  );

  const chartData = validData.map(row => ({
    ...row,
    Country: row.REF_AREA,
    TotalCases: row.Total_Cases || 'N/A',
    TotalDeaths: row.Total_Deaths || 'N/A',
    CaseFatalityRate: row.Case_Fatality_Rate || 'N/A',
    COVIDPerformanceScore: row.COVID_Performance_Score || 'N/A',
    HealthExpenditure: row.HealthExpenditure || 'N/A',
    DevelopmentLevel: row.Development_Level || 'N/A'
  }));

  const regions = [...new Set(data.map(row => row.Development_Level).filter(Boolean))];

  // Helper function to safely format numbers
  const formatNumber = (value: any, decimals: number = 0) => {
    if (value === null || value === undefined || value === 'N/A') return 'N/A';
    if (typeof value === 'number') {
      if (value >= 1000000) return (value / 1000000).toFixed(decimals) + 'M';
      if (value >= 1000) return (value / 1000).toFixed(decimals) + 'K';
      return value.toFixed(decimals);
    }
    return 'N/A';
  };

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-xl">Loading COVID-19 Health Impact Analysis...</div>
    </div>
  );
  
  if (error) return (
    <div className="min-h-screen flex items-center justify-center text-red-600">
      {error}
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <Link href="/" className="text-blue-700 hover:underline mb-4 inline-block font-medium">
          ← Back to Home
        </Link>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold text-gray-900 mb-2">COVID-19 Health Impact Analysis</h1>
          <p className="text-gray-700">Comprehensive analysis of COVID-19 impact on global health systems</p>
        </motion.div>

        {/* Data Summary */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-xl shadow-lg p-6 mb-8"
        >
          <h2 className="text-2xl font-semibold mb-4">Data Overview</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-blue-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">{validData.length}</div>
              <div className="text-sm text-gray-600">Countries with Data</div>
            </div>
            <div className="bg-red-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-red-600">
                {validData.filter(row => row.TotalCases !== null && row.TotalCases !== 'N/A').length}
              </div>
              <div className="text-sm text-gray-600">Countries with Case Data</div>
            </div>
            <div className="bg-green-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-green-600">
                {validData.filter(row => row.TotalRecovered !== null && row.TotalRecovered !== 'N/A').length}
              </div>
              <div className="text-sm text-gray-600">Countries with Recovery Data</div>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">
                {regions.length}
              </div>
              <div className="text-sm text-gray-600">Regions</div>
            </div>
          </div>
        </motion.div>

        {/* Filters */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-xl shadow-lg p-6 mb-8"
        >
          <h2 className="text-2xl font-semibold mb-4">Filters & Controls</h2>
          <div className="flex flex-wrap gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Region</label>
              <select
                value={filterRegion}
                onChange={(e) => setFilterRegion(e.target.value)}
                className="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="all">All Regions</option>
                {regions.map(region => (
                  <option key={region} value={region}>{region}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Chart Type</label>
              <select
                value={selectedChart}
                onChange={(e) => setSelectedChart(e.target.value)}
                className="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="scatter">Cases vs Deaths</option>
                <option value="bar">Top Countries by Cases</option>
                <option value="line">Recovery Rate</option>
                <option value="pie">Regional Distribution</option>
              </select>
            </div>
          </div>
        </motion.div>

        {/* Charts */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white rounded-xl shadow-lg p-6 mb-8"
        >
          <h2 className="text-2xl font-semibold mb-4">Visualizations</h2>
          
          {selectedChart === 'scatter' && (
            <div className="h-96">
              <ResponsiveContainer width="100%" height="100%">
                <ScatterChart data={chartData.filter(row => 
                  row.TotalCases !== 'N/A' && row.TotalDeaths !== 'N/A' && 
                  typeof row.TotalCases === 'number' && typeof row.TotalDeaths === 'number'
                )}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis 
                    dataKey="TotalCases" 
                    name="Total Cases"
                    type="number"
                    domain={['dataMin', 'dataMax']}
                    stroke="#374151"
                  />
                  <YAxis 
                    dataKey="TotalDeaths" 
                    name="Total Deaths"
                    type="number"
                    domain={['dataMin', 'dataMax']}
                    stroke="#374151"
                  />
                  <Tooltip 
                    formatter={(value, name) => [
                      typeof value === 'number' ? formatNumber(value) : value,
                      name
                    ]}
                  />
                  <Legend />
                  <Scatter 
                    dataKey="TotalDeaths" 
                    fill="#ef4444" 
                    name="Cases vs Deaths"
                  />
                </ScatterChart>
              </ResponsiveContainer>
            </div>
          )}

          {selectedChart === 'bar' && (
            <div className="h-96">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData
                  .filter(row => row.TotalCases !== 'N/A' && typeof row.TotalCases === 'number')
                  .sort((a, b) => b.TotalCases - a.TotalCases)
                  .slice(0, 15)
                }>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="Country" />
                  <YAxis />
                  <Tooltip 
                    formatter={(value, name) => [
                      typeof value === 'number' ? formatNumber(value) : value,
                      name
                    ]}
                  />
                  <Legend />
                  <Bar dataKey="TotalCases" fill="#3b82f6" name="Total Cases" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}

          {selectedChart === 'line' && (
            <div className="h-96">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData
                  .filter(row => 
                    row.TotalRecovered !== 'N/A' && row.TotalCases !== 'N/A' &&
                    typeof row.TotalRecovered === 'number' && typeof row.TotalCases === 'number'
                  )
                  .map(row => ({
                    ...row,
                    RecoveryRate: row.TotalCases > 0 ? (row.TotalRecovered / row.TotalCases) * 100 : 0
                  }))
                  .sort((a, b) => b.RecoveryRate - a.RecoveryRate)
                  .slice(0, 20)
                }>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="Country" />
                  <YAxis />
                  <Tooltip 
                    formatter={(value, name) => [
                      typeof value === 'number' ? value.toFixed(2) + '%' : value,
                      name
                    ]}
                  />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="RecoveryRate" 
                    stroke="#10b981" 
                    strokeWidth={2}
                    dot={{ fill: '#10b981', strokeWidth: 2, r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}

          {selectedChart === 'pie' && (
            <div className="h-96">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={regions.map(region => {
                      const regionData = chartData.filter(row => row.Region === region);
                      const totalCases = regionData.reduce((sum, row) => 
                        sum + (typeof row.TotalCases === 'number' ? row.TotalCases : 0), 0
                      );
                      return { name: region, value: totalCases };
                    }).filter(item => item.value > 0)}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${((percent || 0) * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {regions.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#ff0000'][index % 5]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => [formatNumber(value), 'Total Cases']} />
                </PieChart>
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
          <h2 className="text-2xl font-semibold mb-4">Data Table</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Country</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Region</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total Cases</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total Deaths</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total Recovered</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Active Cases</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Population</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {chartData.slice(0, 10).map((row, index) => (
                  <tr key={index} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{row.Country}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{row.Region || 'N/A'}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatNumber(row.TotalCases)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatNumber(row.TotalDeaths)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatNumber(row.TotalRecovered)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatNumber(row.ActiveCases)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatNumber(row.Population)}
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
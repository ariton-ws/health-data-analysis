'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  BarChart, Bar, ScatterChart, Scatter, PieChart, Pie, Cell
} from 'recharts';

export default function AdvancedHealthPage() {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedChart, setSelectedChart] = useState('scatter');
  const [filterGDP, setFilterGDP] = useState('all');

  useEffect(() => {
    fetch('/api/advanced-health-data')
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
    if (filterGDP === 'all') return true;
    return row.GDPGroup === filterGDP;
  });

  const validData = filteredData.filter(row => 
    row.HealthExpenditure != null && 
    row.LifeExpectancy != null && 
    row.GDPPerCapita != null
  );

  const chartData = validData.map(row => ({
    ...row,
    // Handle null values for display
    PhysiciansPer1000: row.PhysiciansPer1000 || 'N/A',
    HospitalBedsPer1000: row.HospitalBedsPer1000 || 'N/A',
    InfantMortality: row.InfantMortality || 'N/A'
  }));

  const gdpGroups = [...new Set(data.map(row => row.GDPGroup).filter(Boolean))];

  // Helper function to safely format numbers
  const formatNumber = (value: any, decimals: number = 2) => {
    if (value === null || value === undefined || value === 'N/A') return 'N/A';
    if (typeof value === 'number') return value.toFixed(decimals);
    return 'N/A';
  };

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-xl">Loading Advanced Health Analytics...</div>
    </div>
  );
  
  if (error) return (
    <div className="min-h-screen flex items-center justify-center text-red-600">
      {error}
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <Link href="/" className="text-blue-700 hover:underline mb-4 inline-block font-medium">
          ← Back to Home
        </Link>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Advanced Health Analytics</h1>
          <p className="text-gray-700">Comprehensive health system efficiency analysis across countries</p>
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
              <div className="text-sm text-gray-600">Countries with Complete Data</div>
            </div>
            <div className="bg-green-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-green-600">
                {validData.filter(row => row.PhysiciansPer1000 !== null && row.PhysiciansPer1000 !== 'N/A').length}
              </div>
              <div className="text-sm text-gray-600">Countries with Physician Data</div>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">
                {validData.filter(row => row.HospitalBedsPer1000 !== null && row.HospitalBedsPer1000 !== 'N/A').length}
              </div>
              <div className="text-sm text-gray-600">Countries with Hospital Bed Data</div>
            </div>
            <div className="bg-orange-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-orange-600">
                {gdpGroups.length}
              </div>
              <div className="text-sm text-gray-600">GDP Groups</div>
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
              <label className="block text-sm font-medium text-gray-700 mb-2">GDP Group</label>
              <select
                value={filterGDP}
                onChange={(e) => setFilterGDP(e.target.value)}
                className="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="all">All Countries</option>
                {gdpGroups.map(group => (
                  <option key={group} value={group}>{group}</option>
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
                <option value="scatter">Health vs GDP Scatter</option>
                <option value="efficiency">Efficiency vs Expenditure</option>
                <option value="life">Life Expectancy vs Expenditure</option>
                <option value="gdp">GDP Distribution</option>
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
                <ScatterChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="GDPPerCapita" 
                    name="GDP per Capita"
                    type="number"
                    domain={['dataMin', 'dataMax']}
                  />
                  <YAxis 
                    dataKey="LifeExpectancy" 
                    name="Life Expectancy"
                    type="number"
                    domain={['dataMin', 'dataMax']}
                  />
                  <Tooltip 
                    formatter={(value, name) => [
                      typeof value === 'number' ? value.toFixed(2) : value,
                      name
                    ]}
                  />
                  <Legend />
                  <Scatter 
                    dataKey="LifeExpectancy" 
                    fill="#8884d8" 
                    name="Life Expectancy vs GDP"
                  />
                </ScatterChart>
              </ResponsiveContainer>
            </div>
          )}

          {selectedChart === 'efficiency' && (
            <div className="h-96">
              <ResponsiveContainer width="100%" height="100%">
                <ScatterChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="HealthExpenditure" 
                    name="Health Expenditure (%)"
                    type="number"
                    domain={['dataMin', 'dataMax']}
                  />
                  <YAxis 
                    dataKey="EfficiencyScore" 
                    name="Efficiency Score"
                    type="number"
                    domain={['dataMin', 'dataMax']}
                  />
                  <Tooltip 
                    formatter={(value, name) => [
                      typeof value === 'number' ? value.toFixed(2) : value,
                      name
                    ]}
                  />
                  <Legend />
                  <Scatter 
                    dataKey="EfficiencyScore" 
                    fill="#82ca9d" 
                    name="Efficiency vs Expenditure"
                  />
                </ScatterChart>
              </ResponsiveContainer>
            </div>
          )}

          {selectedChart === 'life' && (
            <div className="h-96">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="HealthExpenditure" 
                    name="Health Expenditure (%)"
                    type="number"
                  />
                  <YAxis 
                    dataKey="LifeExpectancy" 
                    name="Life Expectancy"
                    type="number"
                  />
                  <Tooltip 
                    formatter={(value, name) => [
                      typeof value === 'number' ? value.toFixed(2) : value,
                      name
                    ]}
                  />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="LifeExpectancy" 
                    stroke="#8884d8" 
                    strokeWidth={2}
                    dot={{ fill: '#8884d8', strokeWidth: 2, r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}

          {selectedChart === 'gdp' && (
            <div className="h-96">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="REF_AREA" />
                  <YAxis />
                  <Tooltip 
                    formatter={(value, name) => [
                      typeof value === 'number' ? value.toFixed(2) : value,
                      name
                    ]}
                  />
                  <Legend />
                  <Bar dataKey="GDPPerCapita" fill="#8884d8" name="GDP per Capita" />
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
          <h2 className="text-2xl font-semibold mb-4">Data Table</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Country</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Health Exp (%)</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Life Expectancy</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Infant Mortality</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Physicians/1000</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Hospital Beds/1000</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">GDP per Capita</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Efficiency Score</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {chartData.slice(0, 10).map((row, index) => (
                  <tr key={index} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{row.REF_AREA}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatNumber(row.HealthExpenditure, 2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatNumber(row.LifeExpectancy, 1)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatNumber(row.InfantMortality, 1)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatNumber(row.PhysiciansPer1000, 2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatNumber(row.HospitalBedsPer1000, 2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatNumber(row.GDPPerCapita, 0)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatNumber(row.EfficiencyScore, 2)}
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
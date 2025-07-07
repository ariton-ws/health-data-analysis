'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  BarChart, Bar, ScatterChart, Scatter, PieChart, Pie, Cell
} from 'recharts';

export default function DataExplorerPage() {
  const [gdpData, setGdpData] = useState<any[]>([]);
  const [covidData, setCovidData] = useState<any[]>([]);
  const [advancedData, setAdvancedData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedDataset, setSelectedDataset] = useState('gdp');
  const [selectedChart, setSelectedChart] = useState('overview');

  useEffect(() => {
    const loadAllData = async () => {
      try {
        const [gdpRes, covidRes, advancedRes] = await Promise.all([
          fetch('/api/gdp-recovery-data'),
          fetch('/api/covid-health-data'),
          fetch('/api/advanced-health-data')
        ]);

        const gdp = await gdpRes.json();
        const covid = await covidRes.json();
        const advanced = await advancedRes.json();

        if (Array.isArray(gdp) && Array.isArray(covid) && Array.isArray(advanced)) {
          setGdpData(gdp.filter(row => {
            const nullCount = Object.values(row).filter(val => val === null).length;
            return nullCount < 3;
          }));
          setCovidData(covid.filter(row => {
            const nullCount = Object.values(row).filter(val => val === null).length;
            return nullCount < 3;
          }));
          setAdvancedData(advanced.filter(row => {
            const nullCount = Object.values(row).filter(val => val === null).length;
            return nullCount < 3;
          }));
        } else {
          setError('Invalid data format');
        }
        setLoading(false);
      } catch (err) {
        setError('Failed to load data');
        setLoading(false);
      }
    };

    loadAllData();
  }, []);

  const currentData = selectedDataset === 'gdp' ? gdpData : 
                     selectedDataset === 'covid' ? covidData : advancedData;

  const validData = currentData.filter(row => {
    if (selectedDataset === 'gdp') {
      return row.Country != null && (row.GDPGrowth2020 != null || row.GDPGrowth2021 != null);
    } else if (selectedDataset === 'covid') {
      return row.Country != null && (row.TotalCases != null || row.TotalDeaths != null);
    } else {
      return row.REF_AREA != null && (row.HealthExpenditure != null || row.LifeExpectancy != null);
    }
  });

  // Helper function to safely format numbers
  const formatNumber = (value: any, decimals: number = 2) => {
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
      <div className="text-xl">Loading Data Explorer...</div>
    </div>
  );
  
  if (error) return (
    <div className="min-h-screen flex items-center justify-center text-red-600">
      {error}
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-red-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <Link href="/" className="text-blue-700 hover:underline mb-4 inline-block font-medium">
          ← Back to Home
        </Link>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Data Explorer</h1>
          <p className="text-gray-700">Interactive exploration of all health and economic datasets</p>
        </motion.div>

        {/* Dataset Summary */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-xl shadow-lg p-6 mb-8"
        >
          <h2 className="text-2xl font-semibold mb-4">Dataset Overview</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-blue-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">{gdpData.length}</div>
              <div className="text-sm text-gray-600">GDP Recovery Records</div>
            </div>
            <div className="bg-green-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-green-600">{covidData.length}</div>
              <div className="text-sm text-gray-600">COVID-19 Records</div>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">{advancedData.length}</div>
              <div className="text-sm text-gray-600">Advanced Health Records</div>
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
          <h2 className="text-2xl font-semibold mb-4">Exploration Controls</h2>
          <div className="flex flex-wrap gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Dataset</label>
              <select
                value={selectedDataset}
                onChange={(e) => setSelectedDataset(e.target.value)}
                className="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="gdp">GDP Recovery Data</option>
                <option value="covid">COVID-19 Data</option>
                <option value="advanced">Advanced Health Data</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Chart Type</label>
              <select
                value={selectedChart}
                onChange={(e) => setSelectedChart(e.target.value)}
                className="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="overview">Data Overview</option>
                <option value="distribution">Value Distribution</option>
                <option value="correlation">Correlation Analysis</option>
                <option value="top">Top Countries</option>
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
          <h2 className="text-2xl font-semibold mb-4">Data Visualizations</h2>
          
          {selectedChart === 'overview' && (
            <div className="h-96">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={validData.slice(0, 20)}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey={selectedDataset === 'gdp' ? 'Country' : selectedDataset === 'covid' ? 'Country' : 'REF_AREA'} />
                  <YAxis />
                  <Tooltip 
                    formatter={(value, name) => [
                      typeof value === 'number' ? formatNumber(value) : value,
                      name
                    ]}
                  />
                  <Legend />
                  {selectedDataset === 'gdp' && (
                    <>
                      <Bar dataKey="GDPGrowth2020" fill="#ef4444" name="GDP Growth 2020" />
                      <Bar dataKey="GDPGrowth2021" fill="#10b981" name="GDP Growth 2021" />
                    </>
                  )}
                  {selectedDataset === 'covid' && (
                    <>
                      <Bar dataKey="TotalCases" fill="#3b82f6" name="Total Cases" />
                      <Bar dataKey="TotalDeaths" fill="#ef4444" name="Total Deaths" />
                    </>
                  )}
                  {selectedDataset === 'advanced' && (
                    <>
                      <Bar dataKey="HealthExpenditure" fill="#8b5cf6" name="Health Expenditure %" />
                      <Bar dataKey="LifeExpectancy" fill="#f59e0b" name="Life Expectancy" />
                    </>
                  )}
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}

          {selectedChart === 'distribution' && (
            <div className="h-96">
              <ResponsiveContainer width="100%" height="100%">
                <ScatterChart data={validData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey={selectedDataset === 'gdp' ? 'GDPGrowth2020' : 
                            selectedDataset === 'covid' ? 'TotalCases' : 'HealthExpenditure'}
                    name={selectedDataset === 'gdp' ? 'GDP Growth 2020' : 
                          selectedDataset === 'covid' ? 'Total Cases' : 'Health Expenditure'}
                    type="number"
                  />
                  <YAxis 
                    dataKey={selectedDataset === 'gdp' ? 'GDPGrowth2021' : 
                            selectedDataset === 'covid' ? 'TotalDeaths' : 'LifeExpectancy'}
                    name={selectedDataset === 'gdp' ? 'GDP Growth 2021' : 
                          selectedDataset === 'covid' ? 'Total Deaths' : 'Life Expectancy'}
                    type="number"
                  />
                  <Tooltip 
                    formatter={(value, name) => [
                      typeof value === 'number' ? formatNumber(value) : value,
                      name
                    ]}
                  />
                  <Legend />
                  <Scatter 
                    dataKey={selectedDataset === 'gdp' ? 'GDPGrowth2021' : 
                            selectedDataset === 'covid' ? 'TotalDeaths' : 'LifeExpectancy'}
                    fill="#8884d8" 
                    name="Distribution"
                  />
                </ScatterChart>
              </ResponsiveContainer>
            </div>
          )}

          {selectedChart === 'correlation' && (
            <div className="h-96">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={validData.slice(0, 30)}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey={selectedDataset === 'gdp' ? 'Country' : selectedDataset === 'covid' ? 'Country' : 'REF_AREA'} />
                  <YAxis />
                  <Tooltip 
                    formatter={(value, name) => [
                      typeof value === 'number' ? formatNumber(value) : value,
                      name
                    ]}
                  />
                  <Legend />
                  {selectedDataset === 'gdp' && (
                    <>
                      <Line type="monotone" dataKey="GDPGrowth2020" stroke="#ef4444" strokeWidth={2} />
                      <Line type="monotone" dataKey="GDPGrowth2021" stroke="#10b981" strokeWidth={2} />
                    </>
                  )}
                  {selectedDataset === 'covid' && (
                    <>
                      <Line type="monotone" dataKey="TotalCases" stroke="#3b82f6" strokeWidth={2} />
                      <Line type="monotone" dataKey="TotalDeaths" stroke="#ef4444" strokeWidth={2} />
                    </>
                  )}
                  {selectedDataset === 'advanced' && (
                    <>
                      <Line type="monotone" dataKey="HealthExpenditure" stroke="#8b5cf6" strokeWidth={2} />
                      <Line type="monotone" dataKey="LifeExpectancy" stroke="#f59e0b" strokeWidth={2} />
                    </>
                  )}
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}

          {selectedChart === 'top' && (
            <div className="h-96">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={validData
                  .sort((a, b) => {
                    const aVal = selectedDataset === 'gdp' ? a.GDPGrowth2021 : 
                                selectedDataset === 'covid' ? a.TotalCases : a.HealthExpenditure;
                    const bVal = selectedDataset === 'gdp' ? b.GDPGrowth2021 : 
                                selectedDataset === 'covid' ? b.TotalCases : b.HealthExpenditure;
                    return (bVal || 0) - (aVal || 0);
                  })
                  .slice(0, 15)
                }>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey={selectedDataset === 'gdp' ? 'Country' : selectedDataset === 'covid' ? 'Country' : 'REF_AREA'} />
                  <YAxis />
                  <Tooltip 
                    formatter={(value, name) => [
                      typeof value === 'number' ? formatNumber(value) : value,
                      name
                    ]}
                  />
                  <Legend />
                  <Bar 
                    dataKey={selectedDataset === 'gdp' ? 'GDPGrowth2021' : 
                            selectedDataset === 'covid' ? 'TotalCases' : 'HealthExpenditure'}
                    fill="#8884d8" 
                    name={selectedDataset === 'gdp' ? 'GDP Growth 2021' : 
                          selectedDataset === 'covid' ? 'Total Cases' : 'Health Expenditure %'}
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
          <h2 className="text-2xl font-semibold mb-4">Raw Data Table</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {selectedDataset === 'gdp' ? 'Country' : selectedDataset === 'covid' ? 'Country' : 'Country Code'}
                  </th>
                  {selectedDataset === 'gdp' && (
                    <>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">GDP Growth 2020</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">GDP Growth 2021</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Recovery Rate</th>
                    </>
                  )}
                  {selectedDataset === 'covid' && (
                    <>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total Cases</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total Deaths</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total Recovered</th>
                    </>
                  )}
                  {selectedDataset === 'advanced' && (
                    <>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Health Expenditure %</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Life Expectancy</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">GDP per Capita</th>
                    </>
                  )}
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {validData.slice(0, 10).map((row, index) => (
                  <tr key={index} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {selectedDataset === 'gdp' ? row.Country : selectedDataset === 'covid' ? row.Country : row.REF_AREA}
                    </td>
                    {selectedDataset === 'gdp' && (
                      <>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {formatNumber(row.GDPGrowth2020, 2)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {formatNumber(row.GDPGrowth2021, 2)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {formatNumber(row.RecoveryRate, 2)}
                        </td>
                      </>
                    )}
                    {selectedDataset === 'covid' && (
                      <>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {formatNumber(row.TotalCases)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {formatNumber(row.TotalDeaths)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {formatNumber(row.TotalRecovered)}
                        </td>
                      </>
                    )}
                    {selectedDataset === 'advanced' && (
                      <>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {formatNumber(row.HealthExpenditure, 2)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {formatNumber(row.LifeExpectancy, 1)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {formatNumber(row.GDPPerCapita, 0)}
                        </td>
                      </>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="mt-4 text-sm text-gray-600">
            Showing first 10 rows of {validData.length} total records from {selectedDataset.toUpperCase()} dataset
          </div>
        </motion.div>
      </div>
    </div>
  );
} 
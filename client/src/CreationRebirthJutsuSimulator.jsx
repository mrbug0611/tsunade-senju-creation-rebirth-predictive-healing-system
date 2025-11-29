import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { Play, RotateCcw, AlertCircle } from 'lucide-react';

export default function CreationRebirthJutsuSimulator() {

    // const [value, setValue] = useState(initialValue);
    // manages states (data that can change over time)
    const [parameters, setParameters] = useState({
        k_activation: 0.5,
        k_healing: 2.0,
        k_stress: 0.1,
        k_decay: 0.3,
    });

    const [initialState, setInitialState] = useState({
        chakra_reserves: 1000,
        damaged_cells: 500,
        healthy_cells: 500,
    });

    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [activeTab, setActiveTab] = useState('parameters');
    const [apiUrl, setApiUrl] = useState(import.meta.env.VITE_API_URL || 'http://localhost:5000');
    // async means it can wait for something to happen without freezing the whole app
    const generateSimulation = async () => {
        setLoading(true);
        setError(null);

        try {
            // await means "pause here until this is done"
            // response is raw http response from the server
            const response = await fetch(`${apiUrl}/api/simulate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    parameters,
                    initial_states: initialState,
                }),
            });

            if (!response.ok) {
                throw new Error(`API Error: ${response.statusText}`);
            }

            // data is the parsed JSON from the response
            const data = await response.json();

            if (!data.success) {
                throw new Error(data.error || 'Simulation failed');
            }


            setResult({
                data: data.data, // accessing the 'data' field from the response
                summary: data.summary, // accessing the 'summary' field from the response
            });
        } catch (err) {
            setError(err.message);
            console.error('Simulation error:', err);
        } finally {
            setLoading(false);
        }
    }

    const handleParameterChange = (param, value) => {
        // ... spread operator to copy existing parameters
        // [param] overrides one parameter with new value
        // param = key_healing and value = '3.5' 
        // then it becomes key_healing: 3.5
        // parseFloat to convert string input to number

        setParameters({...parameters, [param]: parseFloat(value)});
    }

    const handleStateChange = (state, value) => {
        setInitialState({...initialState, [state]: parseFloat(value)});
    }

    const resetToDefaults = () => {
        setParameters({
            k_activation: 0.5,
            k_healing: 2.0,
            k_stress: 0.1,
            k_decay: 0.3,
        }); 
    
        setResult(null);
        setError(null);
    }
 return (
    <div className="min-h-screen bg-gradient-to-br from-red-900 via-purple-900 to-black p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">
            創造再生 Sōzō Saisei
          </h1>
          <p className="text-purple-300">Creation Rebirth Cellular Kinetics Simulator</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Control Panel */}
          <div className="lg:col-span-1">
            <div className="bg-gray-900 border border-purple-500 rounded-lg p-6 shadow-lg">
              {/* API Configuration */}
              <div className="mb-6 p-4 bg-gray-800 rounded border border-gray-700">
                <label className="block text-sm text-purple-300 mb-2">API URL</label>
                <input
                  type="text"
                  value={apiUrl}
                  onChange={(e) => setApiUrl(e.target.value)}
                  placeholder="http://localhost:5000"
                  className="w-full bg-gray-700 text-white px-3 py-2 rounded text-sm border border-gray-600 focus:border-purple-500 outline-none"
                />
              </div>

              <div className="flex gap-2 mb-6">
                <button
                  onClick={() => setActiveTab('parameters')}
                  className={`flex-1 py-2 px-3 rounded transition ${
                    activeTab === 'parameters'
                      ? 'bg-purple-600 text-white'
                      : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                  }`}
                >
                  Parameters
                </button>
                <button
                  onClick={() => setActiveTab('initial')}
                  className={`flex-1 py-2 px-3 rounded transition ${
                    activeTab === 'initial'
                      ? 'bg-purple-600 text-white'
                      : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                  }`}
                >
                  Initial State
                </button>
              </div>

              {/* Parameters Tab */}
              {activeTab === 'parameters' && (
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-white mb-4">Reaction Rates</h3>
                  
                  {[
                    { key: 'k_activation', label: 'Chakra Activation', hint: 'Seal release rate' },
                    { key: 'k_healing', label: 'Mitotic Healing', hint: 'Cell repair rate' },
                    { key: 'k_stress', label: 'Stress Factor', hint: 'Telomere damage rate' },
                    { key: 'k_decay', label: 'Chakra Decay', hint: 'Enzyme dissipation' }
                  ].map(param => (
                    <div key={param.key}>
                      <label className="block text-sm text-purple-300 mb-1">{param.label}</label>
                      <p className="text-xs text-gray-500 mb-2">{param.hint}</p>
                      <input
                        type="range"
                        min="0"
                        max="5"
                        step="0.1"
                        value={parameters[param.key]}
                        onChange={(e) => handleParameterChange(param.key, e.target.value)}
                        className="w-full"
                      />
                      <div className="text-right text-sm text-gray-400 mt-1">
                        {parameters[param.key].toFixed(2)}
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Initial State Tab */}
              {activeTab === 'initial' && (
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-white mb-4">Initial Conditions</h3>
                  
                  {[
                    { key: 'chakra_reserves', label: 'Chakra Reserves', max: 2000 },
                    { key: 'damaged_cells', label: 'Damaged Cells', max: 1000 },
                    { key: 'healthy_cells', label: 'Healthy Cells', max: 1000 }
                  ].map(state => (
                    <div key={state.key}>
                      <label className="block text-sm text-purple-300 mb-1">{state.label}</label>
                      <input
                        type="range"
                        min="0"
                        max={state.max}
                        step="10"
                        value={initialState[state.key]}
                        onChange={(e) => handleStateChange(state.key, e.target.value)}
                        className="w-full"
                      />
                      <div className="text-right text-sm text-gray-400 mt-1">
                        {initialState[state.key]}
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Error Message */}
              {error && (
                <div className="mt-6 p-4 bg-red-900 border border-red-600 rounded flex gap-3">
                  <AlertCircle size={20} className="text-red-400 flex-shrink-0 mt-0.5" />
                  <div>
                    <p className="text-red-200 text-sm font-semibold">Error</p>
                    <p className="text-red-300 text-xs mt-1">{error}</p>
                  </div>
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex gap-3 mt-8">
                <button
                  onClick={generateSimulation}
                  disabled={loading}
                  className="flex-1 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 disabled:opacity-50 text-white font-semibold py-2 px-4 rounded flex items-center justify-center gap-2 transition"
                >
                  <Play size={18} />
                  {loading ? 'Simulating...' : 'Run Jutsu'}
                </button>
                <button
                  onClick={resetToDefaults}
                  className="bg-gray-800 hover:bg-gray-700 text-gray-300 py-2 px-4 rounded transition"
                >
                  <RotateCcw size={18} />
                </button>
              </div>
            </div>
          </div>

          {/* Results Panel */}
          <div className="lg:col-span-2">
            {result ? (
              <div className="space-y-6">
                {/* Summary Stats */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {[
                    { label: 'Healthy Cells', value: result.summary.finalHealthy, colorClass: 'text-white' },
                    { label: 'Damaged Cells', value: result.summary.finalDamaged, colorClass: 'text-red-500' },
                    { label: 'Telomere Stress', value: result.summary.stressLevel, colorClass: 'text-white' },
                    { label: 'Status', value: result.summary.recovered ? '✓ RECOVERED' : '⚠ PARTIAL', colorClass: 'text-white' }
                  ].map((stat, idx) => (
                    <div key={idx} className="bg-gray-900 border border-purple-400 rounded p-4">
                      <p className="text-gray-400 text-xs uppercase">{stat.label}</p>
                      <p className={`text-2xl font-bold mt-1 ${stat.colorClass}`}>{stat.value}</p>
                    </div>
                  ))}
                </div>

                {/* Cell Regeneration Chart */}
                <div className="bg-gray-900 border border-purple-400 rounded p-4">
                  <h3 className="text-white font-semibold mb-4">Cellular Dynamics</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <AreaChart data={result.data}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                      <XAxis dataKey="time" stroke="#888" />
                      <YAxis stroke="#888" />
                      <Tooltip contentStyle={{ backgroundColor: '#1a1a1a', border: '1px solid #666' }} />
                      <Legend />
                      <Area type="monotone" dataKey="healthy_cells" stackId="1" stroke="#10b981" fill="#10b981" fillOpacity={0.6} />
                      <Area type="monotone" dataKey="damaged_cells" stackId="1" stroke="#ef4444" fill="#ef4444" fillOpacity={0.6} />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>

                {/* Energy and Stress Chart */}
                <div className="bg-gray-900 border border-purple-400 rounded p-4">
                  <h3 className="text-white font-semibold mb-4">Chakra & Stress Levels</h3>
                  <ResponsiveContainer width="100%" height={250}>
                    <LineChart data={result.data}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                      <XAxis dataKey="time" stroke="#888" />
                      <YAxis stroke="#888" />
                      <Tooltip contentStyle={{ backgroundColor: '#1a1a1a', border: '1px solid #666' }} />
                      <Legend />
                      <Line type="monotone" dataKey="chakra" stroke="#8b5cf6" strokeWidth={2} dot={false} />
                      <Line type="monotone" dataKey="active_enzymes" stroke="#f59e0b" strokeWidth={2} dot={false} />
                      <Line type="monotone" dataKey="telomere_stress" stroke="#ef4444" strokeWidth={2} dot={false} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>
            ) : (
              <div className="bg-gray-900 border border-purple-400 rounded p-8 h-full flex items-center justify-center">
                <div className="text-center">
                  <p className="text-gray-400 text-lg">Configure parameters and run the jutsu</p>
                  <p className="text-gray-600 text-sm mt-2">to visualize cellular regeneration dynamics</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
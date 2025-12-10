import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Car, Users, MapPin, TrendingDown, DollarSign, Zap, Sparkles, RefreshCw } from 'lucide-react';
import MapView from './components/MapView';
import StatsCard from './components/StatsCard';
import ControlPanel from './components/ControlPanel';
import ResultsPanel from './components/ResultsPanel';
import axios from 'axios';

const API_URL = 'http://localhost:5001/api';

function App() {
  const [riders, setRiders] = useState([]);
  const [drivers, setDrivers] = useState([]);
  const [optimizationResult, setOptimizationResult] = useState(null);
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [error, setError] = useState(null);
  const [showResults, setShowResults] = useState(false);

  // Generate initial sample data
  useEffect(() => {
    generateSampleData();
  }, []);

  const generateSampleData = async () => {
    try {
      const response = await axios.get(`${API_URL}/generate-sample?riders=8&drivers=3`);
      if (response.data.success) {
        setRiders(response.data.riders);
        setDrivers(response.data.drivers);
        setOptimizationResult(null);
        setShowResults(false);
        setError(null);
      }
    } catch (err) {
      setError('Failed to generate sample data. Make sure the backend server is running on port 5000.');
      console.error(err);
    }
  };

  const optimizeRides = async () => {
    if (riders.length === 0 || drivers.length === 0) {
      setError('Please add at least one rider and one driver');
      return;
    }

    setIsOptimizing(true);
    setError(null);

    try {
      const response = await axios.post(`${API_URL}/optimize`, {
        riders,
        drivers
      });

      if (response.data.success) {
        setOptimizationResult(response.data);
        setShowResults(true);
      } else {
        setError(response.data.error || 'Optimization failed');
      }
    } catch (err) {
      setError('Failed to connect to backend. Make sure the server is running on port 5000.');
      console.error(err);
    } finally {
      setIsOptimizing(false);
    }
  };

  const addRider = (pickup, dropoff) => {
    const newRider = {
      id: riders.length + 1,
      pickup,
      dropoff
    };
    setRiders([...riders, newRider]);
  };

  const addDriver = (location) => {
    const newDriver = {
      id: drivers.length + 1,
      location,
      capacity: 4
    };
    setDrivers([...drivers, newDriver]);
  };

  const removeRider = (id) => {
    setRiders(riders.filter(r => r.id !== id));
    setOptimizationResult(null);
    setShowResults(false);
  };

  const removeDriver = (id) => {
    setDrivers(drivers.filter(d => d.id !== id));
    setOptimizationResult(null);
    setShowResults(false);
  };

  const metrics = optimizationResult?.metrics;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      {/* Header */}
      <motion.header 
        className="bg-slate-900/50 backdrop-blur-lg border-b border-slate-700/50 sticky top-0 z-50"
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ type: "spring", stiffness: 100 }}
      >
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-gradient-to-br from-primary-500 to-accent-500 p-3 rounded-xl shadow-lg">
                <Car className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold gradient-text flex items-center gap-2">
                  Ride-Sharing Optimizer
                  <Sparkles className="w-6 h-6 text-accent-400" />
                </h1>
                <p className="text-sm text-slate-400">AI-Powered Carpooling Solution</p>
              </div>
            </div>
            <button
              onClick={generateSampleData}
              className="flex items-center gap-2 px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg transition-colors"
            >
              <RefreshCw className="w-4 h-4" />
              Generate Sample
            </button>
          </div>
        </div>
      </motion.header>

      {/* Error Banner */}
      <AnimatePresence>
        {error && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="bg-red-500/10 border-b border-red-500/50"
          >
            <div className="container mx-auto px-6 py-3">
              <p className="text-red-400">{error}</p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Stats Overview */}
      <div className="container mx-auto px-6 py-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <StatsCard
            icon={<Users className="w-6 h-6" />}
            title="Total Riders"
            value={riders.length}
            color="from-blue-500 to-cyan-500"
            delay={0.1}
          />
          <StatsCard
            icon={<Car className="w-6 h-6" />}
            title="Total Drivers"
            value={drivers.length}
            color="from-purple-500 to-pink-500"
            delay={0.2}
          />
          <StatsCard
            icon={<TrendingDown className="w-6 h-6" />}
            title="Savings"
            value={metrics ? `${metrics.savings_percent}%` : '--'}
            color="from-green-500 to-emerald-500"
            delay={0.3}
          />
          <StatsCard
            icon={<DollarSign className="w-6 h-6" />}
            title="Total Cost"
            value={metrics ? `$${metrics.total_cost}` : '--'}
            color="from-yellow-500 to-orange-500"
            delay={0.4}
          />
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Map */}
          <motion.div
            className="lg:col-span-2"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.5 }}
          >
            <div className="bg-slate-800/50 backdrop-blur-lg rounded-2xl p-4 shadow-2xl border border-slate-700/50">
              <MapView
                riders={riders}
                drivers={drivers}
                optimizationResult={optimizationResult}
              />
            </div>
          </motion.div>

          {/* Control Panel */}
          <motion.div
            className="lg:col-span-1"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.6 }}
          >
            <ControlPanel
              riders={riders}
              drivers={drivers}
              onOptimize={optimizeRides}
              isOptimizing={isOptimizing}
              onRemoveRider={removeRider}
              onRemoveDriver={removeDriver}
            />
          </motion.div>
        </div>

        {/* Results Panel */}
        <AnimatePresence>
          {showResults && optimizationResult && (
            <ResultsPanel result={optimizationResult} />
          )}
        </AnimatePresence>
      </div>

      {/* Footer */}
      <footer className="bg-slate-900/50 border-t border-slate-700/50 mt-12 py-6">
        <div className="container mx-auto px-6 text-center text-slate-400">
          <p className="flex items-center justify-center gap-2">
            <Zap className="w-4 h-4 text-primary-400" />
            Powered by OR-Tools, Machine Learning & React
          </p>
          <p className="text-sm mt-2">
            Optimizing rides for a better tomorrow 🌍
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;

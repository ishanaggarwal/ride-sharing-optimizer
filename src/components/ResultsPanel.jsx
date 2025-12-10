import React from 'react';
import { motion } from 'framer-motion';
import { TrendingDown, DollarSign, Route, Users, CheckCircle, ArrowRight } from 'lucide-react';

const ResultsPanel = ({ result }) => {
  const { matches, metrics } = result;

  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 50 }}
      transition={{ type: "spring", damping: 20 }}
      className="mt-6"
    >
      <div className="bg-slate-800/50 backdrop-blur-lg rounded-2xl p-6 shadow-2xl border border-slate-700/50">
        <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
          <CheckCircle className="w-6 h-6 text-green-400" />
          Optimization Results
        </h2>

        {/* Metrics Summary */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <div className="bg-gradient-to-br from-blue-500/10 to-cyan-500/10 border border-blue-500/30 rounded-xl p-4">
            <div className="flex items-center gap-2 mb-2">
              <Users className="w-5 h-5 text-blue-400" />
              <p className="text-sm text-slate-400">Riders Matched</p>
            </div>
            <p className="text-3xl font-bold">{metrics.riders_matched}</p>
            <p className="text-xs text-slate-500 mt-1">out of {metrics.total_riders}</p>
          </div>

          <div className="bg-gradient-to-br from-green-500/10 to-emerald-500/10 border border-green-500/30 rounded-xl p-4">
            <div className="flex items-center gap-2 mb-2">
              <TrendingDown className="w-5 h-5 text-green-400" />
              <p className="text-sm text-slate-400">Distance Saved</p>
            </div>
            <p className="text-3xl font-bold">{metrics.savings_percent}%</p>
            <p className="text-xs text-slate-500 mt-1">
              {(metrics.solo_distance - metrics.total_distance).toFixed(2)} km
            </p>
          </div>

          <div className="bg-gradient-to-br from-purple-500/10 to-pink-500/10 border border-purple-500/30 rounded-xl p-4">
            <div className="flex items-center gap-2 mb-2">
              <Route className="w-5 h-5 text-purple-400" />
              <p className="text-sm text-slate-400">Total Distance</p>
            </div>
            <p className="text-3xl font-bold">{metrics.total_distance}</p>
            <p className="text-xs text-slate-500 mt-1">kilometers</p>
          </div>

          <div className="bg-gradient-to-br from-yellow-500/10 to-orange-500/10 border border-yellow-500/30 rounded-xl p-4">
            <div className="flex items-center gap-2 mb-2">
              <DollarSign className="w-5 h-5 text-yellow-400" />
              <p className="text-sm text-slate-400">Cost Per Rider</p>
            </div>
            <p className="text-3xl font-bold">${metrics.cost_per_rider}</p>
            <p className="text-xs text-slate-500 mt-1">shared cost</p>
          </div>
        </div>

        {/* Matches Details */}
        <div>
          <h3 className="text-xl font-semibold mb-4">Driver Assignments</h3>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {matches.map((match, index) => (
              <motion.div
                key={match.driver_id}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1 }}
                className="bg-slate-700/50 rounded-xl p-4 border border-slate-600/50"
              >
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <div className="bg-gradient-to-br from-green-500 to-emerald-500 p-2 rounded-lg">
                      <Route className="w-5 h-5 text-white" />
                    </div>
                    <div>
                      <h4 className="font-bold">Driver {match.driver_id}</h4>
                      <p className="text-xs text-slate-400">
                        {match.riders.length} rider{match.riders.length > 1 ? 's' : ''}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-slate-400">Cost</p>
                    <p className="text-lg font-bold text-green-400">${match.cost}</p>
                  </div>
                </div>

                <div className="space-y-2 mb-3">
                  {match.riders.map((rider) => (
                    <div
                      key={rider.id}
                      className="bg-slate-800/50 rounded-lg p-2 text-sm"
                    >
                      <div className="flex items-center gap-2">
                        <Users className="w-4 h-4 text-primary-400" />
                        <span className="font-semibold">Rider {rider.id}</span>
                      </div>
                      <div className="flex items-center gap-2 text-xs text-slate-400 mt-1">
                        <span className="flex items-center gap-1">
                          <span className="w-2 h-2 bg-primary-400 rounded-full"></span>
                          Pickup
                        </span>
                        <ArrowRight className="w-3 h-3" />
                        <span className="flex items-center gap-1">
                          <span className="w-2 h-2 bg-accent-400 rounded-full"></span>
                          Dropoff
                        </span>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="flex items-center justify-between text-sm pt-3 border-t border-slate-600">
                  <span className="text-slate-400">Total Distance</span>
                  <span className="font-semibold">{match.distance} km</span>
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Environmental Impact */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="mt-6 p-4 bg-gradient-to-r from-green-500/10 to-emerald-500/10 border border-green-500/30 rounded-xl"
        >
          <h4 className="font-bold mb-2 flex items-center gap-2">
            🌍 Environmental Impact
          </h4>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
              <p className="text-slate-400">CO₂ Saved</p>
              <p className="font-bold text-green-400">
                {((metrics.solo_distance - metrics.total_distance) * 0.12).toFixed(2)} kg
              </p>
            </div>
            <div>
              <p className="text-slate-400">Money Saved</p>
              <p className="font-bold text-green-400">
                ${((metrics.solo_distance - metrics.total_distance) * 2.5).toFixed(2)}
              </p>
            </div>
            <div>
              <p className="text-slate-400">Efficiency</p>
              <p className="font-bold text-green-400">
                {metrics.savings_percent}%
              </p>
            </div>
            <div>
              <p className="text-slate-400">Cars Reduced</p>
              <p className="font-bold text-green-400">
                {metrics.total_riders - metrics.total_drivers}
              </p>
            </div>
          </div>
        </motion.div>
      </div>
    </motion.div>
  );
};

export default ResultsPanel;

import React from 'react';
import { motion } from 'framer-motion';
import { Play, Users, Car, X, Loader2 } from 'lucide-react';

const ControlPanel = ({ riders, drivers, onOptimize, isOptimizing, onRemoveRider, onRemoveDriver }) => {
  return (
    <div className="bg-slate-800/50 backdrop-blur-lg rounded-2xl p-6 shadow-2xl border border-slate-700/50 h-full">
      <h2 className="text-2xl font-bold mb-6 gradient-text">Control Panel</h2>

      {/* Optimize Button */}
      <motion.button
        onClick={onOptimize}
        disabled={isOptimizing || riders.length === 0 || drivers.length === 0}
        className={`w-full py-4 rounded-xl font-bold text-lg mb-6 flex items-center justify-center gap-2 transition-all ${
          isOptimizing || riders.length === 0 || drivers.length === 0
            ? 'bg-slate-700 text-slate-500 cursor-not-allowed'
            : 'bg-gradient-to-r from-primary-500 to-accent-500 hover:from-primary-600 hover:to-accent-600 text-white shadow-lg hover:shadow-xl'
        }`}
        whileHover={!isOptimizing && riders.length > 0 && drivers.length > 0 ? { scale: 1.02 } : {}}
        whileTap={!isOptimizing && riders.length > 0 && drivers.length > 0 ? { scale: 0.98 } : {}}
      >
        {isOptimizing ? (
          <>
            <Loader2 className="w-5 h-5 animate-spin" />
            Optimizing...
          </>
        ) : (
          <>
            <Play className="w-5 h-5" />
            Optimize Rides
          </>
        )}
      </motion.button>

      {/* Riders List */}
      <div className="mb-6">
        <div className="flex items-center gap-2 mb-3">
          <Users className="w-5 h-5 text-primary-400" />
          <h3 className="text-lg font-semibold">Riders ({riders.length})</h3>
        </div>
        <div className="space-y-2 max-h-64 overflow-y-auto custom-scrollbar">
          {riders.length === 0 ? (
            <p className="text-slate-500 text-sm text-center py-4">No riders added</p>
          ) : (
            riders.map((rider) => (
              <motion.div
                key={rider.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className="bg-slate-700/50 rounded-lg p-3 flex items-center justify-between hover:bg-slate-700 transition-colors"
              >
                <div className="flex-1">
                  <p className="font-semibold text-sm">Rider {rider.id}</p>
                  <p className="text-xs text-slate-400">
                    From {rider.pickup[0].toFixed(3)}, {rider.pickup[1].toFixed(3)}
                  </p>
                  <p className="text-xs text-slate-400">
                    To {rider.dropoff[0].toFixed(3)}, {rider.dropoff[1].toFixed(3)}
                  </p>
                </div>
                <button
                  onClick={() => onRemoveRider(rider.id)}
                  className="p-1 hover:bg-red-500/20 rounded transition-colors"
                >
                  <X className="w-4 h-4 text-red-400" />
                </button>
              </motion.div>
            ))
          )}
        </div>
      </div>

      {/* Drivers List */}
      <div>
        <div className="flex items-center gap-2 mb-3">
          <Car className="w-5 h-5 text-green-400" />
          <h3 className="text-lg font-semibold">Drivers ({drivers.length})</h3>
        </div>
        <div className="space-y-2 max-h-64 overflow-y-auto custom-scrollbar">
          {drivers.length === 0 ? (
            <p className="text-slate-500 text-sm text-center py-4">No drivers added</p>
          ) : (
            drivers.map((driver) => (
              <motion.div
                key={driver.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className="bg-slate-700/50 rounded-lg p-3 flex items-center justify-between hover:bg-slate-700 transition-colors"
              >
                <div className="flex-1">
                  <p className="font-semibold text-sm">Driver {driver.id}</p>
                  <p className="text-xs text-slate-400">
                    Location: {driver.location[0].toFixed(3)}, {driver.location[1].toFixed(3)}
                  </p>
                  <p className="text-xs text-slate-400">
                    Capacity: {driver.capacity} passengers
                  </p>
                </div>
                <button
                  onClick={() => onRemoveDriver(driver.id)}
                  className="p-1 hover:bg-red-500/20 rounded transition-colors"
                >
                  <X className="w-4 h-4 text-red-400" />
                </button>
              </motion.div>
            ))
          )}
        </div>
      </div>

      {/* Info */}
      <div className="mt-6 p-4 bg-primary-500/10 border border-primary-500/30 rounded-lg">
        <p className="text-xs text-slate-300">
          💡 <strong>Tip:</strong> Click "Generate Sample" to add random riders and drivers, 
          then click "Optimize Rides" to see the algorithm in action!
        </p>
      </div>
    </div>
  );
};

export default ControlPanel;

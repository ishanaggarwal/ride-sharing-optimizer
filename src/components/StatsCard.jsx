import React from 'react';
import { motion } from 'framer-motion';

const StatsCard = ({ icon, title, value, color, delay }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, type: "spring" }}
      className="bg-slate-800/50 backdrop-blur-lg rounded-xl p-6 shadow-xl border border-slate-700/50 hover-lift"
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-slate-400 text-sm mb-1">{title}</p>
          <p className="text-3xl font-bold text-white">{value}</p>
        </div>
        <div className={`bg-gradient-to-br ${color} p-3 rounded-lg shadow-lg`}>
          {icon}
        </div>
      </div>
    </motion.div>
  );
};

export default StatsCard;

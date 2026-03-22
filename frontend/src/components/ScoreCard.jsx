import React from 'react';
import { motion } from 'framer-motion';

const ScoreCard = ({ score }) => {
  // Determine color based on score
  const getColor = (s) => {
    if (s > 75) return 'text-emerald-500';
    if (s > 50) return 'text-amber-500';
    return 'text-rose-500';
  };

  return (
    <div className="flex flex-col items-center justify-center p-6 bg-slate-900/50 backdrop-blur-md rounded-3xl border border-white/10 shadow-2xl">
      <div className="relative w-48 h-48">
        {/* Simple Circle Gauge */}
        <svg className="w-full h-full transform -rotate-90">
          <circle
            cx="96"
            cy="96"
            r="80"
            stroke="currentColor"
            strokeWidth="12"
            fill="transparent"
            className="text-white/5"
          />
          <motion.circle
            cx="96"
            cy="96"
            r="80"
            stroke="currentColor"
            strokeWidth="12"
            strokeDasharray={2 * Math.PI * 80}
            initial={{ strokeDashoffset: 2 * Math.PI * 80 }}
            animate={{ strokeDashoffset: 2 * Math.PI * 80 * (1 - score / 100) }}
            transition={{ duration: 1.5, ease: "easeOut" }}
            fill="transparent"
            className={`${getColor(score)}`}
          />
        </svg>
        <div className="absolute top-0 left-0 w-full h-full flex items-center justify-center">
          <span className={`text-5xl font-extrabold tracking-tighter ${getColor(score)}`}>
            {score}
          </span>
        </div>
      </div>
      <h3 className="mt-4 text-slate-400 font-medium uppercase tracking-widest text-xs">
        Match Confidence Score
      </h3>
    </div>
  );
};

export default ScoreCard;

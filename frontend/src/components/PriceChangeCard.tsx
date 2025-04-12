import React from "react";
import { motion } from "framer-motion";

interface PriceChangeCardProps {
  percentage: number;
  symbol: string;
}

const PriceChangeCard: React.FC<PriceChangeCardProps> = ({
  percentage,
  symbol,
}) => {
  const isPositive = percentage >= 0;
  const colorClass = isPositive ? "text-green-400" : "text-red-400";
  const bgColorClass = isPositive ? "bg-green-500/10" : "bg-red-500/10";
  const borderColorClass = isPositive
    ? "border-green-500/20"
    : "border-red-500/20";
  const arrow = isPositive ? "↑" : "↓";

  return (
    <motion.div
      initial={{ scale: 0.95, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.3 }}
      className={`${bgColorClass} p-6 rounded-2xl border ${borderColorClass} backdrop-blur-sm shadow-xl`}
    >
      <div className="flex items-center justify-between">
        <div className="space-y-1">
          <h3 className="text-xl font-bold text-black flex items-center gap-2">
            {symbol}
            <span className="text-sm font-normal text-gray-400">ETF</span>
          </h3>
          <p className="text-sm text-black">Today's Change</p>
        </div>
        <motion.div
          initial={{ scale: 0.9 }}
          animate={{ scale: 1 }}
          transition={{
            type: "spring",
            stiffness: 200,
            damping: 10,
          }}
          className={`text-3xl font-bold ${colorClass} flex items-center gap-1`}
        >
          <span className="text-2xl">{arrow}</span>
          <span>{Math.abs(percentage).toFixed(2)}%</span>
        </motion.div>
      </div>

      {/* Progress bar */}
      <div className="mt-4 bg-gray-700/30 h-2 rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${Math.min(Math.abs(percentage) * 5, 100)}%` }}
          transition={{ duration: 0.5, ease: "easeOut" }}
          className={`h-full rounded-full ${
            isPositive ? "bg-green-400/50" : "bg-red-400/50"
          }`}
        />
      </div>
    </motion.div>
  );
};

export default PriceChangeCard;

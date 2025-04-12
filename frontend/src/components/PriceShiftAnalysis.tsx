import React from "react";
import { Card, Title } from "@tremor/react";
import { motion } from "framer-motion";

interface PriceData {
  date: string;
  price: number;
  volume: number;
}

interface PriceShiftAnalysisProps {
  data: PriceData[];
  symbol: string;
}

const PriceShiftAnalysis: React.FC<PriceShiftAnalysisProps> = ({
  data,
  symbol,
}) => {
  // Calculate percentage changes
  const calculateChanges = () => {
    if (data.length < 2) return null;

    const latestPrice = data[data.length - 1].price;
    const previousPrice = data[data.length - 2].price;
    const weekAgoPrice = data[Math.max(0, data.length - 5)].price;
    const monthAgoPrice = data[0].price;

    return {
      daily: ((latestPrice - previousPrice) / previousPrice) * 100,
      weekly: ((latestPrice - weekAgoPrice) / weekAgoPrice) * 100,
      monthly: ((latestPrice - monthAgoPrice) / monthAgoPrice) * 100,
    };
  };

  const changes = calculateChanges();
  if (!changes) return null;

  const getColorClass = (value: number) => {
    return value >= 0 ? "text-green-600" : "text-red-600";
  };

  const getArrow = (value: number) => {
    return value >= 0 ? "↑" : "↓";
  };

  return (
    <Card className="bg-white/80 backdrop-blur-sm shadow-lg rounded-2xl border border-gray-200">
      <Title className="text-xl mb-6 text-gray-800 flex items-center gap-2">
        <span className="text-blue-600">📈</span> {symbol} Price Shifts
      </Title>

      <div className="grid grid-cols-3 gap-4">
        {/* Daily Change */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className="bg-gray-50 rounded-xl p-4 border border-gray-100"
        >
          <div className="text-sm text-gray-600 mb-1">24h Change</div>
          <div
            className={`text-lg font-bold ${getColorClass(
              changes.daily
            )} flex items-center gap-1`}
          >
            {getArrow(changes.daily)}
            {Math.abs(changes.daily).toFixed(2)}%
          </div>
        </motion.div>

        {/* Weekly Change */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.1 }}
          className="bg-gray-50 rounded-xl p-4 border border-gray-100"
        >
          <div className="text-sm text-gray-600 mb-1">Weekly Change</div>
          <div
            className={`text-lg font-bold ${getColorClass(
              changes.weekly
            )} flex items-center gap-1`}
          >
            {getArrow(changes.weekly)}
            {Math.abs(changes.weekly).toFixed(2)}%
          </div>
        </motion.div>

        {/* Monthly Change */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.2 }}
          className="bg-gray-50 rounded-xl p-4 border border-gray-100"
        >
          <div className="text-sm text-gray-600 mb-1">Monthly Change</div>
          <div
            className={`text-lg font-bold ${getColorClass(
              changes.monthly
            )} flex items-center gap-1`}
          >
            {getArrow(changes.monthly)}
            {Math.abs(changes.monthly).toFixed(2)}%
          </div>
        </motion.div>

        {/* Price Chart */}
        <div className="col-span-3 h-24 relative mt-4">
          <div className="absolute inset-0 flex items-end space-x-1">
            {data.map((item, index) => {
              const maxPrice = Math.max(...data.map((d) => d.price));
              const minPrice = Math.min(...data.map((d) => d.price));
              const range = maxPrice - minPrice;
              const height = ((item.price - minPrice) / range) * 100;
              const isPositive =
                index > 0 ? item.price >= data[index - 1].price : true;

              return (
                <motion.div
                  key={index}
                  initial={{ height: 0 }}
                  animate={{ height: `${height}%` }}
                  transition={{ duration: 0.5, delay: index * 0.05 }}
                  className={`flex-1 rounded-t-sm ${
                    isPositive ? "bg-green-500/20" : "bg-red-500/20"
                  }`}
                />
              );
            })}
          </div>
        </div>
      </div>
    </Card>
  );
};

export default PriceShiftAnalysis;

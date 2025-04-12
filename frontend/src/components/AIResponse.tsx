import React from "react";
import { motion } from "framer-motion";

interface AIResponseProps {
  content: string;
}

const AIResponse: React.FC<AIResponseProps> = ({ content }) => {
  // Split content into sections based on patterns
  const sections = content.split("\n").filter((line) => line.trim() !== "");

  const renderSection = (text: string, index: number) => {
    // Performance metrics section (matches patterns like "Current Price: $X" or "Volume: X")
    if (text.match(/^(Current Price|Change|Volume|YTD Performance):/i)) {
      const [label, value] = text.split(":").map((s) => s.trim());
      return (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
          key={index}
          className="bg-blue-50 rounded-xl p-4 shadow-sm border border-blue-100"
        >
          <div className="text-sm text-gray-600">{label}</div>
          <div className="text-lg font-semibold text-gray-100">{value}</div>
        </motion.div>
      );
    }

    // Question type identification (usually first line)
    if (text.includes("question is") || text.includes("analysis for")) {
      return (
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          key={index}
          className="text-blue-600 font-medium mb-4"
        >
          {text}
        </motion.div>
      );
    }

    // Performance summary section
    if (text.includes("Performance") && text.endsWith(":")) {
      return (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          key={index}
          className="text-lg font-semibold text-gray-100 mt-4 mb-2"
        >
          {text}
        </motion.div>
      );
    }

    // Key points or bullet points
    if (text.startsWith("-") || text.startsWith("•")) {
      return (
        <motion.div
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: index * 0.1 }}
          key={index}
          className="flex items-start gap-3 mb-2"
        >
          <div className="w-1.5 h-1.5 bg-blue-500 rounded-full mt-2 flex-shrink-0" />
          <div className="text-gray-700">{text.substring(1).trim()}</div>
        </motion.div>
      );
    }

    // Outlook or conclusion section
    if (
      text.toLowerCase().includes("outlook") ||
      text.toLowerCase().includes("conclusion")
    ) {
      return (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          key={index}
          className="bg-blue-50 border border-blue-100 rounded-xl p-4 mt-4"
        >
          <div className="font-semibold text-blue-600 mb-2">
            {text.split(":")[0]}:
          </div>
          <div className="text-gray-700">{text.split(":")[1]?.trim()}</div>
        </motion.div>
      );
    }

    // Default text formatting
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: index * 0.05 }}
        key={index}
        className="text-gray-700 mb-2"
      >
        {text}
      </motion.div>
    );
  };

  return (
    <div className="space-y-2">
      {/* Metrics Grid */}
      <div className="grid grid-cols-2 gap-3 mb-4">
        {sections
          .filter((section) =>
            section.match(/^(Current Price|Change|Volume|YTD Performance):/i)
          )
          .map((section, index) => renderSection(section, index))}
      </div>

      {/* Other Sections */}
      {sections
        .filter(
          (section) =>
            !section.match(/^(Current Price|Change|Volume|YTD Performance):/i)
        )
        .map((section, index) => renderSection(section, index))}
    </div>
  );
};

export default AIResponse;

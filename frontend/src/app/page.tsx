"use client";

import { useState } from "react";
import { Card, Title, LineChart, Text, AreaChart } from "@tremor/react";
import { motion } from "framer-motion";
import dynamic from "next/dynamic";
import PriceChangeCard from "../components/PriceChangeCard";
import AIResponse from "../components/AIResponse";
import PriceShiftAnalysis from "../components/PriceShiftAnalysis";

const CorrelationHeatmap = dynamic(
  () => import("../components/CorrelationHeatmap"),
  {
    ssr: false,
  }
);

const ParetoAnalysis = dynamic(() => import("../components/ParetoAnalysis"), {
  ssr: false,
});

const stockData = [
  { date: "2024-01", price: 350.25, volume: 25000000 },
  { date: "2024-02", price: 358.75, volume: 28000000 },
  { date: "2024-03", price: 365.5, volume: 22000000 },
  { date: "2024-04", price: 362.8, volume: 24000000 },
  { date: "2024-05", price: 370.15, volume: 26000000 },
];

interface Message {
  role: "user" | "assistant";
  content: string;
}

const formatAIResponse = (content: string) => {
  const sections = content.split("\n\n");
  return sections.map((section, index) => {
    if (section.startsWith("Article Date:")) {
      return (
        <div key={index} className="mb-4 flex items-center gap-2 text-gray-600">
          <span className="text-blue-500">📅</span>
          <span>{section.replace("Article Date:", "").trim()}</span>
        </div>
      );
    }

    if (section.startsWith("Source:")) {
      const source = section.replace("Source:", "").trim();
      return (
        <div key={index} className="mb-4 flex items-center gap-2 text-gray-600">
          <span className="text-blue-500">🔗</span>
          <a
            href={source}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 hover:underline"
          >
            {source}
          </a>
        </div>
      );
    }

    if (section.startsWith("Market Sentiment:")) {
      const sentiment = section.replace("Market Sentiment:", "").trim();
      const sentimentColor = sentiment.includes("BULLISH")
        ? "green"
        : sentiment.includes("BEARISH")
        ? "red"
        : "blue";
      return (
        <div
          key={index}
          className="mb-6 bg-white border border-gray-100 rounded-xl p-4"
        >
          <h3 className="text-lg font-semibold text-gray-800 mb-2">
            Market Sentiment
          </h3>
          <div className={`text-${sentimentColor}-500 font-medium`}>
            {sentiment}
          </div>
        </div>
      );
    }

    if (section.startsWith("Key Metrics:")) {
      const metrics = section
        .replace("Key Metrics:", "")
        .trim()
        .split("\n")
        .filter((point) => point.trim().length > 0)
        .map((point) => point.trim().replace(/^[•\-]\s*/, ""));

      return (
        <div key={index} className="mb-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-3">
            Key Metrics
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {metrics.map((metric, i) => {
              const [number, explanation] = metric.split(" - ");
              return (
                <div key={i} className="bg-blue-50 rounded-xl p-4">
                  <div className="text-xl font-bold text-blue-600 mb-1">
                    {number}
                  </div>
                  <div className="text-gray-600">{explanation}</div>
                </div>
              );
            })}
          </div>
        </div>
      );
    }

    if (section.startsWith("Impact Factors:")) {
      const factors = section
        .replace("Impact Factors:", "")
        .trim()
        .split("\n")
        .filter((point) => point.trim().length > 0)
        .map((point) => point.trim().replace(/^[•\-]\s*/, ""));

      return (
        <div key={index} className="mb-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-3">
            Impact Factors
          </h3>
          <div className="space-y-2">
            {factors.map((factor, i) => (
              <div
                key={i}
                className="flex items-start gap-3 bg-gray-50 p-4 rounded-xl"
              >
                <div className="w-1.5 h-1.5 bg-blue-500 rounded-full mt-2"></div>
                <p className="text-gray-700 flex-1">{factor}</p>
              </div>
            ))}
          </div>
        </div>
      );
    }

    if (section.startsWith("Technical Indicators:")) {
      const indicators = section
        .replace("Technical Indicators:", "")
        .trim()
        .split("\n")
        .filter((point) => point.trim().length > 0)
        .map((point) => point.trim().replace(/^[•\-]\s*/, ""));

      return (
        <div key={index} className="mb-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-3">
            Technical Indicators
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {indicators.map((indicator, i) => {
              const [name, value] = indicator.split(": ");
              return (
                <div key={i} className="bg-gray-50 rounded-xl p-4">
                  <div className="text-gray-600 mb-1">{name}</div>
                  <div className="text-lg font-semibold text-gray-800">
                    {value}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      );
    }

    if (section.startsWith("Outlook:")) {
      return (
        <div key={index} className="mb-4 bg-blue-50 p-4 rounded-xl">
          <h3 className="text-lg font-semibold text-gray-800 mb-2">Outlook</h3>
          <p className="text-gray-700">
            {section.replace("Outlook:", "").trim()}
          </p>
        </div>
      );
    }

    return null;
  });
};

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    { role: "assistant", content: "Hello, how can I assist you today?" },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [priceChange, setPriceChange] = useState<{
    percentage: number;
    symbol: string;
  } | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { role: "user" as const, content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);
    setPriceChange(null);

    try {
      const response = await fetch(
        `http://localhost:8001/analyze?question=${encodeURIComponent(input)}`
      );
      const data = await response.json();

      // Extract price change information
      const content = data.analysis.content;
      let priceChangeInfo = null;

      // Try to find specific stock change
      const changeMatch = content.match(
        /Change:\s*([+-]?\$?\d+\.?\d*)\s*\(([+-]?\d+\.?\d*)%\)/
      );
      const symbolMatch =
        content.match(/status of ([A-Z]+)/i) ||
        content.match(/([A-Z]+) Stock:/);

      if (changeMatch && symbolMatch) {
        priceChangeInfo = {
          percentage: parseFloat(changeMatch[2]),
          symbol: symbolMatch[1],
        };
      }

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.analysis.content,
        },
      ]);

      if (priceChangeInfo) {
        setPriceChange(priceChangeInfo);
      }
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Sorry, I encountered an error while processing your request.",
        },
      ]);
    }

    setIsLoading(false);
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-50 p-8">
      <div className="max-w-[1600px] mx-auto">
        <Title className="text-4xl font-bold mb-10 text-gray-800 text-center bg-clip-text">
          News Sense Dashboard
        </Title>

        <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
          {/* Left Column - Analytics */}
          <div className="space-y-6">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.3 }}
            >
              <Card className="bg-white/80 backdrop-blur-sm shadow-lg rounded-2xl border border-gray-200">
                <Title className="text-xl mb-6 text-gray-800 flex items-center gap-2">
                  <span className="text-blue-600">📊</span> Market Analysis
                </Title>
                <ParetoAnalysis />
              </Card>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.4 }}
            >
              <PriceShiftAnalysis data={stockData} symbol="QQQ" />
            </motion.div>
          </div>

          {/* Right Column - Chat Interface */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
            className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg p-6 flex flex-col h-[calc(100vh-8rem)] border border-gray-200"
          >
            <div className="bg-gradient-to-r from-blue-500/10 to-blue-400/5 px-6 py-4 rounded-xl mb-6 flex items-center gap-3 border border-blue-200">
              <span className="text-2xl">💬</span>
              <div>
                <h2 className="font-semibold text-lg text-gray-800">
                  Chat with Myfi
                </h2>
                <p className="text-sm text-gray-600">
                  Your AI Financial Analyst
                </p>
              </div>
            </div>

            <div className="flex-1 overflow-y-auto space-y-6 mb-6 pr-4 custom-scrollbar">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex ${
                    message.role === "user" ? "justify-end" : "justify-start"
                  } w-full`}
                >
                  {message.role === "assistant" && (
                    <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center mr-3 flex-shrink-0">
                      <span className="text-lg">🤖</span>
                    </div>
                  )}
                  <div
                    className={`${
                      message.role === "user" ? "ml-auto" : ""
                    } max-w-[85%]`}
                  >
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.3 }}
                      className={`rounded-2xl p-4 ${
                        message.role === "user"
                          ? "bg-gradient-to-r from-blue-600 to-blue-500 text-white shadow-md ml-auto"
                          : "bg-gray-50 border border-gray-200 text-gray-800 shadow-md"
                      }`}
                    >
                      {message.role === "assistant" ? (
                        <AIResponse content={message.content} />
                      ) : (
                        <div className="text-white">{message.content}</div>
                      )}
                    </motion.div>
                    <div
                      className={`text-xs text-gray-500 mt-1 ${
                        message.role === "user" ? "text-right" : "text-left"
                      }`}
                    >
                      {message.role === "user" ? "You" : "Myfi AI"}
                    </div>
                  </div>
                  {message.role === "user" && (
                    <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center ml-3 flex-shrink-0">
                      <span className="text-sm">👤</span>
                    </div>
                  )}
                </div>
              ))}
              {isLoading && (
                <div className="flex justify-start items-start">
                  <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center mr-3">
                    <span className="text-lg">🤖</span>
                  </div>
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="bg-gray-50 text-gray-800 rounded-2xl p-4 shadow-md border border-gray-200"
                  >
                    <div className="flex items-center gap-3">
                      <div className="flex space-x-1">
                        <motion.div
                          animate={{
                            scale: [1, 1.2, 1],
                            opacity: [1, 0.5, 1],
                          }}
                          transition={{
                            duration: 1,
                            repeat: Infinity,
                            repeatDelay: 0.2,
                          }}
                          className="w-2 h-2 bg-blue-500 rounded-full"
                        />
                        <motion.div
                          animate={{
                            scale: [1, 1.2, 1],
                            opacity: [1, 0.5, 1],
                          }}
                          transition={{
                            duration: 1,
                            repeat: Infinity,
                            repeatDelay: 0.2,
                            delay: 0.2,
                          }}
                          className="w-2 h-2 bg-blue-500 rounded-full"
                        />
                        <motion.div
                          animate={{
                            scale: [1, 1.2, 1],
                            opacity: [1, 0.5, 1],
                          }}
                          transition={{
                            duration: 1,
                            repeat: Infinity,
                            repeatDelay: 0.2,
                            delay: 0.4,
                          }}
                          className="w-2 h-2 bg-blue-500 rounded-full"
                        />
                      </div>
                      <span>Analyzing market data...</span>
                    </div>
                  </motion.div>
                </div>
              )}
            </div>

            {priceChange && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mb-6"
              >
                <PriceChangeCard
                  percentage={priceChange.percentage}
                  symbol={priceChange.symbol}
                />
              </motion.div>
            )}

            <form onSubmit={handleSubmit} className="mt-auto">
              <div className="flex gap-3">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Ask about market trends..."
                  className="flex-1 p-4 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-gray-800 placeholder-gray-400"
                  disabled={isLoading}
                />
                <button
                  type="submit"
                  disabled={isLoading}
                  className="bg-gradient-to-r from-blue-600 to-blue-500 text-white px-8 py-4 rounded-xl hover:from-blue-700 hover:to-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 transition-all duration-200 font-medium shadow-md"
                >
                  Send
                </button>
              </div>
            </form>
          </motion.div>
        </div>
      </div>
    </main>
  );
}

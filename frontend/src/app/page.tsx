"use client";

import { useState } from "react";
import { Card, Title, LineChart, Text, AreaChart } from "@tremor/react";
import { motion } from "framer-motion";

const dummyData = [
  { date: "2024-01", value: 18000, volume: 1200 },
  { date: "2024-02", value: 17800, volume: 1400 },
  { date: "2024-03", value: 18200, volume: 1100 },
  { date: "2024-04", value: 18100, volume: 1300 },
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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Add user message
    const userMessage = { role: "user" as const, content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch(
        `http://localhost:8001/analyze?question=${encodeURIComponent(input)}`
      );
      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.analysis,
        },
      ]);
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
    <main className="container mx-auto p-6 min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      <Title className="text-3xl font-bold mb-8 text-indigo-900 text-center">
        News Sense Analytics Dashboard
      </Title>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Left Column - Analytics */}
        <div className="space-y-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <Card className="bg-white shadow-xl rounded-xl">
              <Title className="text-xl mb-4">📈 Market Trends</Title>
              <LineChart
                data={dummyData}
                index="date"
                categories={["value"]}
                colors={["blue"]}
                className="h-72"
                showAnimation={true}
                showLegend={false}
                showGridLines={false}
                showYAxis={true}
              />
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <Card className="bg-white shadow-xl rounded-xl">
              <div className="grid grid-cols-2 gap-6">
                <div className="p-4 bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl">
                  <Text className="text-blue-800">🌡️ Temperature</Text>
                  <Title className="mt-2 text-2xl text-blue-900">23°C</Title>
                </div>
                <div className="p-4 bg-gradient-to-br from-green-50 to-green-100 rounded-xl">
                  <Text className="text-green-800">💰 Market Status</Text>
                  <Title className="mt-2 text-2xl text-green-900">Active</Title>
                </div>
              </div>
              <div className="mt-6">
                <Text className="text-lg font-semibold mb-3">
                  Trading Volume
                </Text>
                <AreaChart
                  data={dummyData}
                  index="date"
                  categories={["volume"]}
                  colors={["indigo"]}
                  className="h-32"
                  showAnimation={true}
                  showLegend={false}
                  showGridLines={false}
                />
              </div>
            </Card>
          </motion.div>
        </div>

        {/* Right Column - Chat Interface */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
          className="bg-white rounded-xl shadow-xl p-6 flex flex-col h-[calc(100vh-8rem)]"
        >
          <div className="bg-gradient-to-r from-blue-100 to-blue-50 text-blue-800 px-6 py-3 rounded-xl mb-6 flex items-center">
            <span className="text-xl mr-2">💬</span>
            <span className="font-semibold">Chat with N</span>
          </div>

          <div className="flex-1 overflow-y-auto space-y-6 mb-6 pr-4 custom-scrollbar">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex ${
                  message.role === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`max-w-[85%] rounded-xl p-4 ${
                    message.role === "user"
                      ? "bg-gradient-to-r from-blue-500 to-blue-600 text-white"
                      : "bg-gradient-to-r from-gray-50 to-gray-100 text-gray-800"
                  }`}
                >
                  {message.role === "assistant" && message.content ? (
                    typeof message.content === "string" &&
                    message.content.includes("Market Sentiment:") ? (
                      formatAIResponse(message.content)
                    ) : (
                      <div className="whitespace-pre-wrap">
                        {message.content}
                      </div>
                    )
                  ) : (
                    message.content || ""
                  )}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gradient-to-r from-gray-50 to-gray-100 text-gray-800 rounded-xl p-4">
                  <div className="flex items-center space-x-2">
                    <div className="animate-pulse">⏳</div>
                    <span>Analyzing market data...</span>
                  </div>
                </div>
              </div>
            )}
          </div>

          <form onSubmit={handleSubmit} className="mt-auto">
            <div className="flex gap-3">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about market trends..."
                className="flex-1 p-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-50"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={isLoading}
                className="bg-gradient-to-r from-blue-500 to-blue-600 text-white px-8 py-3 rounded-xl hover:from-blue-600 hover:to-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 transition-all duration-200"
              >
                Send
              </button>
            </div>
          </form>
        </motion.div>
      </div>
    </main>
  );
}

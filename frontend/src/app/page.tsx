"use client";

import { useState } from "react";
import { Card, Title, LineChart, Text } from "@tremor/react";
import { motion } from "framer-motion";

const dummyData = [
  { date: "2024-01", value: 18000 },
  { date: "2024-02", value: 17800 },
  { date: "2024-03", value: 18200 },
  { date: "2024-04", value: 18100 },
];

interface Message {
  role: "user" | "assistant";
  content: string;
}

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
    <main className="container mx-auto p-4 min-h-screen bg-gray-50">
      <Title className="text-2xl font-bold mb-6 text-indigo-900">
        News Sense Analytics Dashboard
      </Title>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Column - Analytics */}
        <div className="space-y-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <Card className="bg-white shadow-lg">
              <Title className="text-lg mb-4">📈 Line Chart</Title>
              <LineChart
                data={dummyData}
                index="date"
                categories={["value"]}
                colors={["blue"]}
                className="h-72"
              />
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <Card className="bg-white shadow-lg">
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 border rounded-lg">
                  <Text>🌡️ Temperature</Text>
                  <Title className="mt-2">23°C</Title>
                </div>
                <div className="p-4 border rounded-lg">
                  <Text>💰 Market Status</Text>
                  <Title className="mt-2">Active</Title>
                </div>
              </div>
              <div className="mt-4">
                <Text className="text-lg font-semibold mb-2">
                  Increased Tariffs
                </Text>
                <div className="space-y-2">
                  <div className="h-2 bg-blue-400 rounded w-3/4"></div>
                  <div className="h-2 bg-green-400 rounded w-1/2"></div>
                  <div className="h-2 bg-purple-400 rounded w-4/5"></div>
                </div>
              </div>
            </Card>
          </motion.div>
        </div>

        {/* Right Column - Chat Interface */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
          className="bg-white rounded-lg shadow-lg p-4 flex flex-col h-[calc(100vh-2rem)]"
        >
          <div className="bg-blue-100 text-blue-800 px-4 py-2 rounded-t-lg mb-4">
            Chat with N
          </div>

          <div className="flex-1 overflow-y-auto space-y-4 mb-4">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex ${
                  message.role === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`max-w-[80%] rounded-lg p-3 ${
                    message.role === "user"
                      ? "bg-blue-500 text-white"
                      : "bg-gray-100 text-gray-800"
                  }`}
                >
                  {message.content}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 text-gray-800 rounded-lg p-3">
                  Thinking...
                </div>
              </div>
            )}
          </div>

          <form onSubmit={handleSubmit} className="mt-auto">
            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type a message..."
                className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={isLoading}
                className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
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

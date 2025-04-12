import React from "react";
import dynamic from "next/dynamic";
import { Data, Layout } from "plotly.js";

// Dynamically import Plot to avoid SSR issues
const Plot = dynamic(() => import("react-plotly.js"), { ssr: false });

const ParetoAnalysis = () => {
  // Sample data - in a real app, this would come from an API
  const dates = ["2024-01", "2024-02", "2024-03", "2024-04"];
  const negativeSentiment = [1200, 1400, 1100, 1300];
  const fundPrice = [18000, 17800, 18200, 18100];

  const data: Data[] = [
    {
      x: dates,
      y: negativeSentiment,
      name: "Negative Sentiment Count",
      type: "bar" as const,
      marker: {
        color: "rgba(255, 99, 71, 0.7)",
        line: {
          color: "rgba(255, 99, 71, 1.0)",
          width: 1.5,
        },
      },
      yaxis: "y1",
    },
    {
      x: dates,
      y: fundPrice,
      name: "Fund Price",
      type: "scatter" as const,
      mode: "lines+markers",
      line: {
        color: "rgba(30, 144, 255, 0.9)",
        width: 3,
      },
      marker: {
        size: 8,
        symbol: "circle",
        color: "white",
        line: {
          width: 2,
          color: "rgba(30, 144, 255, 1.0)",
        },
      },
      yaxis: "y2",
    },
  ];

  const layout: Partial<Layout> = {
    title: {
      text: "Pareto Analysis: Negative News vs Fund Price",
      font: {
        color: "#000000",
        size: 20,
      },
    },
    paper_bgcolor: "rgba(17,17,17,0)",
    plot_bgcolor: "rgba(17,17,17,0)",
    xaxis: {
      title: {
        text: "Date",
        font: {
          color: "#000000",
        },
      },
      tickangle: 45,
      tickfont: {
        color: "#E5ECF6",
      },
      gridcolor: "rgba(229,236,246,0.1)",
      zerolinecolor: "rgba(229,236,246,0.1)",
    },
    yaxis: {
      title: {
        text: "Negative Sentiment Count",
        font: {
          color: "rgba(255, 99, 71, 1.0)",
        },
      },
      tickfont: {
        color: "rgba(255, 99, 71, 0.7)",
      },
      side: "left" as const,
      gridcolor: "rgba(229,236,246,0.1)",
      zerolinecolor: "rgba(229,236,246,0.1)",
    },
    yaxis2: {
      title: {
        text: "Fund Price",
        font: {
          color: "rgba(30, 144, 255, 1.0)",
        },
      },
      tickfont: {
        color: "rgba(30, 144, 255, 0.9)",
      },
      overlaying: "y",
      side: "right" as const,
      gridcolor: "rgba(229,236,246,0.1)",
      zerolinecolor: "rgba(229,236,246,0.1)",
    },
    legend: {
      x: 0.01,
      y: 0.99,
      bgcolor: "rgba(17,17,17,0)",
      font: {
        color: "#E5ECF6",
      },
    },
    margin: {
      l: 60,
      r: 60,
      t: 50,
      b: 50,
    },
    autosize: true,
  };

  return (
    <div className="w-full h-[500px] flex justify-center">
      <Plot
        data={data}
        layout={layout}
        config={{
          responsive: true,
          displayModeBar: false,
        }}
        className="w-full h-full"
        style={{ width: "100%", height: "100%" }}
      />
    </div>
  );
};

export default ParetoAnalysis;

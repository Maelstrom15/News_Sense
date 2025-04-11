import React from "react";
import dynamic from "next/dynamic";
import { Data, Layout } from "plotly.js";

// Dynamically import Plot to avoid SSR issues
const Plot = dynamic(() => import("react-plotly.js"), { ssr: false });

const CorrelationHeatmap = () => {
  // Sample correlation data from the notebook
  const correlationData = [
    [1.0, -0.32, 0.28],
    [-0.32, 1.0, -0.15],
    [0.28, -0.15, 1.0],
  ];

  const labels = ["Fund Price", "Negative Sentiment", "Positive Sentiment"];

  const data: Data[] = [
    {
      z: correlationData,
      x: labels,
      y: labels,
      type: "heatmap" as const,
      colorscale: [
        [0, "rgb(49, 54, 149)"],
        [0.5, "rgb(255,255,255)"],
        [1, "rgb(165, 0, 38)"],
      ],
      showscale: true,
      zmin: -1,
      zmax: 1,
    },
  ];

  const layout: Partial<Layout> = {
    title: {
      text: "Correlation between Fund Price and News Sentiments",
      font: {
        color: "#E5ECF6",
        size: 20,
      },
    },
    paper_bgcolor: "rgba(17,17,17,0)",
    plot_bgcolor: "rgba(17,17,17,0)",
    xaxis: {
      tickfont: {
        color: "#E5ECF6",
      },
      gridcolor: "rgba(229,236,246,0.1)",
      zerolinecolor: "rgba(229,236,246,0.1)",
    },
    yaxis: {
      tickfont: {
        color: "#E5ECF6",
      },
      gridcolor: "rgba(229,236,246,0.1)",
      zerolinecolor: "rgba(229,236,246,0.1)",
    },
    margin: {
      l: 80,
      r: 80,
      t: 50,
      b: 80,
    },
    annotations: correlationData
      .map((row, i) =>
        row.map((val, j) => ({
          text: val.toFixed(2),
          x: j,
          y: i,
          xref: "x" as const,
          yref: "y" as const,
          showarrow: false,
          font: {
            color: Math.abs(val) > 0.5 ? "white" : "#E5ECF6",
            size: 14,
          },
        }))
      )
      .flat(),
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

export default CorrelationHeatmap;

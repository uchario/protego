/* eslint-disable @typescript-eslint/no-explicit-any */
import { useState, useEffect } from "react";
import BASE_URL from "./config/index";

const App = () => {
  const [url, setUrl] = useState<string>("");
  const [metrics, setMetrics] = useState<{
    link_count: number;
    word_count: number;
    image_count: number;
  }>({
    link_count: 0,
    word_count: 0,
    image_count: 0,
  });
  const [history, setHistory] = useState<string[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const chromeApi = (window as any).chrome;
    if (
      chromeApi &&
      chromeApi.tabs &&
      typeof chromeApi.tabs.query === "function"
    ) {
      chromeApi.tabs.query(
        { active: true, currentWindow: true },
        (tabs: any[]) => {
          const currentUrl = (tabs && tabs[0] && tabs[0].url) || "";
          setUrl(currentUrl);

          Promise.all([
            fetch(
              `${BASE_URL}/metrics?url=${encodeURIComponent(currentUrl)}`
            ).then((res) => res.json()),
            fetch(
              `${BASE_URL}/history?url=${encodeURIComponent(currentUrl)}`
            ).then((res) => res.json()),
          ])
            .then(([metricsData, historyData]) => {
              setMetrics(metricsData);
              setHistory(
                historyData.sort(
                  (a: string, b: string) =>
                    new Date(b).getTime() - new Date(a).getTime()
                )
              ); // Ensure descending
              setLoading(false);
            })
            .catch((error) => {
              console.error("Error fetching data:", error);
              setLoading(false);
            });
        }
      );
    } else {
      // Fallback when not running as a browser extension (prevents TS error and runtime crash)
      const currentUrl = window.location.href || "";
      setUrl(currentUrl);

      Promise.all([
        fetch(`${BASE_URL}/metrics?url=${encodeURIComponent(currentUrl)}`).then(
          (res) => res.json()
        ),
        fetch(`${BASE_URL}/history?url=${encodeURIComponent(currentUrl)}`).then(
          (res) => res.json()
        ),
      ])
        .then(([metricsData, historyData]) => {
          setMetrics(metricsData);
          setHistory(
            historyData.sort(
              (a: string, b: string) =>
                new Date(b).getTime() - new Date(a).getTime()
            )
          ); // Ensure descending
          setLoading(false);
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
          setLoading(false);
        });
    }
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  const lastVisited =
    history.length > 0
      ? new Date(history[0]).toLocaleString()
      : "No previous visits";

  return (
    <div className="p-4 bg-gray-50 text-gray-800 min-h-screen flex flex-col space-y-4 text-sm">
      <h1 className="text-xl font-bold text-blue-700 border-b border-gray-300 pb-2">
        Page History
      </h1>
      <div className="bg-white p-3 rounded shadow-sm border border-gray-200">
        <p className="font-semibold text-gray-700">Current URL:</p>
        <p className="text-xs text-gray-600 break-all">{url}</p>
      </div>
      <div>
        <h2 className="text-lg font-semibold text-green-700 mb-2">
          Current Metrics
        </h2>
        <ul className="bg-white p-3 rounded shadow-sm border border-gray-200 space-y-2">
          <li className="flex justify-between">
            <span className="font-medium">Links:</span>
            <span className="text-gray-600">{metrics.link_count}</span>
          </li>
          <li className="flex justify-between">
            <span className="font-medium">Words:</span>
            <span className="text-gray-600">{metrics.word_count}</span>
          </li>
          <li className="flex justify-between">
            <span className="font-medium">Images:</span>
            <span className="text-gray-600">{metrics.image_count}</span>
          </li>
        </ul>
      </div>
      <div>
        <h2 className="text-lg font-semibold text-purple-700 mb-2">
          Last Visited:
        </h2>
        <p className="bg-white p-3 rounded shadow-sm border border-gray-200 text-gray-700">
          {lastVisited}
        </p>
      </div>
      <div>
        <h2 className="text-lg font-semibold text-indigo-700 mb-2">
          Past Visits:
        </h2>
        <ul className="bg-white p-3 rounded shadow-sm border border-gray-200 space-y-1 max-h-48 overflow-y-auto">
          {history.length > 0 ? (
            history.map((timestamp, index) => (
              <li
                key={index}
                className="text-gray-600 text-xs border-b border-gray-100 pb-1 last:border-0"
              >
                {new Date(timestamp).toLocaleString()}
              </li>
            ))
          ) : (
            <li className="text-gray-500 italic">No past visits</li>
          )}
        </ul>
      </div>
    </div>
  );
};

export default App;

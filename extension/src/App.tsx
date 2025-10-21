// extension/src/App.tsx
/* eslint-disable @typescript-eslint/no-explicit-any */
import { useState, useEffect } from "react";
import { getMetrics, getHistory } from "./api/pageApi";
import CurrentUrl from "./components/CurrentUrl";
import MetricsComponent from "./components/Metrics";
import LastVisited from "./components/LastVisited";
import PastVisits from "./components/PastVisits";

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
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const chromeApi = (window as any).chrome;
    let currentUrl = "";
    if (
      chromeApi &&
      chromeApi.tabs &&
      typeof chromeApi.tabs.query === "function"
    ) {
      chromeApi.tabs.query(
        { active: true, currentWindow: true },
        (tabs: any[]) => {
          currentUrl = (tabs && tabs[0] && tabs[0].url) || "";
          setUrl(currentUrl);
          fetchData(currentUrl);
        }
      );
    } else {
      // Fallback when not running as a browser extension
      currentUrl = window.location.href || "";
      setUrl(currentUrl);
      fetchData(currentUrl);
    }
  }, []);

  const fetchData = async (currentUrl: string) => {
    try {
      const [metricsData, historyData] = await Promise.all([
        getMetrics(currentUrl),
        getHistory(currentUrl),
      ]);
      setMetrics(metricsData);
      setHistory(
        historyData.sort(
          (a: string, b: string) =>
            new Date(b).getTime() - new Date(a).getTime()
        )
      ); // Ensure descending
    } catch (err) {
      setError((err as Error).message || "An unknown error occurred");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div className="p-4 text-red-700">Error: {error}</div>;
  }

  return (
    <div className="p-4 bg-gray-50 text-gray-800 min-h-screen flex flex-col space-y-4 text-sm">
      <h1 className="text-xl font-bold text-blue-700 border-b border-gray-300 pb-2">
        Page History
      </h1>
      <CurrentUrl url={url} />
      <MetricsComponent metrics={metrics} />
      <LastVisited history={history} />
      <PastVisits history={history} />
    </div>
  );
};

export default App;
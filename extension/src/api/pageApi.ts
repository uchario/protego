// extension/src/api/pageApi.ts
import BASE_URL from "../config";

export const getMetrics = async (url: string) => {
  const response = await fetch(
    `${BASE_URL}/metrics?url=${encodeURIComponent(url)}`
  );
  if (!response.ok) {
    throw new Error("Failed to fetch metrics");
  }
  return response.json() as Promise<{
    link_count: number;
    word_count: number;
    image_count: number;
  }>;
};

export const getHistory = async (url: string) => {
  const response = await fetch(
    `${BASE_URL}/history?url=${encodeURIComponent(url)}`
  );
  if (response.status === 404) {
    return [];
  }
  if (!response.ok) {
    throw new Error("Failed to fetch history");
  }
  return response.json() as Promise<string[]>;
};

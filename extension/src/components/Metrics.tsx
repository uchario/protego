// extension/src/components/Metrics.tsx
interface MetricsProps {
  metrics: {
    link_count: number;
    word_count: number;
    image_count: number;
  };
}

const Metrics = ({ metrics }: MetricsProps) => {
  return (
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
  );
};

export default Metrics;
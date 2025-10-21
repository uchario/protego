// extension/src/components/PastVisits.tsx
interface PastVisitsProps {
  history: string[];
}

const PastVisits = ({ history }: PastVisitsProps) => {
  return (
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
  );
};

export default PastVisits;
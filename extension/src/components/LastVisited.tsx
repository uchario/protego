// extension/src/components/LastVisited.tsx
interface LastVisitedProps {
  history: string[];
}

const LastVisited = ({ history }: LastVisitedProps) => {
  const lastVisited =
    history.length > 0
      ? new Date(history[0]).toLocaleString()
      : "No previous visits";

  return (
    <div>
      <h2 className="text-lg font-semibold text-purple-700 mb-2">
        Last Visited:
      </h2>
      <p className="bg-white p-3 rounded shadow-sm border border-gray-200 text-gray-700">
        {lastVisited}
      </p>
    </div>
  );
};

export default LastVisited;
// extension/src/components/CurrentUrl.tsx
interface CurrentUrlProps {
  url: string;
}

const CurrentUrl = ({ url }: CurrentUrlProps) => {
  return (
    <div className="bg-white p-3 rounded shadow-sm border border-gray-200">
      <p className="font-semibold text-gray-700">Current URL:</p>
      <p className="text-xs text-gray-600 break-all">{url}</p>
    </div>
  );
};

export default CurrentUrl;

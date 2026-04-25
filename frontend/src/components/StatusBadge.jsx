export default function StatusBadge({ status }) {
  const colors = {
    OPEN: 'bg-red-100 text-red-800',
    IN_PROGRESS: 'bg-yellow-100 text-yellow-800',
    RESOLVED: 'bg-green-100 text-green-800',
    FALSE_POSITIVE: 'bg-gray-100 text-gray-800',
    ACCEPTED_RISK: 'bg-blue-100 text-blue-800'
  };
  return (
    <span className={`px-2 py-1 rounded-full text-xs font-semibold ${colors[status] || 'bg-gray-100'}`}>
      {status}
    </span>
  );
}

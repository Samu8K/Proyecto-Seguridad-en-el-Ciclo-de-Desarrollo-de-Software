import StatusBadge from './StatusBadge';

export default function FindingsTable({ findings, onStatusChange }) {
  return (
    <div className="overflow-x-auto bg-white rounded-lg shadow">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Title</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Severity</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">CVSS</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">File</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {findings.map((f) => (
            <tr key={f.id}>
              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{f.title}</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{f.severity}</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{f.cvss_score || 'N/A'}</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{f.file_path}:{f.line_number}</td>
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="flex flex-col gap-2">
                  <StatusBadge status={f.status} />
                  {onStatusChange && f.status !== 'RESOLVED' && (
                    <div className="flex flex-wrap gap-2 mt-2">
                      {f.status === 'OPEN' && (
                        <button
                          type="button"
                          className="px-2 py-1 text-xs font-semibold text-white bg-blue-600 rounded hover:bg-blue-700"
                          onClick={() => onStatusChange(f.id, 'IN_PROGRESS')}
                        >
                          In Progress
                        </button>
                      )}
                      <button
                        type="button"
                        className="px-2 py-1 text-xs font-semibold text-white bg-green-600 rounded hover:bg-green-700"
                        onClick={() => onStatusChange(f.id, 'RESOLVED')}
                      >
                        Mark Resolved
                      </button>
                    </div>
                  )}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

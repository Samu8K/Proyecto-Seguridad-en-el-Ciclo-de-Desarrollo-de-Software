import StatusBadge from './StatusBadge';

export default function FindingsTable({ findings }) {
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
              <td className="px-6 py-4 whitespace-nowrap"><StatusBadge status={f.status} /></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

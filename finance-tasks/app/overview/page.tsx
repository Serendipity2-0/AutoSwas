/**
 * Overview page component (placeholder)
 */
export default function OverviewPage() {
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Process Overview</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold text-gray-900 mb-2">Total Processes</h2>
          <p className="text-3xl font-bold text-indigo-600">Coming soon</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold text-gray-900 mb-2">Automation Rate</h2>
          <p className="text-3xl font-bold text-indigo-600">Coming soon</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold text-gray-900 mb-2">Time Saved</h2>
          <p className="text-3xl font-bold text-indigo-600">Coming soon</p>
        </div>
      </div>
    </div>
  );
}

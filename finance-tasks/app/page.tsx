import Link from 'next/link';
import { ArrowRight } from 'lucide-react';

/**
 * Landing page component
 */
export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-8 bg-gradient-to-b from-indigo-50 to-white">
      <div className="max-w-3xl text-center">
        <h1 className="text-5xl font-bold text-indigo-900 mb-6">
          Finance Process Automation
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Streamline your financial processes, improve efficiency, and drive automation across your organization.
        </p>
        <div className="flex gap-4 justify-center">
          <Link
            href="/processes"
            className="inline-flex items-center px-6 py-3 text-lg font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors"
          >
            View Processes
            <ArrowRight className="ml-2 h-5 w-5" />
          </Link>
          <Link
            href="/docs"
            className="inline-flex items-center px-6 py-3 text-lg font-medium text-indigo-600 bg-white border-2 border-indigo-600 rounded-lg hover:bg-indigo-50 transition-colors"
          >
            Learn More
          </Link>
        </div>
      </div>

      {/* Features */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16 max-w-6xl w-full">
        <div className="p-6 bg-white rounded-lg shadow-sm border border-gray-100">
          <h3 className="text-lg font-semibold text-indigo-900 mb-2">Process Management</h3>
          <p className="text-gray-600">
            Centralize and organize all your financial processes in one place.
          </p>
        </div>
        <div className="p-6 bg-white rounded-lg shadow-sm border border-gray-100">
          <h3 className="text-lg font-semibold text-indigo-900 mb-2">Automation Tools</h3>
          <p className="text-gray-600">
            Identify and implement automation opportunities to reduce manual work.
          </p>
        </div>
        <div className="p-6 bg-white rounded-lg shadow-sm border border-gray-100">
          <h3 className="text-lg font-semibold text-indigo-900 mb-2">Documentation</h3>
          <p className="text-gray-600">
            Maintain clear documentation for all processes and procedures.
          </p>
        </div>
      </div>
    </div>
  );
}

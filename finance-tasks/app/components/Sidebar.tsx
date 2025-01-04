"use client";

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  Settings, 
  FileText, 
  Layers, 
  BarChart3, 
  Zap
} from 'lucide-react';

/**
 * Sidebar navigation component
 */
export default function Sidebar() {
  const pathname = usePathname();

  const navigation = [
    { name: 'All processes', href: '/processes', icon: Layers },
    { name: 'My Initiatives', href: '/initiatives', icon: Settings },
    { name: 'Documentations', href: '/docs', icon: FileText },
    { name: 'Automation', href: '/automation', icon: Zap },
    { name: 'Overview', href: '/overview', icon: BarChart3 },
  ];

  return (
    <div className="flex flex-col w-64 bg-indigo-700 text-white">
      {/* Logo */}
      <div className="p-4">
        <Link href="/" className="flex items-center">
          <span className="text-3xl font-bold">∞</span>
        </Link>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-2 py-4 space-y-1">
        {navigation.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={`flex items-center px-4 py-3 text-sm rounded-lg transition-colors ${
                isActive
                  ? 'bg-indigo-800 text-white'
                  : 'text-indigo-100 hover:bg-indigo-800'
              }`}
            >
              <item.icon className="h-5 w-5 mr-3" />
              {item.name}
            </Link>
          );
        })}
      </nav>
    </div>
  );
}

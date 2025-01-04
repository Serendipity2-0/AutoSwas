import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  webpack: (config, { isServer }) => {
    // SQLite3 configuration for better-sqlite3
    if (isServer) {
      config.externals = [...config.externals, 'better-sqlite3']
    }
    return config
  },
  // Experimental features needed for API routes
  experimental: {
    serverActions: {
      allowedOrigins: ['localhost:3000']
    }
  },
}

export default nextConfig

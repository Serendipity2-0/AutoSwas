'use client';

import Script from 'next/script';
import { usePathname, useSearchParams } from 'next/navigation';
import { useEffect } from 'react';

// Google Analytics Measurement ID
const GA_MEASUREMENT_ID = 'G-K44ZFNDNPV';

/**
 * Initialize Google Analytics and track page views
 */
export function Analytics() {
  const pathname = usePathname();
  const searchParams = useSearchParams();

  useEffect(() => {
    if (pathname) {
      // Send page view event
      window.gtag?.('event', 'page_view', {
        page_path: pathname,
        page_search: searchParams?.toString(),
      });
    }
  }, [pathname, searchParams]);

  return (
    <>
      <Script
        src={`https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`}
        strategy="afterInteractive"
      />
      <Script id="google-analytics" strategy="afterInteractive">
        {`
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', '${GA_MEASUREMENT_ID}');
        `}
      </Script>
    </>
  );
}

/**
 * Track custom events
 * @param action - The action/event name
 * @param category - Event category
 * @param label - Event label
 * @param value - Event value (optional)
 */
export function trackEvent(
  action: string,
  category: string,
  label: string,
  value?: number
) {
  window.gtag?.('event', action, {
    event_category: category,
    event_label: label,
    value: value,
  });
}

// Type definitions for Google Analytics
type GTagEvent = {
  action: string;
  category: string;
  label: string;
  value?: number;
};

type GTagParams = {
  page_path?: string;
  page_search?: string;
  event_category?: string;
  event_label?: string;
  value?: number;
};

// Add type definition for gtag
declare global {
  interface Window {
    gtag?: (
      command: 'event' | 'config' | 'js',
      targetId: string | Date,
      params?: GTagParams
    ) => void;
    dataLayer?: Array<{ push: (...args: unknown[]) => void }>;
  }
}

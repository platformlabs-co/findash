interface GTMEvent {
  event: string;
  [key: string]: any;
}

declare global {
  interface Window {
    dataLayer: any[];
  }
}

export const initGTM = () => {
  if (!window.dataLayer) {
    window.dataLayer = [];
  }
};

export const pushToDataLayer = (data: GTMEvent) => {
  if (window.dataLayer) {
    window.dataLayer.push(data);
  }
};

// Common events
export const trackPageView = (pagePath: string, pageTitle: string) => {
  pushToDataLayer({
    event: 'page_view',
    page_path: pagePath,
    page_title: pageTitle,
  });
};

export const trackEvent = (category: string, action: string, label?: string, value?: number) => {
  pushToDataLayer({
    event: 'custom_event',
    event_category: category,
    event_action: action,
    event_label: label,
    event_value: value,
  });
}; 
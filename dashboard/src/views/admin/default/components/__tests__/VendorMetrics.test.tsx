import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import VendorMetrics from '../VendorMetrics';
import { useAuth0 } from '@auth0/auth0-react';
import '@testing-library/jest-dom';

// Mock Auth0
jest.mock('@auth0/auth0-react');

// Mock the chart component since we don't need to test its internals
jest.mock('components/charts/BarChart', () => {
  return function DummyChart() {
    return <div data-testid="bar-chart">Chart</div>;
  };
});

const renderWithRouter = (ui: React.ReactElement) => {
  return render(
    <BrowserRouter>
      {ui}
    </BrowserRouter>
  );
};

describe('VendorMetrics', () => {
  beforeEach(() => {
    // Mock Auth0 hook
    (useAuth0 as jest.Mock).mockReturnValue({
      getAccessTokenSilently: jest.fn(),
      isAuthenticated: true,
      user: { sub: 'test-user' }
    });

    // Mock window.location
    Object.defineProperty(window, 'location', {
      value: { pathname: '/' },
      writable: true
    });
  });

  it('renders the component title', () => {
    renderWithRouter(
      <VendorMetrics
        vendor="aws"
        title="AWS Costs"
        demo={true}
      />
    );

    expect(screen.getByText('AWS Costs')).toBeInTheDocument();
  });

  it('shows demo data when demo prop is true', () => {
    renderWithRouter(
      <VendorMetrics
        vendor="aws"
        title="AWS Costs"
        demo={true}
      />
    );

    // The chart should be rendered
    expect(screen.getByTestId('bar-chart')).toBeInTheDocument();
  });
}); 
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['junit', { outputFile: 'playwright-report/results.xml' }]
  ],
  use: {
    baseURL: process.env.CI ? 'http://localhost:3000' : 'http://localhost:3000',
    trace: 'on-first-retry',
    extraHTTPHeaders: {
      // Add any default headers needed
    },
    // Collect traces for failed tests in CI
    trace: process.env.CI ? 'retain-on-failure' : 'on-first-retry',
    // Record video for failed tests in CI
    video: process.env.CI ? 'retain-on-failure' : 'on-first-retry',
    screenshot: process.env.CI ? 'only-on-failure' : 'on',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    // Only run Firefox and WebKit in CI to save time during local development
    process.env.CI ? {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    } : null,
    process.env.CI ? {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    } : null,
  ].filter(Boolean),
  webServer: {
    command: 'npm run start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120000, // Increase timeout for CI
    env: {
      REACT_APP_BACKEND_URL: 'http://localhost:8000',
      CI: process.env.CI ? 'true' : 'false',
    },
  },
}); 
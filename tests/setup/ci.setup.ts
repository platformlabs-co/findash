import { test as setup, expect } from '@playwright/test';

setup('CI setup', async ({ page }) => {
  // Additional CI-specific setup
  if (process.env.CI) {
    // Set longer timeouts for CI environment
    test.setTimeout(60000);
    
    // Mock Auth0 for CI
    await page.route('**/oauth/token', async route => {
      await route.fulfill({
        status: 200,
        body: JSON.stringify({
          access_token: 'fake-token',
          expires_in: 86400
        })
      });
    });
  }
}); 
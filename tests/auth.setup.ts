import { test as setup } from '@playwright/test';

setup('authenticate', async ({ page }) => {
  // Setup authentication state that can be reused across tests
  await page.goto('/');
  
  // Mock Auth0 authentication for tests
  await page.route('**/oauth/token', async route => {
    await route.fulfill({
      status: 200,
      body: JSON.stringify({
        access_token: 'fake-token',
        expires_in: 86400
      })
    });
  });
  
  // Store authentication state
  await page.context().storageState({ path: 'playwright/.auth/user.json' });
}); 
import { test, expect } from '@playwright/test';

test.use({ storageState: 'playwright/.auth/user.json' });

test.describe('Dashboard', () => {
  test('should show welcome message when no configurations exist', async ({ page }) => {
    await page.goto('/admin/default');
    
    // Check for welcome message
    await expect(page.getByText('Welcome to FinDash 🚀')).toBeVisible();
    await expect(page.getByText("To get started, you'll need to configure some accounts.")).toBeVisible();
    
    // Check for "let's get to it!" button
    const configButton = page.getByRole('link', { name: "let's get to it!" });
    await expect(configButton).toBeVisible();
    await expect(configButton).toHaveAttribute('href', '/admin/linked-accounts');
  });

  test('should show vendor metrics when configurations exist', async ({ page }) => {
    // Mock the API response for configurations
    await page.route('/v1/configuration/list', async (route) => {
      await route.fulfill({
        status: 200,
        body: JSON.stringify({
          data: [
            {
              id: 1,
              type: 'aws',
              identifier: 'AWS Config 1'
            },
            {
              id: 2,
              type: 'datadog',
              identifier: 'Datadog Config 1'
            }
          ]
        })
      });
    });

    await page.goto('/admin/default');
    
    // Check for vendor metric cards
    await expect(page.getByText('AWS Metrics')).toBeVisible();
    await expect(page.getByText('Datadog Metrics')).toBeVisible();
  });
}); 
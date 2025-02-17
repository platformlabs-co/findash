import { test, expect } from '@playwright/test';

test.describe('VendorMetrics Component', () => {
  test('should display metrics data correctly', async ({ page }) => {
    // Mock the metrics API response
    await page.route('**/v1/vendors-metrics/**', async (route) => {
      await route.fulfill({
        status: 200,
        body: JSON.stringify({
          data: [
            { month: '01-2024', cost: 1500 },
            { month: '02-2024', cost: 1600 },
            { month: '03-2024', cost: 1700 }
          ]
        })
      });
    });

    await page.goto('/admin/default');

    // Check for metric card elements
    await expect(page.getByText('Monthly Costs')).toBeVisible();
    await expect(page.getByRole('button', { name: 'Actual' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Forecast' })).toBeVisible();
    
    // Check if cost data is displayed
    await expect(page.getByText('$1,500.00')).toBeVisible();
    await expect(page.getByText('$1,700.00')).toBeVisible();
  });

  test('should handle error states', async ({ page }) => {
    // Mock a failed API response
    await page.route('**/v1/vendors-metrics/**', async (route) => {
      await route.fulfill({
        status: 500,
        body: JSON.stringify({ message: 'Failed to fetch vendor metrics' })
      });
    });

    await page.goto('/admin/default');
    
    // Check for error message
    await expect(page.getByText('Failed to fetch vendor metrics')).toBeVisible();
  });
}); 
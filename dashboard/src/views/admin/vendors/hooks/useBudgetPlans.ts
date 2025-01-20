import { useState, useCallback } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import { CallBackendService } from 'utils';

export interface BudgetEntry {
  month: string;
  amount: number;
}

export interface BudgetPlan {
  id: number;
  vendor: string;
  user_id: number;
  budgets: {
    budgets: BudgetEntry[];
  };
  created_at: string;
  updated_at: string;
  type: string;
}

interface UseBudgetPlansReturn {
  loading: boolean;
  error: string | null;
  budgetPlan: BudgetPlan[] | null;
  createBudgetPlan: (vendor: string, budgets: BudgetEntry[]) => Promise<void>;
  fetchBudgetPlan: (vendor: string) => Promise<void>;
}

export const useBudgetPlans = (initialVendor: string): UseBudgetPlansReturn => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [budgetPlan, setBudgetPlan] = useState<BudgetPlan[] | null>(null);
  const { getAccessTokenSilently } = useAuth0();

  const fetchBudgetPlan = useCallback(async (vendor: string) => {
    setLoading(true);
    setError(null);
    try {
      const response = await CallBackendService(
        `/v1/budget-plans?vendor=${vendor}`,
        getAccessTokenSilently
      );
      setBudgetPlan(response.length > 0 ? response : null);
    } catch (err) {
      setError('Failed to fetch budget plan');
      console.error('Error fetching budget plan:', err);
    } finally {
      setLoading(false);
    }
  }, [getAccessTokenSilently]);

  const createBudgetPlan = useCallback(async (vendor: string, budgets: BudgetEntry[]) => {
    setLoading(true);
    setError(null);
    try {
      const response = await CallBackendService(
        '/v1/budget-plans',
        getAccessTokenSilently,
        {
          method: "POST",
          body: JSON.stringify({
            vendor,
            budgets
          }),
          headers: { "Content-Type": "application/json" },
        }
      );
      setBudgetPlan(response);
    } catch (err) {
      setError('Failed to create budget plan');
      console.error('Error creating budget plan:', err);
    } finally {
      setLoading(false);
    }
  }, [getAccessTokenSilently]);

  return {
    loading,
    error,
    budgetPlan,
    createBudgetPlan,
    fetchBudgetPlan
  };
}; 
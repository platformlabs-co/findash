
from typing import List, Dict
from datetime import datetime, timedelta

class ForecastService:
    @staticmethod
    def predict_mom_growth(historical_data: List[Dict[str, any]], months_to_predict: int = 12) -> List[Dict[str, any]]:
        if not historical_data or len(historical_data) < 2:
            return []

        # Calculate average MoM growth
        total_growth = 0
        growth_points = 0
        
        for i in range(1, len(historical_data)):
            if historical_data[i-1]['cost'] > 0:  # Avoid division by zero
                growth = (historical_data[i]['cost'] - historical_data[i-1]['cost']) / historical_data[i-1]['cost']
                total_growth += growth
                growth_points += 1

        avg_growth = total_growth / growth_points if growth_points > 0 else 0
        
        # Define growth rates for different scenarios
        best_case_growth = avg_growth * 1.5  # 50% better growth
        worst_case_growth = avg_growth * 0.5  # 50% worse growth
        
        # Get the last date from historical data
        last_date = datetime.strptime(historical_data[-1]['month'], "%m-%Y")
        last_cost = historical_data[-1]['cost']
        
        forecast_data = []
        current_cost = last_cost
        best_case_cost = last_cost
        worst_case_cost = last_cost
        
        for i in range(months_to_predict):
            next_date = last_date + timedelta(days=30 * (i + 1))
            current_cost = current_cost * (1 + avg_growth)
            best_case_cost = best_case_cost * (1 + best_case_growth)
            worst_case_cost = worst_case_cost * (1 + worst_case_growth)
            
            forecast_data.append({
                'month': next_date.strftime("%m-%Y"),
                'cost': round(current_cost, 2),
                'best_case': round(best_case_cost, 2),
                'worst_case': round(worst_case_cost, 2)
            })
            
        return forecast_data

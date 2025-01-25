from typing import List, Dict, Any, TypedDict
from datetime import datetime, timedelta


class HistoricalDataPoint(TypedDict):
    month: str
    cost: float


class ForecastDataPoint(TypedDict):
    month: str
    cost: float
    best_case: float
    worst_case: float


class ForecastService:
    @staticmethod
    def predict_mom_growth(
        historical_data: List[HistoricalDataPoint], months_to_predict: int = 12
    ) -> Dict[str, Any]:
        if not historical_data or len(historical_data) < 2:
            return {
                "forecast_data": [],
                "sums": {
                    "total_forecast": 0,
                    "total_best_case": 0,
                    "total_worst_case": 0,
                },
                "growth_rates": {
                    "trend_based": 0,
                    "best_case": 0,
                    "worst_case": 0,
                },
            }

        # Calculate average MoM growth including current month
        total_growth: float = 0.0
        growth_points: int = 0

        # Sort historical data by month to ensure correct order
        sorted_data = sorted(
            historical_data, key=lambda x: datetime.strptime(x["month"], "%m-%Y")
        )

        for i in range(1, len(sorted_data)):
            prev_cost = sorted_data[i - 1]["cost"]
            if prev_cost > 0:  # Avoid division by zero
                growth = (sorted_data[i]["cost"] - prev_cost) / prev_cost
                total_growth += growth
                growth_points += 1

        avg_growth = total_growth / growth_points if growth_points > 0 else 0.0

        # Define growth rates for different scenarios
        best_case_growth = avg_growth * 0.5  # 50% less growth (cheaper)
        worst_case_growth = avg_growth * 1.5  # 50% more growth (more expensive)

        # Get the last month's data
        last_date = datetime.strptime(sorted_data[-1]["month"], "%m-%Y")
        last_cost = sorted_data[-1]["cost"]

        forecast_data: List[ForecastDataPoint] = []
        current_cost = last_cost
        best_case_cost = last_cost
        worst_case_cost = last_cost

        # Start forecasting from next month
        for i in range(months_to_predict):
            next_date = last_date + timedelta(days=30 * (i + 1))
            current_cost = current_cost * (1 + avg_growth)
            best_case_cost = best_case_cost * (1 + best_case_growth)
            worst_case_cost = worst_case_cost * (1 + worst_case_growth)

            forecast_data.append(
                {
                    "month": next_date.strftime("%m-%Y"),
                    "cost": round(current_cost, 2),
                    "best_case": round(best_case_cost, 2),
                    "worst_case": round(worst_case_cost, 2),
                }
            )

        # Calculate sums
        total_forecast = sum(entry["cost"] for entry in forecast_data)
        total_best_case = sum(entry["best_case"] for entry in forecast_data)
        total_worst_case = sum(entry["worst_case"] for entry in forecast_data)

        return {
            "forecast_data": forecast_data,
            "sums": {
                "total_forecast": round(total_forecast, 2),
                "total_best_case": round(total_best_case, 2),
                "total_worst_case": round(total_worst_case, 2),
            },
            "growth_rates": {
                "trend_based": round(avg_growth * 100, 2),
                "best_case": round(best_case_growth * 100, 2),
                "worst_case": round(worst_case_growth * 100, 2),
            },
        }

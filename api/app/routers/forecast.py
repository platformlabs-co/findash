
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta

router = APIRouter(tags=["cloud-cost-forecast"])

@router.get("/v1/vendors-forecast/{vendor_name}")
async def get_vendor_forecast(vendor_name: str):
    try:
        # Generate mock data for next 12 months
        current_date = datetime.now()
        forecast_data = []
        
        for i in range(12):
            future_date = current_date + timedelta(days=30 * (i + 1))
            forecast_data.append({
                'month': future_date.strftime("%m-%Y"),
                'predicted_cost': 0.00
            })
            
        return JSONResponse(
            status_code=200,
            content={
                "data": forecast_data,
                "message": "Successfully retrieved forecast"
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "message": str(e),
                "code": "INTERNAL_ERROR"
            }
        )

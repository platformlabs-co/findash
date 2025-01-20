from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.helpers.database import get_db
from app.helpers.auth import get_authenticated_user
from app.models import User
from app.routers.models import BudgetPlanCreate
from app.services.budget_service import BudgetService

router = APIRouter(prefix="/v1/budget-plans", tags=["budget"])


def get_user(
    auth_user: dict = Depends(get_authenticated_user), db: Session = Depends(get_db)
) -> User:
    user = db.query(User).filter(User.sub == auth_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("")
async def create_budget_plan(
    plan: BudgetPlanCreate,
    user: User = Depends(get_user),
    db: Session = Depends(get_db),
):
    """Create or update a budget plan"""
    service = BudgetService(db, user)
    # The service will handle finding and updating existing plans
    return {"data": service.create_budget_plan(plan), "status": "success"}


@router.get("")
async def get_budget_plans(
    vendor: str, user: User = Depends(get_user), db: Session = Depends(get_db)
):
    """Get all budget plans for a vendor"""
    service = BudgetService(db, user)
    plans = service.get_budget_plans(vendor)
    return {"data": plans, "status": "success"}


@router.put("/{plan_id}")
async def update_budget_plan(
    plan_id: int,
    plan: BudgetPlanCreate,
    user: User = Depends(get_user),
    db: Session = Depends(get_db),
):
    """Update an existing budget plan"""
    service = BudgetService(db, user)
    return {"data": service.update_budget_plan(plan_id, plan), "status": "success"}


@router.delete("/{plan_id}")
async def delete_budget_plan(
    plan_id: int, user: User = Depends(get_user), db: Session = Depends(get_db)
):
    """Delete a budget plan"""
    service = BudgetService(db, user)
    service.delete_budget_plan(plan_id)
    return {"message": "Budget plan deleted successfully"}

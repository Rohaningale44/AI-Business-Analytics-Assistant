from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.schemas import AskRequest, AskResponse, CustomerCreate, OrderCreate, ProductCreate
from app.services.ai_assistant import AIAssistant
from app.services.analytics import AnalyticsService
from app.services.data_service import DataService
from app.utils.validation import validate_question

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/customers")
def create_customer(payload: CustomerCreate, db: Session = Depends(get_db)):
    c = DataService(db).create_customer(payload.name, payload.region, payload.segment)
    return {"id": c.id, "name": c.name, "region": c.region, "segment": c.segment}


@router.get("/customers")
def list_customers(db: Session = Depends(get_db)):
    return [
        {"id": c.id, "name": c.name, "region": c.region, "segment": c.segment}
        for c in DataService(db).list_customers()
    ]


@router.post("/products")
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    p = DataService(db).create_product(payload.name, payload.category)
    return {"id": p.id, "name": p.name, "category": p.category}


@router.get("/products")
def list_products(db: Session = Depends(get_db)):
    return [
        {"id": p.id, "name": p.name, "category": p.category}
        for p in DataService(db).list_products()
    ]


@router.post("/orders")
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    try:
        o = DataService(db).create_order(
            payload.customer_id, payload.product_id,
            payload.order_date, payload.quantity, payload.amount
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return {
        "id": o.id, "customer_id": o.customer_id, "product_id": o.product_id,
        "order_date": o.order_date, "quantity": o.quantity, "amount": o.amount
    }


@router.get("/orders")
def list_orders(db: Session = Depends(get_db)):
    return [
        {
            "id": o.id, "customer_id": o.customer_id, "product_id": o.product_id,
            "order_date": o.order_date, "quantity": o.quantity, "amount": o.amount
        }
        for o in DataService(db).list_orders()
    ]


@router.get("/analytics/summary")
def analytics_summary(db: Session = Depends(get_db)):
    return AnalyticsService(db).kpis()


@router.get("/analytics/products")
def analytics_products(db: Session = Depends(get_db)):
    return AnalyticsService(db).sales_by_product()


@router.get("/analytics/regions")
def analytics_regions(db: Session = Depends(get_db)):
    return AnalyticsService(db).sales_by_region()


@router.get("/analytics/monthly")
def analytics_monthly(db: Session = Depends(get_db)):
    return AnalyticsService(db).sales_by_month()


@router.get("/analytics/customers")
def analytics_customers(db: Session = Depends(get_db)):
    return AnalyticsService(db).top_customers()


@router.get("/analytics/powerbi/attendance")
def powerbi_ready_data(db: Session = Depends(get_db)):
    analytics = AnalyticsService(db)
    return {
        "kpis": analytics.kpis(),
        "monthly": analytics.sales_by_month(),
        "products": analytics.sales_by_product(),
        "regions": analytics.sales_by_region(),
    }


@router.post("/ai/ask", response_model=AskResponse)
def ask_ai(payload: AskRequest, db: Session = Depends(get_db)):
    question = validate_question(payload.question)
    answer, data = AIAssistant(db).ask(question)
    return AskResponse(answer=answer, data=data)

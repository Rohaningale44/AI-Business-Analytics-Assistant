from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.database import Customer, Order, Product


class AnalyticsService:
    # Deterministic business analytics. No LLM is used for calculations.

    def __init__(self, db: Session):
        self.db = db

    def total_sales(self):
        total = self.db.scalar(select(func.coalesce(func.sum(Order.amount), 0.0)))
        return {"total_sales": round(float(total or 0), 2)}

    def total_orders(self):
        total = self.db.scalar(select(func.count(Order.id))) or 0
        return {"total_orders": int(total)}

    def total_customers(self):
        total = self.db.scalar(select(func.count(Customer.id))) or 0
        return {"total_customers": int(total)}

    def average_order_value(self):
        value = self.db.scalar(select(func.coalesce(func.avg(Order.amount), 0.0)))
        return {"average_order_value": round(float(value or 0), 2)}

    def sales_by_product(self):
        rows = self.db.execute(
            select(Product.name, func.sum(Order.amount).label("revenue"))
            .join(Order, Order.product_id == Product.id)
            .group_by(Product.id, Product.name)
            .order_by(func.sum(Order.amount).desc())
        ).all()
        return [{"product": n, "revenue": round(float(r or 0), 2)} for n, r in rows]

    def sales_by_region(self):
        rows = self.db.execute(
            select(Customer.region, func.sum(Order.amount).label("revenue"))
            .join(Order, Order.customer_id == Customer.id)
            .group_by(Customer.region)
            .order_by(func.sum(Order.amount).desc())
        ).all()
        return [{"region": n, "revenue": round(float(r or 0), 2)} for n, r in rows]

    def sales_by_month(self):
        rows = self.db.execute(
            select(
                func.strftime("%Y-%m", Order.order_date).label("month"),
                func.sum(Order.amount).label("revenue"),
            )
            .group_by(func.strftime("%Y-%m", Order.order_date))
            .order_by(func.strftime("%Y-%m", Order.order_date))
        ).all()
        return [{"month": m, "revenue": round(float(r or 0), 2)} for m, r in rows]

    def top_customers(self, limit=5):
        rows = self.db.execute(
            select(Customer.name, func.sum(Order.amount).label("revenue"))
            .join(Order, Order.customer_id == Customer.id)
            .group_by(Customer.id, Customer.name)
            .order_by(func.sum(Order.amount).desc())
            .limit(limit)
        ).all()
        return [{"customer": n, "revenue": round(float(r or 0), 2)} for n, r in rows]

    def kpis(self):
        return {
            "total_sales": self.total_sales()["total_sales"],
            "total_orders": self.total_orders()["total_orders"],
            "total_customers": self.total_customers()["total_customers"],
            "average_order_value": self.average_order_value()["average_order_value"],
        }

    def snapshot(self):
        return {
            "kpis": self.kpis(),
            "sales_by_product": self.sales_by_product(),
            "sales_by_region": self.sales_by_region(),
            "sales_by_month": self.sales_by_month(),
            "top_customers": self.top_customers(),
        }

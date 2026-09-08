from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.database import Customer, Order, Product


class DataService:
    def __init__(self, db: Session):
        self.db = db

    def create_customer(self, name, region, segment):
        customer = Customer(name=name, region=region, segment=segment)
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def list_customers(self):
        return list(self.db.scalars(select(Customer)).all())

    def create_product(self, name, category):
        product = Product(name=name, category=category)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def list_products(self):
        return list(self.db.scalars(select(Product)).all())

    def create_order(self, customer_id, product_id, order_date, quantity, amount):
        customer = self.db.get(Customer, customer_id)
        product = self.db.get(Product, product_id)

        if not customer:
            raise ValueError("Customer not found.")
        if not product:
            raise ValueError("Product not found.")

        order = Order(
            customer_id=customer_id,
            product_id=product_id,
            order_date=order_date,
            quantity=quantity,
            amount=amount,
        )
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def list_orders(self):
        return list(self.db.scalars(select(Order)).all())

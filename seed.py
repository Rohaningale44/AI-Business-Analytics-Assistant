from datetime import date

from app.db import SessionLocal, init_db
from app.models.database import Customer, Order, Product


def seed():
    init_db()
    db = SessionLocal()

    try:
        if db.query(Customer).count() > 0:
            print("Database already contains data. Seed skipped.")
            return

        customers = [
            Customer(name="Rahul Mehta", region="West", segment="Enterprise"),
            Customer(name="Priya Shah", region="West", segment="SMB"),
            Customer(name="Amit Kumar", region="North", segment="Enterprise"),
            Customer(name="Neha Patil", region="South", segment="SMB"),
            Customer(name="Vikram Singh", region="North", segment="Enterprise"),
        ]

        products = [
            Product(name="Laptop", category="Computing"),
            Product(name="Monitor", category="Display"),
            Product(name="Keyboard", category="Accessories"),
            Product(name="Server", category="Infrastructure"),
        ]

        db.add_all(customers)
        db.add_all(products)
        db.flush()

        orders = [
            Order(customer_id=1, product_id=1, order_date=date(2026,1,10), quantity=5, amount=500000),
            Order(customer_id=2, product_id=2, order_date=date(2026,1,18), quantity=10, amount=250000),
            Order(customer_id=3, product_id=4, order_date=date(2026,2,5), quantity=2, amount=800000),
            Order(customer_id=4, product_id=3, order_date=date(2026,2,20), quantity=20, amount=100000),
            Order(customer_id=1, product_id=1, order_date=date(2026,3,7), quantity=8, amount=800000),
            Order(customer_id=5, product_id=4, order_date=date(2026,3,25), quantity=3, amount=1200000),
            Order(customer_id=2, product_id=2, order_date=date(2026,4,3), quantity=15, amount=375000),
            Order(customer_id=3, product_id=1, order_date=date(2026,4,17), quantity=10, amount=1000000),
            Order(customer_id=4, product_id=3, order_date=date(2026,5,11), quantity=30, amount=150000),
            Order(customer_id=5, product_id=4, order_date=date(2026,5,28), quantity=4, amount=1600000),
            Order(customer_id=1, product_id=1, order_date=date(2026,6,8), quantity=12, amount=1200000),
            Order(customer_id=2, product_id=2, order_date=date(2026,6,21), quantity=20, amount=500000),
        ]

        db.add_all(orders)
        db.commit()
        print("Seed completed successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()

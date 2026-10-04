from sqlalchemy import Float, create_engine, String, select
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column, Session

from typing import Optional
from datetime import datetime



engine = create_engine("sqlite:///product_catalog.db", echo=True
)

class Base(DeclarativeBase):
    pass

# -----------
# CATEGORY MODEL
# -----------
class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    # id INTEGER PRIMARY KEY AUTOINCREMENT

    name: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True
    )
    #name  (string, not null, unique)

    description: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True
    )
    #description (optional string)

    def __repr__(self):
        return f"Category(id={self.id}, name='{self.name}', description='{self.description}')"
    # -----------
# PRODUCT MODEL
# -----------
class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    # id INTEGER PRIMARY KEY AUTOINCREMENT

    name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )
    #name  (string, not null)

    price: Mapped[float] = mapped_column(
        Float, nullable=False
    )
    #price (float, not null)

    in_stock: Mapped[bool] = mapped_column(default=True)
    #in_stock (boolean, default True)

    category_name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )
    #category_name (string, not null)
    def __repr__(self):
        return f"Product(id={self.id}, name='{self.name}', price={self.price}, in_stock={self.in_stock}, category_name='{self.category_name}')"
# -----------
# CREATE TABLES
# -----------
Base.metadata.create_all(engine) 

# -----------
# ADD DATA
# -----------
with Session(engine) as session:

    # Create 3 new categories
    new_category1 = Category(name="Electronics", description="Electronic gadgets and devices")
    new_category2 = Category(name="Books", description="Educational and recreational books")
    new_category3 = Category(name="Clothing", description="Apparel and accessories")

    session.add(new_category1)
    session.add(new_category2)
    session.add(new_category3)
    


    # Create 6 new products
    new_product1 = Product(name="Smartphone", price=699.99, in_stock=True, category_name="Electronics")
    new_product2 = Product(name="Laptop", price=1299.99, in_stock=True, category_name="Electronics")
    new_product3 = Product(name="Python Programming Book", price=29.99, in_stock=True, category_name="Books")
    new_product4 = Product(name="Java Programming Book", price=39.99, in_stock=False, category_name="Books")
    new_product5 = Product(name="T-Shirt", price=19.99, in_stock=True, category_name="Clothing")
    new_product6 = Product(name="Jeans", price=49.99, in_stock=True, category_name="Clothing")

    session.add(new_product1)
    session.add(new_product2)
    session.add(new_product3)
    session.add(new_product4)
    session.add(new_product5)
    session.add(new_product6)
    session.commit()

# -----------------------
# QUERY ALL CATEGORIES
# -----------------------
with Session(engine) as session:

    statement = select(Category)

    categories = session.scalars(statement).all()  

    for category in categories:
        print(category)

# -----------------------
# QUERY ALL PRODUCTS in stock
# -----------------------

with Session(engine) as session:

    statement = select(Product).where(Product.in_stock == True)

    products_in_stock = session.scalars(statement).all()  

    for product in products_in_stock:
        print(product)

# -----------------------
# QUERY ALL PRODUCTS < $50  
# -----------------------

with Session(engine) as session:

    statement = select(Product).where(Product.price < 50)

    products_under_50 = session.scalars(statement).all()  

    for product in products_under_50:
        print(product)
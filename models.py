from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

class Product(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100))
    description: Mapped[str] = mapped_column(db.String(200))
    price: Mapped[float]
    qty: Mapped[int]
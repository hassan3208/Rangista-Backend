from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import models

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment variables")

# Connect to Supabase
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_data():
    db: Session = SessionLocal()

    # Clear existing data in products table
    db.query(models.Product).delete()
    db.commit()

    # -------------------
    # PRODUCTS (all collections, with new images and 6 sizes)
    # -------------------
    products = [
        models.Product(
            id="eid-1",
            name="Eid Bloom Kurta",
            image="https://images.unsplash.com/photo-1541099649105-f69ad21f3246?q=80&w=1200&auto=format&fit=crop",
            images=[
                "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?q=80&w=1200&auto=format&fit=crop",
                "https://images.unsplash.com/photo-1487412947147-5cebf100ffc2?q=80&w=1200&auto=format&fit=crop"
            ],
            collection="Eid Collection",
            XS_price=1800, S_price=2000, M_price=2200, L_price=2400, XL_price=2600, XXL_price=2800,
            XS_stock=10, S_stock=15, M_stock=20, L_stock=15, XL_stock=10, XXL_stock=5,
            kids=False
        ),
        models.Product(
            id="eid-2",
            name="Festive Grace Kurti",
            image="https://images.unsplash.com/photo-1487412947147-5cebf100ffc2?q=80&w=1200&auto=format&fit=crop",
            images=[
                "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?q=80&w=1200&auto=format&fit=crop",
                "https://images.unsplash.com/photo-1487412947147-5cebf100ffc2?q=80&w=1200&auto=format&fit=crop"
            ],
            collection="Eid Collection",
            XS_price=2300, S_price=2500, M_price=2700, L_price=2900, XL_price=3100, XXL_price=3300,
            XS_stock=20, S_stock=25, M_stock=30, L_stock=25, XL_stock=20, XXL_stock=15,
            kids=False
        ),
        models.Product(
            id="ind-1",
            name="Azadi Kurta Green",
            image="https://images.unsplash.com/photo-1541099649105-f69ad21f3246?q=80&w=1200&auto=format&fit=crop",
            images=[
                "https://images.unsplash.com/photo-1487412947147-5cebf100ffc2?q=80&w=1200&auto=format&fit=crop",
                "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?q=80&w=1200&auto=format&fit=crop"
            ],
            collection="14 August Independence Collection",
            XS_price=1600, S_price=1800, M_price=2000, L_price=2200, XL_price=2400, XXL_price=2600,
            XS_stock=25, S_stock=30, M_stock=35, L_stock=30, XL_stock=25, XXL_stock=20,
            kids=True
        ),
    ]
    db.add_all(products)
    db.commit()

    db.close()
    print("✅ All collections (Eid + Independence) seeded successfully!")

if __name__ == "__main__":
    seed_data()

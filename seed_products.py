from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models

# Drop and recreate all tables (for clean seeding)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def seed_data():
    db: Session = SessionLocal()

    # Clear existing data
    db.query(models.PriceAndStock).delete()
    db.query(models.Product).delete()
    db.commit()

    # -------------------
    # PRODUCTS (all collections, with new images)
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
        ),
    ]
    db.add_all(products)
    db.commit()

    # -------------------
    # PRICE AND STOCK
    # -------------------
    price_stocks = [
        models.PriceAndStock(
            S_price=2000, M_price=2200, L_price=2400,
            S_stock=10, M_stock=15, L_stock=5,
            kids=False, product_id="eid-1"
        ),
        models.PriceAndStock(
            S_price=2500, M_price=2700, L_price=3000,
            S_stock=20, M_stock=18, L_stock=8,
            kids=False, product_id="eid-2"
        ),
        models.PriceAndStock(
            S_price=1800, M_price=2000, L_price=2200,
            S_stock=25, M_stock=30, L_stock=10,
            kids=True, product_id="ind-1"
        ),
    ]
    db.add_all(price_stocks)
    db.commit()

    db.close()
    print("✅ All collections (Eid + Independence) seeded successfully!")

if __name__ == "__main__":
    seed_data()
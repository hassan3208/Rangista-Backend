# from sqlalchemy import Column, Integer, String, Boolean, Float, Date, ForeignKey, JSON
# from sqlalchemy.orm import relationship
# from database import Base

# # -------------------------
# # USERS TABLE
# # -------------------------
# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, nullable=False)
#     email = Column(String, unique=True, nullable=False)
#     name = Column(String, nullable=False)
#     hashed_password = Column(String, nullable=False)
#     disabled = Column(Boolean, default=False)
#     contact_number = Column(String, nullable=False) 
#     permanent_address = Column(String, nullable=False) 
#     country = Column(String, nullable=False) 
#     city = Column(String, nullable=False) 
#     contact_number_2 = Column(String, nullable=True) 

#     # Relationships
#     reviews = relationship("Review", back_populates="user", cascade="all, delete")
#     carts = relationship("Cart", back_populates="user", cascade="all, delete")
#     orders = relationship("Order", back_populates="user", cascade="all, delete")

# # -------------------------
# # PRODUCTS TABLE (merged with PriceAndStock)
# # -------------------------
# class Product(Base):
#     __tablename__ = "products"

#     id = Column(String, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     image = Column(String, nullable=False)
#     images = Column(JSON, nullable=True)  # List of image URLs
#     collection = Column(String(50), nullable=False)
#     XS_price = Column(Integer, nullable=False)
#     S_price = Column(Integer, nullable=False)
#     M_price = Column(Integer, nullable=False)
#     L_price = Column(Integer, nullable=False)
#     XL_price = Column(Integer, nullable=False)
#     XXL_price = Column(Integer, nullable=False)
#     XS_stock = Column(Float, nullable=False)
#     S_stock = Column(Float, nullable=False)
#     M_stock = Column(Float, nullable=False)
#     L_stock = Column(Float, nullable=False)
#     XL_stock = Column(Float, nullable=False)
#     XXL_stock = Column(Float, nullable=False)
#     kids = Column(Boolean, nullable=True)

#     # Relationships
#     reviews = relationship("Review", back_populates="product", cascade="all, delete")
#     carts = relationship("Cart", back_populates="product", cascade="all, delete")
#     order_items = relationship("OrderItem", back_populates="product", cascade="all, delete")

# # -------------------------
# # REVIEWS TABLE
# # -------------------------
# class Review(Base):
#     __tablename__ = "reviews"

#     id = Column(Integer, primary_key=True, index=True)
#     stars = Column(Float, nullable=False)
#     text = Column(String, nullable=True)
#     time = Column(Date, nullable=False)
#     user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
#     product_id = Column(String, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)

#     # Relationships
#     user = relationship("User", back_populates="reviews")
#     product = relationship("Product", back_populates="reviews")

# # -------------------------
# # CART TABLE
# # -------------------------
# class Cart(Base):
#     __tablename__ = "cart"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
#     product_id = Column(String, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
#     size = Column(String(5), nullable=False)  # XS, S, M, L, XL, XXL
#     quantity = Column(Integer, default=1, nullable=False)

#     # Relationships
#     user = relationship("User", back_populates="carts")
#     product = relationship("Product", back_populates="carts")

# # -------------------------
# # ORDERS TABLE
# # -------------------------
# class Order(Base):
#     __tablename__ = "orders"

#     id = Column(Integer, primary_key=True, index=True)
#     status = Column(String, nullable=False)
#     time = Column(Date, nullable=False)
#     user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

#     # Relationships
#     user = relationship("User", back_populates="orders")
#     items = relationship("OrderItem", back_populates="order", cascade="all, delete")

# # -------------------------
# # ORDER ITEMS TABLE
# # -------------------------
# class OrderItem(Base):
#     __tablename__ = "order_items"

#     id = Column(Integer, primary_key=True, index=True)
#     order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
#     product_id = Column(String, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
#     size = Column(String(5), nullable=False)  # XS, S, M, L, XL, XXL
#     quantity = Column(Integer, default=1, nullable=False)

#     # Relationships
#     order = relationship("Order", back_populates="items")
#     product = relationship("Product", back_populates="order_items")





from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)
    contact_number = Column(String)
    permanent_address = Column(String)
    country = Column(String)
    city = Column(String)
    contact_number_2 = Column(String)

class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, unique=True, index=True, nullable=False)
    token_type = Column(String, nullable=False)  # 'access' or 'refresh'
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Product(Base):
    __tablename__ = "products"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    image = Column(String)
    images = Column(String)
    collection = Column(String)
    XS_price = Column(Integer)
    S_price = Column(Integer)
    M_price = Column(Integer)
    L_price = Column(Integer)
    XL_price = Column(Integer)
    XXL_price = Column(Integer)
    XS_stock = Column(Integer)
    S_stock = Column(Integer)
    M_stock = Column(Integer)
    L_stock = Column(Integer)
    XL_stock = Column(Integer)
    XXL_stock = Column(Integer)
    kids = Column(Boolean)

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    stars = Column(Integer, nullable=False)
    text = Column(String)
    time = Column(DateTime(timezone=True), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)

class Cart(Base):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    size = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, nullable=False)
    time = Column(DateTime(timezone=True), nullable=False)

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    size = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
# from sqlalchemy.orm import Session
# from sqlalchemy import func
# import models, schemas
# from models import User, Order, Product
# from passlib.context import CryptContext
# from datetime import date
# from typing import Optional
# from fastapi import HTTPException


# pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# # -------------------------
# # USER FUNCTIONS
# # -------------------------
# def get_user_by_login(db: Session, login: str):
#     return db.query(models.User).filter(
#         (models.User.username == login) |
#         (models.User.email == login) |
#         (models.User.contact_number == login)
#     ).first()

# def get_user_by_username(db: Session, username: str):
#     return db.query(models.User).filter(models.User.username == username).first()

# def get_user_by_email(db: Session, email: str): 
#     return db.query(models.User).filter(models.User.email == email).first()  

# def get_all_users(db: Session):
#     return db.query(models.User).all()

# def create_user(db: Session, user: schemas.UserCreate): 
#     hashed_password = pwd_context.hash(user.password) 
#     db_user = models.User( 
#         name=user.name, 
#         username=user.username, 
#         email=user.email, 
#         hashed_password=hashed_password, 
#         disabled=False, 
#         contact_number=user.contact_number, 
#         permanent_address=user.permanent_address, 
#         country=user.country, 
#         city=user.city, 
#         contact_number_2=user.contact_number_2
#     ) 
#     db.add(db_user) 
#     db.commit() 
#     db.refresh(db_user) 
#     return db_user

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def update_user(db: Session, db_user: models.User, updates: schemas.UserUpdate): 
#     if updates.email is not None: 
#         db_user.email = updates.email 
#     if updates.full_name is not None: 
#         db_user.name = updates.full_name 
#     if updates.disabled is not None: 
#         db_user.disabled = updates.disabled 
#     if updates.contact_number is not None: 
#         db_user.contact_number = updates.contact_number 
#     if updates.permanent_address is not None: 
#         db_user.permanent_address = updates.permanent_address 
#     if updates.country is not None: 
#         db_user.country = updates.country 
#     if updates.city is not None: 
#         db_user.city = updates.city 
#     if updates.contact_number_2 is not None: 
#         db_user.contact_number_2 = updates.contact_number_2
#     db.commit() 
#     db.refresh(db_user) 
#     return db_user

# # -------------------------
# # PRODUCT FUNCTIONS
# # -------------------------
# def get_all_products_with_reviews(db: Session):
#     """
#     Fetch all products with:
#     - total number of reviews
#     - average rating
#     - price and stock info (XS/S/M/L/XL/XXL, kids)
#     """
#     results = (
#         db.query(
#             models.Product.id,
#             models.Product.name,
#             models.Product.image,
#             models.Product.images,
#             models.Product.collection,
#             func.count(models.Review.id).label("total_reviews"),
#             func.coalesce(func.avg(models.Review.stars), 0).label("average_rating"),
#             models.Product.XS_price,
#             models.Product.S_price,
#             models.Product.M_price,
#             models.Product.L_price,
#             models.Product.XL_price,
#             models.Product.XXL_price,
#             models.Product.XS_stock,
#             models.Product.S_stock,
#             models.Product.M_stock,
#             models.Product.L_stock,
#             models.Product.XL_stock,
#             models.Product.XXL_stock,
#             models.Product.kids,
#         )
#         .outerjoin(models.Review, models.Product.id == models.Review.product_id)
#         .group_by(models.Product.id)
#         .all()
#     )

#     products = []
#     for r in results:
#         products.append(
#             schemas.ProductResponse(
#                 id=r.id,
#                 name=r.name,
#                 image=r.image,
#                 images=r.images,
#                 collection=r.collection,
#                 total_reviews=r.total_reviews,
#                 average_rating=round(float(r.average_rating or 0), 2),
#                 XS_price=r.XS_price,
#                 S_price=r.S_price,
#                 M_price=r.M_price,
#                 L_price=r.L_price,
#                 XL_price=r.XL_price,
#                 XXL_price=r.XXL_price,
#                 XS_stock=r.XS_stock,
#                 S_stock=r.S_stock,
#                 M_stock=r.M_stock,
#                 L_stock=r.L_stock,
#                 XL_stock=r.XL_stock,
#                 XXL_stock=r.XXL_stock,
#                 kids=r.kids,
#             )
#         )
#     return products

# # -------------------------
# # REVIEW FUNCTIONS
# # -------------------------
# def get_reviews_by_product(db: Session, product_id: str):
#     """
#     Fetch all reviews for a specific product, including username, stars, text, and time.
#     """
#     results = (
#         db.query(
#             models.User.username,
#             models.Review.stars,
#             models.Review.text,
#             models.Review.time,
#         )
#         .join(models.Review, models.User.id == models.Review.user_id)
#         .filter(models.Review.product_id == product_id)
#         .order_by(models.Review.time.desc())  # Latest first
#         .all()
#     )

#     return [
#         schemas.ReviewDetail(
#             username=r.username,
#             stars=r.stars,
#             text=r.text,
#             time=r.time,
#         )
#         for r in results
#     ]

# # -------------------------
# # GET ALL PRODUCTS IN USER CART
# # -------------------------
# def get_user_cart(db: Session, user_id: int):
#     """
#     Returns all products in a user's cart with product name, collection,
#     size, quantity, image, user_id, product_id, product price, and total number of distinct products.
#     """
#     results = (
#         db.query(
#             models.Product.name.label("product_name"),
#             models.Product.collection.label("collection"),
#             models.Cart.size.label("size"),
#             models.Cart.quantity.label("quantity"),
#             models.Product.image.label("image"),
#             models.Cart.user_id.label("user_id"),
#             models.Cart.product_id.label("product_id"),
#             models.Product.XS_price,
#             models.Product.S_price,
#             models.Product.M_price,
#             models.Product.L_price,
#             models.Product.XL_price,
#             models.Product.XXL_price,
#         )
#         .join(models.Cart, models.Product.id == models.Cart.product_id)
#         .filter(models.Cart.user_id == user_id)
#         .all()
#     )

#     items = []
#     for r in results:
#         price = (
#             r.XS_price if r.size == "XS" else
#             r.S_price if r.size == "S" else
#             r.M_price if r.size == "M" else
#             r.L_price if r.size == "L" else
#             r.XL_price if r.size == "XL" else
#             r.XXL_price if r.size == "XXL" else 0
#         ) * r.quantity

#         items.append(
#             schemas.CartProduct(
#                 product_name=r.product_name,
#                 collection=r.collection,
#                 size=r.size,
#                 quantity=r.quantity,
#                 image=r.image,
#                 user_id=r.user_id,
#                 product_id=r.product_id,
#                 price=price,
#             )
#         )

#     total_products = len(items)
#     return schemas.CartResponse(total_products=total_products, items=items)

# # -------------------------
# # GET ALL ORDERS OF ALL USERS
# # -------------------------
# def get_all_orders(db: Session):
#     """
#     Fetch all orders from all users with product details.
#     """
#     results = (
#         db.query(
#             models.Order.id.label("order_id"),
#             models.Order.user_id,
#             models.User.username,
#             models.Order.status,
#             models.Order.time.label("order_time"),
#             func.count(models.OrderItem.id).label("total_products"),
#             func.sum(
#                 models.OrderItem.quantity * (
#                     models.Product.XS_price * (models.OrderItem.size == "XS") +
#                     models.Product.S_price * (models.OrderItem.size == "S") +
#                     models.Product.M_price * (models.OrderItem.size == "M") +
#                     models.Product.L_price * (models.OrderItem.size == "L") +
#                     models.Product.XL_price * (models.OrderItem.size == "XL") +
#                     models.Product.XXL_price * (models.OrderItem.size == "XXL")
#                 )
#             ).label("total_price")
#         )
#         .join(models.User, models.Order.user_id == models.User.id)
#         .join(models.OrderItem, models.Order.id == models.OrderItem.order_id)
#         .join(models.Product, models.OrderItem.product_id == models.Product.id)
#         .group_by(models.Order.id, models.User.username)
#         .all()
#     )

#     orders = []
#     for r in results:
#         order_items = db.query(
#             models.OrderItem.quantity,
#             models.OrderItem.size,
#             models.OrderItem.product_id,
#             models.Product.name.label("product_name"),
#             models.Product.XS_price,
#             models.Product.S_price,
#             models.Product.M_price,
#             models.Product.L_price,
#             models.Product.XL_price,
#             models.Product.XXL_price,
#         ).join(
#             models.Product, models.OrderItem.product_id == models.Product.id
#         ).filter(
#             models.OrderItem.order_id == r.order_id
#         ).all()

#         products = [
#             schemas.OrderProduct(
#                 product_name=item.product_name,
#                 quantity=item.quantity,
#                 size=item.size,
#                 product_id=item.product_id,
#                 price=(
#                     item.XS_price if item.size == "XS" else
#                     item.S_price if item.size == "S" else
#                     item.M_price if item.size == "M" else
#                     item.L_price if item.size == "L" else
#                     item.XL_price if item.size == "XL" else
#                     item.XXL_price if item.size == "XXL" else 0
#                 ) * item.quantity
#             )
#             for item in order_items
#         ]

#         orders.append(
#             schemas.OrderResponse(
#                 order_id=r.order_id,
#                 user_id=r.user_id,
#                 username=r.username,
#                 status=r.status,
#                 total_products=r.total_products,
#                 total_price=int(r.total_price or 0),
#                 products=products,
#                 order_time=r.order_time
#             )
#         )
#     return orders

# # -------------------------
# # GET USER ORDERS
# # -------------------------
# def get_user_orders(db: Session, user_id: int):
#     """
#     Fetch all orders for a specific user with product details.
#     """
#     results = (
#         db.query(
#             models.Order.id.label("order_id"),
#             models.Order.user_id,
#             models.User.username,
#             models.Order.status,
#             models.Order.time.label("order_time"),
#             func.count(models.OrderItem.id).label("total_products"),
#             func.sum(
#                 models.OrderItem.quantity * (
#                     models.Product.XS_price * (models.OrderItem.size == "XS") +
#                     models.Product.S_price * (models.OrderItem.size == "S") +
#                     models.Product.M_price * (models.OrderItem.size == "M") +
#                     models.Product.L_price * (models.OrderItem.size == "L") +
#                     models.Product.XL_price * (models.OrderItem.size == "XL") +
#                     models.Product.XXL_price * (models.OrderItem.size == "XXL")
#                 )
#             ).label("total_price")
#         )
#         .join(models.User, models.Order.user_id == models.User.id)
#         .join(models.OrderItem, models.Order.id == models.OrderItem.order_id)
#         .join(models.Product, models.OrderItem.product_id == models.Product.id)
#         .filter(models.Order.user_id == user_id)
#         .group_by(models.Order.id, models.User.username)
#         .all()
#     )

#     orders = []
#     for r in results:
#         order_items = db.query(
#             models.OrderItem.quantity,
#             models.OrderItem.size,
#             models.OrderItem.product_id,
#             models.Product.name.label("product_name"),
#             models.Product.XS_price,
#             models.Product.S_price,
#             models.Product.M_price,
#             models.Product.L_price,
#             models.Product.XL_price,
#             models.Product.XXL_price,
#         ).join(
#             models.Product, models.OrderItem.product_id == models.Product.id
#         ).filter(
#             models.OrderItem.order_id == r.order_id
#         ).all()

#         products = [
#             schemas.OrderProduct(
#                 product_name=item.product_name,
#                 quantity=item.quantity,
#                 size=item.size,
#                 product_id=item.product_id,
#                 price=(
#                     item.XS_price if item.size == "XS" else
#                     item.S_price if item.size == "S" else
#                     item.M_price if item.size == "M" else
#                     item.L_price if item.size == "L" else
#                     item.XL_price if item.size == "XL" else
#                     item.XXL_price if item.size == "XXL" else 0
#                 ) * item.quantity
#             )
#             for item in order_items
#         ]

#         orders.append(
#             schemas.OrderResponse(
#                 order_id=r.order_id,
#                 user_id=r.user_id,
#                 username=r.username,
#                 status=r.status,
#                 total_products=r.total_products,
#                 total_price=int(r.total_price or 0),
#                 products=products,
#                 order_time=r.order_time
#             )
#         )
#     return orders

# # -------------------------
# # GET ORDER BY ID
# # -------------------------
# def get_order(db: Session, order_id: int):
#     """
#     Fetch a specific order with product details.
#     """
#     result = (
#         db.query(
#             models.Order.id.label("order_id"),
#             models.Order.user_id,
#             models.User.username,
#             models.Order.status,
#             models.Order.time.label("order_time"),
#             func.count(models.OrderItem.id).label("total_products"),
#             func.sum(
#                 models.OrderItem.quantity * (
#                     models.Product.XS_price * (models.OrderItem.size == "XS") +
#                     models.Product.S_price * (models.OrderItem.size == "S") +
#                     models.Product.M_price * (models.OrderItem.size == "M") +
#                     models.Product.L_price * (models.OrderItem.size == "L") +
#                     models.Product.XL_price * (models.OrderItem.size == "XL") +
#                     models.Product.XXL_price * (models.OrderItem.size == "XXL")
#                 )
#             ).label("total_price")
#         )
#         .join(models.User, models.Order.user_id == models.User.id)
#         .join(models.OrderItem, models.Order.id == models.OrderItem.order_id)
#         .join(models.Product, models.OrderItem.product_id == models.Product.id)
#         .filter(models.Order.id == order_id)
#         .group_by(models.Order.id, models.User.username)
#         .first()
#     )

#     if not result:
#         return None

#     order_items = db.query(
#         models.OrderItem.quantity,
#         models.OrderItem.size,
#         models.OrderItem.product_id,
#         models.Product.name.label("product_name"),
#         models.Product.XS_price,
#         models.Product.S_price,
#         models.Product.M_price,
#         models.Product.L_price,
#         models.Product.XL_price,
#         models.Product.XXL_price,
#     ).join(
#         models.Product, models.OrderItem.product_id == models.Product.id
#     ).filter(
#         models.OrderItem.order_id == result.order_id
#     ).all()

#     products = [
#         schemas.OrderProduct(
#             product_name=item.product_name,
#             quantity=item.quantity,
#             size=item.size,
#             product_id=item.product_id,
#             price=(
#                 item.XS_price if item.size == "XS" else
#                 item.S_price if item.size == "S" else
#                 item.M_price if item.size == "M" else
#                 item.L_price if item.size == "L" else
#                 item.XL_price if item.size == "XL" else
#                 item.XXL_price if item.size == "XXL" else 0
#             ) * item.quantity
#         )
#         for item in order_items
#     ]

#     return schemas.OrderResponse(
#         order_id=result.order_id,
#         user_id=result.user_id,
#         username=result.username,
#         status=result.status,
#         total_products=result.total_products,
#         total_price=int(result.total_price or 0),
#         products=products,
#         order_time=result.order_time
#     )

# # -------------------------
# # UPDATE ORDER STATUS
# # -------------------------
# def update_order_status(db: Session, order_id: int, status: str):
#     order = db.query(models.Order).filter(models.Order.id == order_id).first()
#     if not order:
#         return None
#     order.status = status
#     db.commit()
#     db.refresh(order)
#     return order

# # -------------------------
# # CREATE REVIEW
# # -------------------------
# def create_review(db: Session, review: schemas.ReviewCreate):
#     """
#     Create a review for a product.
#     """
#     # Check if user and product exist
#     user = db.query(models.User).filter(models.User.id == review.user_id).first()
#     if not user:
#         return None
#     product = db.query(models.Product).filter(models.Product.id == review.product_id).first()
#     if not product:
#         return None

#     # Check if user has already reviewed this product
#     existing_review = db.query(models.Review).filter(
#         models.Review.user_id == review.user_id,
#         models.Review.product_id == review.product_id
#     ).first()
#     if existing_review:
#         return None

#     db_review = models.Review(
#         user_id=review.user_id,
#         product_id=review.product_id,
#         stars=review.stars,
#         text=review.text,
#         time=date.fromisoformat(review.time)
#     )
#     db.add(db_review)
#     db.commit()
#     db.refresh(db_review)
#     return db_review

# # -------------------------
# # GET REVIEW DETAIL
# # -------------------------
# def get_review_detail(db: Session, review_id: int):
#     """
#     Fetch details of a specific review.
#     """
#     result = (
#         db.query(
#             models.User.username,
#             models.Review.stars,
#             models.Review.text,
#             models.Review.time
#         )
#         .join(models.User, models.User.id == models.Review.user_id)
#         .filter(models.Review.id == review_id)
#         .first()
#     )
#     if not result:
#         return None
#     return schemas.ReviewDetail(
#         username=result.username,
#         stars=result.stars,
#         text=result.text,
#         time=result.time
#     )

# # -------------------------
# # UPDATE CART QUANTITY
# # -------------------------
# def update_cart_quantity(db: Session, user_id: int, product_id: str, size: str, quantity: int):
#     """
#     Update the quantity of a cart item and adjust stock accordingly.
#     """
#     if quantity < 1:
#         raise HTTPException(status_code=400, detail="Quantity must be at least 1")

#     cart_item = db.query(models.Cart).filter(
#         models.Cart.user_id == user_id,
#         models.Cart.product_id == product_id,
#         models.Cart.size == size
#     ).first()
#     if not cart_item:
#         return None

#     product = db.query(models.Product).filter(models.Product.id == product_id).first()
#     if not product:
#         return None

#     # Calculate stock change
#     quantity_delta = quantity - cart_item.quantity

#     if quantity_delta > 0:
#         # Check if enough stock is available
#         if size == "XS" and product.XS_stock < quantity_delta:
#             raise HTTPException(status_code=400, detail="Insufficient XS stock")
#         elif size == "S" and product.S_stock < quantity_delta:
#             raise HTTPException(status_code=400, detail="Insufficient S stock")
#         elif size == "M" and product.M_stock < quantity_delta:
#             raise HTTPException(status_code=400, detail="Insufficient M stock")
#         elif size == "L" and product.L_stock < quantity_delta:
#             raise HTTPException(status_code=400, detail="Insufficient L stock")
#         elif size == "XL" and product.XL_stock < quantity_delta:
#             raise HTTPException(status_code=400, detail="Insufficient XL stock")
#         elif size == "XXL" and product.XXL_stock < quantity_delta:
#             raise HTTPException(status_code=400, detail="Insufficient XXL stock")

#         # Deduct stock
#         if size == "XS":
#             product.XS_stock -= quantity_delta
#         elif size == "S":
#             product.S_stock -= quantity_delta
#         elif size == "M":
#             product.M_stock -= quantity_delta
#         elif size == "L":
#             product.L_stock -= quantity_delta
#         elif size == "XL":
#             product.XL_stock -= quantity_delta
#         elif size == "XXL":
#             product.XXL_stock -= quantity_delta
#     elif quantity_delta < 0:
#         # Add back to stock
#         if size == "XS":
#             product.XS_stock += abs(quantity_delta)
#         elif size == "S":
#             product.S_stock += abs(quantity_delta)
#         elif size == "M":
#             product.M_stock += abs(quantity_delta)
#         elif size == "L":
#             product.L_stock += abs(quantity_delta)
#         elif size == "XL":
#             product.XL_stock += abs(quantity_delta)
#         elif size == "XXL":
#             product.XXL_stock += abs(quantity_delta)

#     # Update cart item quantity
#     cart_item.quantity = quantity
#     db.commit()
#     db.refresh(cart_item)
#     db.refresh(product)
#     return cart_item

# # -------------------------
# # REMOVE FROM CART
# # -------------------------
# def remove_from_cart(db: Session, user_id: int, product_id: str, size: str):
#     cart_item = db.query(models.Cart).filter(
#         models.Cart.user_id == user_id,
#         models.Cart.product_id == product_id,
#         models.Cart.size == size
#     ).first()
#     if not cart_item:
#         return None

#     product = db.query(models.Product).filter(models.Product.id == product_id).first()
#     if not product:
#         db.delete(cart_item)
#         db.commit()
#         return True

#     # Add back the quantity to the appropriate size stock
#     if size == "XS":
#         product.XS_stock += cart_item.quantity
#     elif size == "S":
#         product.S_stock += cart_item.quantity
#     elif size == "M":
#         product.M_stock += cart_item.quantity
#     elif size == "L":
#         product.L_stock += cart_item.quantity
#     elif size == "XL":
#         product.XL_stock += cart_item.quantity
#     elif size == "XXL":
#         product.XXL_stock += cart_item.quantity

#     # Delete the cart item
#     db.delete(cart_item)
#     db.commit()
#     db.refresh(product)
#     return True

# # -------------------------
# # ADD TO CART
# # -------------------------
# def add_to_cart(db: Session, cart_item: schemas.CartCreate):
#     """
#     Add a new item to the cart or update quantity if it already exists, and reduce stock only for net increases.
#     """
#     # Validate user and product existence
#     user = db.query(models.User).filter(models.User.id == cart_item.user_id).first()
#     if not user:
#         return None
#     product = db.query(models.Product).filter(models.Product.id == cart_item.product_id).first()
#     if not product:
#         return None

#     # Check if the item already exists in the cart
#     existing_cart_item = db.query(models.Cart).filter(
#         models.Cart.user_id == cart_item.user_id,
#         models.Cart.product_id == cart_item.product_id,
#         models.Cart.size == cart_item.size
#     ).first()

#     if existing_cart_item:
#         # Calculate delta for stock deduction (only deduct if quantity is increasing)
#         quantity_delta = cart_item.quantity - existing_cart_item.quantity
#         if quantity_delta > 0:
#             # Verify stock for the additional quantity
#             if cart_item.size == "XS" and product.XS_stock < quantity_delta:
#                 raise HTTPException(status_code=400, detail="Insufficient XS stock")
#             elif cart_item.size == "S" and product.S_stock < quantity_delta:
#                 raise HTTPException(status_code=400, detail="Insufficient S stock")
#             elif cart_item.size == "M" and product.M_stock < quantity_delta:
#                 raise HTTPException(status_code=400, detail="Insufficient M stock")
#             elif cart_item.size == "L" and product.L_stock < quantity_delta:
#                 raise HTTPException(status_code=400, detail="Insufficient L stock")
#             elif cart_item.size == "XL" and product.XL_stock < quantity_delta:
#                 raise HTTPException(status_code=400, detail="Insufficient XL stock")
#             elif cart_item.size == "XXL" and product.XXL_stock < quantity_delta:
#                 raise HTTPException(status_code=400, detail="Insufficient XXL stock")

#             # Deduct stock
#             if cart_item.size == "XS":
#                 product.XS_stock -= quantity_delta
#             elif cart_item.size == "S":
#                 product.S_stock -= quantity_delta
#             elif cart_item.size == "M":
#                 product.M_stock -= quantity_delta
#             elif cart_item.size == "L":
#                 product.L_stock -= quantity_delta
#             elif cart_item.size == "XL":
#                 product.XL_stock -= quantity_delta
#             elif cart_item.size == "XXL":
#                 product.XXL_stock -= quantity_delta
#         elif quantity_delta < 0:
#             # Add back to stock
#             if cart_item.size == "XS":
#                 product.XS_stock += abs(quantity_delta)
#             elif cart_item.size == "S":
#                 product.S_stock += abs(quantity_delta)
#             elif cart_item.size == "M":
#                 product.M_stock += abs(quantity_delta)
#             elif cart_item.size == "L":
#                 product.L_stock += abs(quantity_delta)
#             elif cart_item.size == "XL":
#                 product.XL_stock += abs(quantity_delta)
#             elif cart_item.size == "XXL":
#                 product.XXL_stock += abs(quantity_delta)

#         # Update quantity
#         existing_cart_item.quantity = cart_item.quantity
#         db.commit()
#         db.refresh(existing_cart_item)
#         db.refresh(product)
#         return existing_cart_item

#     # For new item: Verify and deduct full stock
#     if cart_item.size == "XS" and product.XS_stock < cart_item.quantity:
#         raise HTTPException(status_code=400, detail="Insufficient XS stock")
#     elif cart_item.size == "S" and product.S_stock < cart_item.quantity:
#         raise HTTPException(status_code=400, detail="Insufficient S stock")
#     elif cart_item.size == "M" and product.M_stock < cart_item.quantity:
#         raise HTTPException(status_code=400, detail="Insufficient M stock")
#     elif cart_item.size == "L" and product.L_stock < cart_item.quantity:
#         raise HTTPException(status_code=400, detail="Insufficient L stock")
#     elif cart_item.size == "XL" and product.XL_stock < cart_item.quantity:
#         raise HTTPException(status_code=400, detail="Insufficient XL stock")
#     elif cart_item.size == "XXL" and product.XXL_stock < cart_item.quantity:
#         raise HTTPException(status_code=400, detail="Insufficient XXL stock")

#     # Deduct stock
#     if cart_item.size == "XS":
#         product.XS_stock -= cart_item.quantity
#     elif cart_item.size == "S":
#         product.S_stock -= cart_item.quantity
#     elif cart_item.size == "M":
#         product.M_stock -= cart_item.quantity
#     elif cart_item.size == "L":
#         product.L_stock -= cart_item.quantity
#     elif cart_item.size == "XL":
#         product.XL_stock -= cart_item.quantity
#     elif cart_item.size == "XXL":
#         product.XXL_stock -= cart_item.quantity

#     # Create new cart item
#     db_cart_item = models.Cart(
#         user_id=cart_item.user_id,
#         product_id=cart_item.product_id,
#         size=cart_item.size,
#         quantity=cart_item.quantity
#     )
#     db.add(db_cart_item)
#     db.commit()
#     db.refresh(db_cart_item)
#     db.refresh(product)
#     return db_cart_item

# # -------------------------
# # CREATE ORDER FROM CART
# # -------------------------
# def create_order_from_cart(db: Session, order: schemas.OrderCreate):
#     """
#     Create a new order for a user using all items in their cart and clear the cart.
#     Returns the updated list of user orders.
#     """
#     # Validate user existence
#     user = db.query(models.User).filter(models.User.id == order.user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     # Fetch cart items
#     cart_items = db.query(models.Cart).filter(models.Cart.user_id == order.user_id).all()
#     if not cart_items:
#         raise HTTPException(status_code=400, detail="Cart is empty")

#     # Validate products
#     for item in cart_items:
#         product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
#         if not product:
#             raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")

#     # Create new order
#     db_order = models.Order(
#         user_id=order.user_id,
#         status="pending",
#         time=date.fromisoformat(order.order_time)
#     )
#     db.add(db_order)
#     db.commit()
#     db.refresh(db_order)

#     # Add order items from cart
#     for item in cart_items:
#         db_item = models.OrderItem(
#             order_id=db_order.id,
#             product_id=item.product_id,
#             size=item.size,
#             quantity=item.quantity
#         )
#         db.add(db_item)
#         db.commit()

#     # Clear user's cart
#     db.query(models.Cart).filter(models.Cart.user_id == order.user_id).delete()
#     db.commit()

#     # Return all user orders
#     return get_user_orders(db, order.user_id)

# # -------------------------
# # CHECK IF USER REVIEWED PRODUCT
# # -------------------------
# def has_user_reviewed_product(db: Session, user_id: int, product_id: str):
#     """
#     Check if a user has already submitted a review for a product.
#     Returns True if a review exists, False otherwise.
#     """
#     review = db.query(models.Review).filter(
#         models.Review.user_id == user_id,
#         models.Review.product_id == product_id
#     ).first()
#     return review is not None


from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas
from models import User, Order, Product, Token
from passlib.context import CryptContext
from datetime import date
from typing import Optional
from fastapi import HTTPException
import logging
from jose import jwt, JWTError
import os

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# -------------------------
# USER FUNCTIONS
# -------------------------
def get_user_by_login(db: Session, login: str):
    return db.query(models.User).filter(
        (models.User.username == login) |
        (models.User.email == login) |
        (models.User.contact_number == login)
    ).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str): 
    return db.query(models.User).filter(models.User.email == email).first()  

def get_all_users(db: Session):
    return db.query(models.User).all()

def create_user(db: Session, user: schemas.UserCreate): 
    hashed_password = pwd_context.hash(user.password) 
    db_user = models.User( 
        name=user.name, 
        username=user.username, 
        email=user.email, 
        hashed_password=hashed_password, 
        disabled=False, 
        contact_number=user.contact_number, 
        permanent_address=user.permanent_address, 
        country=user.country, 
        city=user.city, 
        contact_number_2=user.contact_number_2
    ) 
    db.add(db_user) 
    db.commit() 
    db.refresh(db_user) 
    return db_user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def update_user(db: Session, db_user: models.User, updates: schemas.UserUpdate): 
    if updates.email is not None: 
        db_user.email = updates.email 
    if updates.full_name is not None: 
        db_user.name = updates.full_name 
    if updates.disabled is not None: 
        db_user.disabled = updates.disabled 
    if updates.contact_number is not None: 
        db_user.contact_number = updates.contact_number 
    if updates.permanent_address is not None: 
        db_user.permanent_address = updates.permanent_address 
    if updates.country is not None: 
        db_user.country = updates.country 
    if updates.city is not None: 
        db_user.city = updates.city 
    if updates.contact_number_2 is not None: 
        db_user.contact_number_2 = updates.contact_number_2
    db.commit() 
    db.refresh(db_user) 
    return db_user

# -------------------------
# TOKEN FUNCTIONS
# -------------------------
def create_token(db: Session, user_id: int, token: str, token_type: str):
    try:
        logger.debug(f"Creating {token_type} token for user_id: {user_id}")
        # Delete existing token of the same type for the user
        db.query(models.Token).filter(
            models.Token.user_id == user_id,
            models.Token.token_type == token_type
        ).delete()
        db.commit()
        logger.debug(f"Deleted existing {token_type} token")
        # Create new token
        db_token = models.Token(user_id=user_id, token=token, token_type=token_type)
        db.add(db_token)
        db.commit()
        db.refresh(db_token)
        logger.debug(f"{token_type.capitalize()} token added to DB")
        return db_token
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create {token_type} token: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create {token_type} token: {str(e)}")

def get_token(db: Session, token: str, token_type: str):
    return db.query(models.Token).filter(
        models.Token.token == token,
        models.Token.token_type == token_type
    ).first()

def delete_token(db: Session, token: str, token_type: str):
    try:
        logger.debug(f"Attempting to delete {token_type} token: {token[:10]}...")
        db_token = db.query(models.Token).filter(
            models.Token.token == token,
            models.Token.token_type == token_type
        ).first()
        if db_token:
            db.delete(db_token)
            db.commit()
            logger.debug(f"{token_type.capitalize()} token deleted from DB")
        else:
            logger.warning(f"{token_type.capitalize()} token not found in DB")
        return db_token
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to delete {token_type} token: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete {token_type} token: {str(e)}")

def cleanup_expired_tokens(db: Session):
    try:
        logger.debug("Cleaning up expired tokens")
        tokens = db.query(models.Token).all()
        deleted_count = 0
        for token in tokens:
            try:
                jwt.decode(token.token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
            except JWTError:
                db.delete(token)
                deleted_count += 1
        db.commit()
        logger.debug(f"Deleted {deleted_count} expired tokens")
        return {"message": f"Deleted {deleted_count} expired tokens"}
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to clean up expired tokens: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to clean up expired tokens: {str(e)}")

# -------------------------
# PRODUCT FUNCTIONS
# -------------------------
def get_all_products_with_reviews(db: Session):
    """
    Fetch all products with:
    - total number of reviews
    - average rating
    - price and stock info (XS/S/M/L/XL/XXL, kids)
    """
    results = (
        db.query(
            models.Product.id,
            models.Product.name,
            models.Product.image,
            models.Product.images,
            models.Product.collection,
            func.count(models.Review.id).label("total_reviews"),
            func.coalesce(func.avg(models.Review.stars), 0).label("average_rating"),
            models.Product.XS_price,
            models.Product.S_price,
            models.Product.M_price,
            models.Product.L_price,
            models.Product.XL_price,
            models.Product.XXL_price,
            models.Product.XS_stock,
            models.Product.S_stock,
            models.Product.M_stock,
            models.Product.L_stock,
            models.Product.XL_stock,
            models.Product.XXL_stock,
            models.Product.kids,
        )
        .outerjoin(models.Review, models.Product.id == models.Review.product_id)
        .group_by(models.Product.id)
        .all()
    )

    products = []
    for r in results:
        products.append(
            schemas.ProductResponse(
                id=r.id,
                name=r.name,
                image=r.image,
                images=r.images,
                collection=r.collection,
                total_reviews=r.total_reviews,
                average_rating=round(float(r.average_rating or 0), 2),
                XS_price=r.XS_price,
                S_price=r.S_price,
                M_price=r.M_price,
                L_price=r.L_price,
                XL_price=r.XL_price,
                XXL_price=r.XXL_price,
                XS_stock=r.XS_stock,
                S_stock=r.S_stock,
                M_stock=r.M_stock,
                L_stock=r.L_stock,
                XL_stock=r.XL_stock,
                XXL_stock=r.XXL_stock,
                kids=r.kids,
            )
        )
    return products

# -------------------------
# REVIEW FUNCTIONS
# -------------------------
def get_reviews_by_product(db: Session, product_id: str):
    """
    Fetch all reviews for a specific product, including username, stars, text, and time.
    """
    results = (
        db.query(
            models.User.username,
            models.Review.stars,
            models.Review.text,
            models.Review.time,
        )
        .join(models.Review, models.User.id == models.Review.user_id)
        .filter(models.Review.product_id == product_id)
        .order_by(models.Review.time.desc())
        .all()
    )

    return [
        schemas.ReviewDetail(
            username=r.username,
            stars=r.stars,
            text=r.text,
            time=r.time,
        )
        for r in results
    ]

# -------------------------
# GET ALL PRODUCTS IN USER CART
# -------------------------
def get_user_cart(db: Session, user_id: int):
    """
    Returns all products in a user's cart with product name, collection,
    size, quantity, image, user_id, product_id, product price, and total number of distinct products.
    """
    results = (
        db.query(
            models.Product.name.label("product_name"),
            models.Product.collection.label("collection"),
            models.Cart.size.label("size"),
            models.Cart.quantity.label("quantity"),
            models.Product.image.label("image"),
            models.Cart.user_id.label("user_id"),
            models.Cart.product_id.label("product_id"),
            models.Product.XS_price,
            models.Product.S_price,
            models.Product.M_price,
            models.Product.L_price,
            models.Product.XL_price,
            models.Product.XXL_price,
        )
        .join(models.Cart, models.Product.id == models.Cart.product_id)
        .filter(models.Cart.user_id == user_id)
        .all()
    )

    items = []
    for r in results:
        price = (
            r.XS_price if r.size == "XS" else
            r.S_price if r.size == "S" else
            r.M_price if r.size == "M" else
            r.L_price if r.size == "L" else
            r.XL_price if r.size == "XL" else
            r.XXL_price
        )
        items.append(
            schemas.CartProduct(
                product_name=r.product_name,
                collection=r.collection,
                size=r.size,
                quantity=r.quantity,
                image=r.image,
                user_id=r.user_id,
                product_id=r.product_id,
                price=price,
            )
        )

    return schemas.CartResponse(
        total_products=len(items),
        items=items
    )

# -------------------------
# GET ALL ORDERS
# -------------------------
def get_all_orders(db: Session):
    """
    Fetch all orders with associated products, username, and total price.
    """
    results = (
        db.query(models.Order)
        .join(models.User, models.Order.user_id == models.User.id)
        .all()
    )

    orders = []
    for order in results:
        items = (
            db.query(
                models.OrderItem.quantity,
                models.OrderItem.size,
                models.OrderItem.product_id,
                models.Product.name.label("product_name"),
                models.Product.XS_price,
                models.Product.S_price,
                models.Product.M_price,
                models.Product.L_price,
                models.Product.XL_price,
                models.Product.XXL_price,
            )
            .join(models.Product, models.OrderItem.product_id == models.Product.id)
            .filter(models.OrderItem.order_id == order.id)
            .all()
        )

        order_products = []
        total_price = 0
        for item in items:
            price = (
                item.XS_price if item.size == "XS" else
                item.S_price if item.size == "S" else
                item.M_price if item.size == "M" else
                item.L_price if item.size == "L" else
                item.XL_price if item.size == "XL" else
                item.XXL_price
            )
            total_price += price * item.quantity
            order_products.append(
                schemas.OrderProduct(
                    product_name=item.product_name,
                    quantity=item.quantity,
                    size=item.size,
                    product_id=item.product_id,
                    price=price,
                )
            )

        orders.append(
            schemas.OrderResponse(
                order_id=order.id,
                user_id=order.user_id,
                username=order.user.username,
                status=order.status,
                total_products=len(items),
                total_price=total_price,
                products=order_products,
                order_time=order.time,
            )
        )
    return orders

# -------------------------
# GET USER ORDERS
# -------------------------
def get_user_orders(db: Session, user_id: int):
    """
    Fetch all orders for a specific user with associated products, username, and total price.
    """
    results = (
        db.query(models.Order)
        .join(models.User, models.Order.user_id == models.User.id)
        .filter(models.Order.user_id == user_id)
        .all()
    )

    orders = []
    for order in results:
        items = (
            db.query(
                models.OrderItem.quantity,
                models.OrderItem.size,
                models.OrderItem.product_id,
                models.Product.name.label("product_name"),
                models.Product.XS_price,
                models.Product.S_price,
                models.Product.M_price,
                models.Product.L_price,
                models.Product.XL_price,
                models.Product.XXL_price,
            )
            .join(models.Product, models.OrderItem.product_id == models.Product.id)
            .filter(models.OrderItem.order_id == order.id)
            .all()
        )

        order_products = []
        total_price = 0
        for item in items:
            price = (
                item.XS_price if item.size == "XS" else
                item.S_price if item.size == "S" else
                item.M_price if item.size == "M" else
                item.L_price if item.size == "L" else
                item.XL_price if item.size == "XL" else
                item.XXL_price
            )
            total_price += price * item.quantity
            order_products.append(
                schemas.OrderProduct(
                    product_name=item.product_name,
                    quantity=item.quantity,
                    size=item.size,
                    product_id=item.product_id,
                    price=price,
                )
            )

        orders.append(
            schemas.OrderResponse(
                order_id=order.id,
                user_id=order.user_id,
                username=order.user.username,
                status=order.status,
                total_products=len(items),
                total_price=total_price,
                products=order_products,
                order_time=order.time,
            )
        )
    return orders

# -------------------------
# UPDATE ORDER STATUS
# -------------------------
def update_order_status(db: Session, order_id: int, status: str):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order:
        order.status = status
        db.commit()
        db.refresh(order)
    return order

# -------------------------
# GET ORDER
# -------------------------
def get_order(db: Session, order_id: int):
    order = (
        db.query(models.Order)
        .join(models.User, models.Order.user_id == models.User.id)
        .filter(models.Order.id == order_id)
        .first()
    )
    if not order:
        return None

    items = (
        db.query(
            models.OrderItem.quantity,
            models.OrderItem.size,
            models.OrderItem.product_id,
            models.Product.name.label("product_name"),
            models.Product.XS_price,
            models.Product.S_price,
            models.Product.M_price,
            models.Product.L_price,
            models.Product.XL_price,
            models.Product.XXL_price,
        )
        .join(models.Product, models.OrderItem.product_id == models.Product.id)
        .filter(models.OrderItem.order_id == order.id)
        .all()
    )

    order_products = []
    total_price = 0
    for item in items:
        price = (
            item.XS_price if item.size == "XS" else
            item.S_price if item.size == "S" else
            item.M_price if item.size == "M" else
            item.L_price if item.size == "L" else
            item.XL_price if item.size == "XL" else
            item.XXL_price
        )
        total_price += price * item.quantity
        order_products.append(
            schemas.OrderProduct(
                product_name=item.product_name,
                quantity=item.quantity,
                size=item.size,
                product_id=item.product_id,
                price=price,
            )
        )

    return schemas.OrderResponse(
        order_id=order.id,
        user_id=order.user_id,
        username=order.user.username,
        status=order.status,
        total_products=len(items),
        total_price=total_price,
        products=order_products,
        order_time=order.time,
    )

# -------------------------
# CREATE REVIEW
# -------------------------
def create_review(db: Session, review: schemas.ReviewCreate):
    product = db.query(models.Product).filter(models.Product.id == review.product_id).first()
    if not product:
        return None
    user = db.query(models.User).filter(models.User.id == review.user_id).first()
    if not user:
        return None
    db_review = models.Review(
        stars=review.stars,
        text=review.text,
        time=date.fromisoformat(review.time),
        user_id=review.user_id,
        product_id=review.product_id
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

# -------------------------
# GET REVIEW DETAIL
# -------------------------
def get_review_detail(db: Session, review_id: int):
    result = (
        db.query(
            models.User.username,
            models.Review.stars,
            models.Review.text,
            models.Review.time,
        )
        .join(models.Review, models.User.id == models.Review.user_id)
        .filter(models.Review.id == review_id)
        .first()
    )
    if not result:
        return None
    return schemas.ReviewDetail(
        username=result.username,
        stars=result.stars,
        text=result.text,
        time=result.time,
    )

# -------------------------
# UPDATE CART QUANTITY
# -------------------------
def update_cart_quantity(db: Session, user_id: int, product_id: str, size: str, quantity: int):
    cart_item = db.query(models.Cart).filter(
        models.Cart.user_id == user_id,
        models.Cart.product_id == product_id,
        models.Cart.size == size
    ).first()
    if not cart_item:
        return None
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        return None

    # Calculate delta for stock deduction (only deduct if quantity is increasing)
    quantity_delta = quantity - cart_item.quantity
    if quantity_delta > 0:
        # Verify stock for the additional quantity
        if size == "XS" and product.XS_stock < quantity_delta:
            raise HTTPException(status_code=400, detail="Insufficient XS stock")
        elif size == "S" and product.S_stock < quantity_delta:
            raise HTTPException(status_code=400, detail="Insufficient S stock")
        elif size == "M" and product.M_stock < quantity_delta:
            raise HTTPException(status_code=400, detail="Insufficient M stock")
        elif size == "L" and product.L_stock < quantity_delta:
            raise HTTPException(status_code=400, detail="Insufficient L stock")
        elif size == "XL" and product.XL_stock < quantity_delta:
            raise HTTPException(status_code=400, detail="Insufficient XL stock")
        elif size == "XXL" and product.XXL_stock < quantity_delta:
            raise HTTPException(status_code=400, detail="Insufficient XXL stock")

        # Deduct stock
        if size == "XS":
            product.XS_stock -= quantity_delta
        elif size == "S":
            product.S_stock -= quantity_delta
        elif size == "M":
            product.M_stock -= quantity_delta
        elif size == "L":
            product.L_stock -= quantity_delta
        elif size == "XL":
            product.XL_stock -= quantity_delta
        elif size == "XXL":
            product.XXL_stock -= quantity_delta
    elif quantity_delta < 0:
        # Add back to stock
        if size == "XS":
            product.XS_stock += abs(quantity_delta)
        elif size == "S":
            product.S_stock += abs(quantity_delta)
        elif size == "M":
            product.M_stock += abs(quantity_delta)
        elif size == "L":
            product.L_stock += abs(quantity_delta)
        elif size == "XL":
            product.XL_stock += abs(quantity_delta)
        elif size == "XXL":
            product.XXL_stock += abs(quantity_delta)

    # Update quantity
    cart_item.quantity = quantity
    db.commit()
    db.refresh(cart_item)
    db.refresh(product)
    return cart_item

# -------------------------
# REMOVE FROM CART
# -------------------------
def remove_from_cart(db: Session, user_id: int, product_id: str, size: str):
    cart_item = db.query(models.Cart).filter(
        models.Cart.user_id == user_id,
        models.Cart.product_id == product_id,
        models.Cart.size == size
    ).first()
    if not cart_item:
        return None
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        return None

    # Add stock back
    if size == "XS":
        product.XS_stock += cart_item.quantity
    elif size == "S":
        product.S_stock += cart_item.quantity
    elif size == "M":
        product.M_stock += cart_item.quantity
    elif size == "L":
        product.L_stock += cart_item.quantity
    elif size == "XL":
        product.XL_stock += cart_item.quantity
    elif size == "XXL":
        product.XXL_stock += cart_item.quantity

    db.delete(cart_item)
    db.commit()
    db.refresh(product)
    return True

# -------------------------
# ADD TO CART
# -------------------------
def add_to_cart(db: Session, cart_item: schemas.CartCreate):
    product = db.query(models.Product).filter(models.Product.id == cart_item.product_id).first()
    if not product:
        return None

    # Check if the item already exists in the cart
    existing_cart_item = db.query(models.Cart).filter(
        models.Cart.user_id == cart_item.user_id,
        models.Cart.product_id == cart_item.product_id,
        models.Cart.size == cart_item.size
    ).first()

    if existing_cart_item:
        # Calculate delta for stock deduction (only deduct if quantity is increasing)
        quantity_delta = cart_item.quantity - existing_cart_item.quantity
        if quantity_delta > 0:
            # Verify stock for the additional quantity
            if cart_item.size == "XS" and product.XS_stock < quantity_delta:
                raise HTTPException(status_code=400, detail="Insufficient XS stock")
            elif cart_item.size == "S" and product.S_stock < quantity_delta:
                raise HTTPException(status_code=400, detail="Insufficient S stock")
            elif cart_item.size == "M" and product.M_stock < quantity_delta:
                raise HTTPException(status_code=400, detail="Insufficient M stock")
            elif cart_item.size == "L" and product.L_stock < quantity_delta:
                raise HTTPException(status_code=400, detail="Insufficient L stock")
            elif cart_item.size == "XL" and product.XL_stock < quantity_delta:
                raise HTTPException(status_code=400, detail="Insufficient XL stock")
            elif cart_item.size == "XXL" and product.XXL_stock < quantity_delta:
                raise HTTPException(status_code=400, detail="Insufficient XXL stock")

            # Deduct stock
            if cart_item.size == "XS":
                product.XS_stock -= quantity_delta
            elif cart_item.size == "S":
                product.S_stock -= quantity_delta
            elif cart_item.size == "M":
                product.M_stock -= quantity_delta
            elif cart_item.size == "L":
                product.L_stock -= quantity_delta
            elif cart_item.size == "XL":
                product.XL_stock -= quantity_delta
            elif cart_item.size == "XXL":
                product.XXL_stock -= quantity_delta
        elif quantity_delta < 0:
            # Add back to stock
            if cart_item.size == "XS":
                product.XS_stock += abs(quantity_delta)
            elif cart_item.size == "S":
                product.S_stock += abs(quantity_delta)
            elif cart_item.size == "M":
                product.M_stock += abs(quantity_delta)
            elif cart_item.size == "L":
                product.L_stock += abs(quantity_delta)
            elif cart_item.size == "XL":
                product.XL_stock += abs(quantity_delta)
            elif cart_item.size == "XXL":
                product.XXL_stock += abs(quantity_delta)

        # Update quantity
        existing_cart_item.quantity = cart_item.quantity
        db.commit()
        db.refresh(existing_cart_item)
        db.refresh(product)
        return existing_cart_item

    # For new item: Verify and deduct full stock
    if cart_item.size == "XS" and product.XS_stock < cart_item.quantity:
        raise HTTPException(status_code=400, detail="Insufficient XS stock")
    elif cart_item.size == "S" and product.S_stock < cart_item.quantity:
        raise HTTPException(status_code=400, detail="Insufficient S stock")
    elif cart_item.size == "M" and product.M_stock < cart_item.quantity:
        raise HTTPException(status_code=400, detail="Insufficient M stock")
    elif cart_item.size == "L" and product.L_stock < cart_item.quantity:
        raise HTTPException(status_code=400, detail="Insufficient L stock")
    elif cart_item.size == "XL" and product.XL_stock < cart_item.quantity:
        raise HTTPException(status_code=400, detail="Insufficient XL stock")
    elif cart_item.size == "XXL" and product.XXL_stock < cart_item.quantity:
        raise HTTPException(status_code=400, detail="Insufficient XXL stock")

    # Deduct stock
    if cart_item.size == "XS":
        product.XS_stock -= cart_item.quantity
    elif cart_item.size == "S":
        product.S_stock -= cart_item.quantity
    elif cart_item.size == "M":
        product.M_stock -= cart_item.quantity
    elif cart_item.size == "L":
        product.L_stock -= cart_item.quantity
    elif cart_item.size == "XL":
        product.XL_stock -= cart_item.quantity
    elif cart_item.size == "XXL":
        product.XXL_stock -= cart_item.quantity

    # Create new cart item
    db_cart_item = models.Cart(
        user_id=cart_item.user_id,
        product_id=cart_item.product_id,
        size=cart_item.size,
        quantity=cart_item.quantity
    )
    db.add(db_cart_item)
    db.commit()
    db.refresh(db_cart_item)
    db.refresh(product)
    return db_cart_item

# -------------------------
# CREATE ORDER FROM CART
# -------------------------
def create_order_from_cart(db: Session, order: schemas.OrderCreate):
    """
    Create a new order for a user using all items in their cart and clear the cart.
    Returns the updated list of user orders.
    """
    # Validate user existence
    user = db.query(models.User).filter(models.User.id == order.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch cart items
    cart_items = db.query(models.Cart).filter(models.Cart.user_id == order.user_id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # Validate products
    for item in cart_items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")

    # Create new order
    db_order = models.Order(
        user_id=order.user_id,
        status="pending",
        time=date.fromisoformat(order.order_time)
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Add order items from cart
    for item in cart_items:
        db_item = models.OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            size=item.size,
            quantity=item.quantity
        )
        db.add(db_item)
        db.commit()

    # Clear user's cart
    db.query(models.Cart).filter(models.Cart.user_id == order.user_id).delete()
    db.commit()

    # Return all user orders
    return get_user_orders(db, order.user_id)

# -------------------------
# CHECK IF USER REVIEWED PRODUCT
# -------------------------
def has_user_reviewed_product(db: Session, user_id: int, product_id: str):
    """
    Check if a user has already submitted a review for a product.
    Returns True if a review exists, False otherwise.
    """
    review = db.query(models.Review).filter(
        models.Review.user_id == user_id,
        models.Review.product_id == product_id
    ).first()
    return review is not None
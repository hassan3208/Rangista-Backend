from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas
from models import User, Order, Product
from passlib.context import CryptContext
from datetime import date
from typing import Optional
from fastapi import HTTPException

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
# PRODUCT FUNCTIONS
# -------------------------
def get_all_products_with_reviews(db: Session):
    """
    Fetch all products with:
    - total number of reviews
    - average rating
    - price and stock info (S/M/L, kids)
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
            models.PriceAndStock.S_price,
            models.PriceAndStock.M_price,
            models.PriceAndStock.L_price,
            models.PriceAndStock.S_stock,
            models.PriceAndStock.M_stock,
            models.PriceAndStock.L_stock,
            models.PriceAndStock.kids,
        )
        .outerjoin(models.Review, models.Product.id == models.Review.product_id)
        .outerjoin(models.PriceAndStock, models.Product.id == models.PriceAndStock.product_id)
        .group_by(models.Product.id)
        .group_by(models.PriceAndStock.id)
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
                S_price=r.S_price,
                M_price=r.M_price,
                L_price=r.L_price,
                S_stock=r.S_stock,
                M_stock=r.M_stock,
                L_stock=r.L_stock,
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
        .order_by(models.Review.time.desc())  # Latest first
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
            models.PriceAndStock.S_price,
            models.PriceAndStock.M_price,
            models.PriceAndStock.L_price,
        )
        .join(models.Cart, models.Product.id == models.Cart.product_id)
        .join(models.PriceAndStock, models.Product.id == models.PriceAndStock.product_id)
        .filter(models.Cart.user_id == user_id)
        .all()
    )

    items = [
        schemas.CartProduct(
            product_name=r.product_name,
            collection=r.collection,
            size=r.size,
            quantity=r.quantity,
            image=r.image,
            user_id=r.user_id,
            product_id=r.product_id,
            price=(r.S_price if r.size == "S" else r.M_price if r.size == "M" else r.L_price) * r.quantity,
        )
        for r in results
    ]

    total_products = len(items)
    return schemas.CartResponse(total_products=total_products, items=items)






# ------------------------- 
# GET ALL ORDERS OF ALL USER 
# ------------------------- 
def get_all_orders(db: Session):
    """
    Fetch all orders from all users with product details.
    Each order contains:
    - order_id
    - user_id
    - username
    - status
    - total_products
    - total_price
    - products: list of {product_name, quantity, size, product_id, price}
    - order_time
    """
    orders = db.query(models.Order).all()
    order_responses = []

    for order in orders:
        username = order.user.username
        products_list = []
        total_price = 0
        for item in order.items:
            price_stock = db.query(models.PriceAndStock).filter(models.PriceAndStock.product_id == item.product_id).first()
            if price_stock:
                price = (
                    price_stock.S_price if item.size == "S" else
                    price_stock.M_price if item.size == "M" else
                    price_stock.L_price
                )
                products_list.append(schemas.OrderProduct(
                    product_name=item.product.name,
                    quantity=item.quantity,
                    size=item.size,
                    product_id=item.product_id,
                    price=price * item.quantity
                ))
                total_price += price * item.quantity
        total_products = sum(item.quantity for item in order.items)
        order_responses.append(
            schemas.OrderResponse(
                order_id=order.id,
                user_id=order.user_id,  # Added user_id
                username=username,
                status=order.status,
                total_products=total_products,
                total_price=total_price,  # Added total_price
                products=products_list,
                order_time=order.time
            )
        )
    return order_responses

# -------------------------
# GET ALL ORDERS OF A SPECIFIC USER
# -------------------------
def get_user_orders(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return []
    orders_list = []
    orders = db.query(Order).filter(Order.user_id == user_id).order_by(Order.time.desc(), Order.id.desc()).all()
    for order in orders:
        products = []
        total_products = 0
        total_price = 0
        for item in order.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            price_stock = db.query(models.PriceAndStock).filter(models.PriceAndStock.product_id == item.product_id).first()
            if product and price_stock:
                price = (
                    price_stock.S_price if item.size == "S" else
                    price_stock.M_price if item.size == "M" else
                    price_stock.L_price
                )
                products.append(schemas.OrderProduct(
                    product_name=product.name,
                    quantity=item.quantity,
                    size=item.size,
                    product_id=item.product_id,
                    price=price * item.quantity
                ))
                total_products += item.quantity
                total_price += price * item.quantity
        orders_list.append(schemas.OrderResponse(
            order_id=order.id,
            user_id=user.id,
            username=user.username,
            status=order.status,
            total_products=total_products,
            total_price=total_price,
            products=products,
            order_time=order.time
        ))
    return orders_list

# ------------------------- 
# GET ORDER 
# ------------------------- 
def get_order(db: Session, order_id: int):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        return None
    username = order.user.username
    products_list = []
    total_price = 0
    for item in order.items:
        price_stock = db.query(models.PriceAndStock).filter(models.PriceAndStock.product_id == item.product_id).first()
        if price_stock:
            price = (
                price_stock.S_price if item.size == "S" else
                price_stock.M_price if item.size == "M" else
                price_stock.L_price
            )
            products_list.append(schemas.OrderProduct(
                product_name=item.product.name,
                quantity=item.quantity,
                size=item.size,
                product_id=item.product_id,
                price=price * item.quantity
            ))
            total_price += price * item.quantity
    total_products = sum(item.quantity for item in order.items)
    return schemas.OrderResponse(
        order_id=order.id,
        user_id=order.user_id,
        username=username,
        status=order.status,
        total_products=total_products,
        total_price=total_price,
        products=products_list,
        order_time=order.time
    )

# -------------------------
# NEW CRUD FUNCTIONS
# -------------------------
def update_order_status(db: Session, order_id: int, status: str):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        return None
    order.status = status
    db.commit()
    db.refresh(order)
    return order

# ------------------------- 
# GET ORDER 
# ------------------------- 
def get_order(db: Session, order_id: int):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        return None
    username = order.user.username
    products_list = []
    total_price = 0
    for item in order.items:
        price_stock = db.query(models.PriceAndStock).filter(models.PriceAndStock.product_id == item.product_id).first()
        if price_stock:
            price = (
                price_stock.S_price if item.size == "S" else
                price_stock.M_price if item.size == "M" else
                price_stock.L_price
            )
            products_list.append(schemas.OrderProduct(
                product_name=item.product.name,
                quantity=item.quantity,
                size=item.size,
                product_id=item.product_id,
                price=price * item.quantity
            ))
            total_price += price * item.quantity
    total_products = sum(item.quantity for item in order.items)
    return schemas.OrderResponse(
        order_id=order.id,
        user_id=order.user_id,
        username=username,
        status=order.status,
        total_products=total_products,
        total_price=total_price,
        products=products_list,
        order_time=order.time
    )
    

# -------------------------
# CREATE REVIEW
# -------------------------

def create_review(db: Session, review: schemas.ReviewCreate):
    try:
        review_time = date.fromisoformat(review.time)
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD.")
    db_review = models.Review(
        stars=review.stars,
        text=review.text,
        time=review_time,
        user_id=review.user_id,
        product_id=review.product_id,
    )
    print("Creating review:", db_review)
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

    # Get the price and stock record
    price_stock = db.query(models.PriceAndStock).filter(
        models.PriceAndStock.product_id == product_id
    ).first()
    if not price_stock:
        return None

    # Calculate the quantity delta (new quantity - old quantity)
    quantity_delta = quantity - cart_item.quantity

    # Update stock based on size and quantity delta
    if quantity_delta > 0:
        # Adding quantity, check if enough stock is available
        if size == "S" and price_stock.S_stock >= quantity_delta:
            price_stock.S_stock -= quantity_delta
        elif size == "M" and price_stock.M_stock >= quantity_delta:
            price_stock.M_stock -= quantity_delta
        elif size == "L" and price_stock.L_stock >= quantity_delta:
            price_stock.L_stock -= quantity_delta
        else:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for additional quantity in size {size}")
    elif quantity_delta < 0:
        # Reducing quantity, add back to stock
        if size == "S":
            price_stock.S_stock += abs(quantity_delta)
        elif size == "M":
            price_stock.M_stock += abs(quantity_delta)
        elif size == "L":
            price_stock.L_stock += abs(quantity_delta)

    # Update cart item quantity
    cart_item.quantity = quantity
    db.commit()
    db.refresh(cart_item)
    db.refresh(price_stock)
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

    # Get the price and stock record to update stock
    price_stock = db.query(models.PriceAndStock).filter(
        models.PriceAndStock.product_id == product_id
    ).first()
    if not price_stock:
        # Even if not found, still remove from cart
        db.delete(cart_item)
        db.commit()
        return True

    # Add back the quantity to the appropriate size stock
    if size == "S":
        price_stock.S_stock += cart_item.quantity
    elif size == "M":
        price_stock.M_stock += cart_item.quantity
    elif size == "L":
        price_stock.L_stock += cart_item.quantity

    # Delete the cart item
    db.delete(cart_item)
    db.commit()
    db.refresh(price_stock)
    return True



# -------------------------
# ADD TO CART
# -------------------------

def add_to_cart(db: Session, cart_item: schemas.CartCreate):
    """
    Add a new item to the cart or update quantity if it already exists, and reduce stock only for net increases.
    """
    # Validate user and product existence
    user = db.query(models.User).filter(models.User.id == cart_item.user_id).first()
    if not user:
        return None
    product = db.query(models.Product).filter(models.Product.id == cart_item.product_id).first()
    if not product:
        return None

    # Get stock
    price_stock = db.query(models.PriceAndStock).filter(models.PriceAndStock.product_id == cart_item.product_id).first()
    if not price_stock:
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
            if cart_item.size == "S" and price_stock.S_stock >= quantity_delta:
                price_stock.S_stock -= quantity_delta
            elif cart_item.size == "M" and price_stock.M_stock >= quantity_delta:
                price_stock.M_stock -= quantity_delta
            elif cart_item.size == "L" and price_stock.L_stock >= quantity_delta:
                price_stock.L_stock -= quantity_delta
            else:
                raise HTTPException(status_code=400, detail=f"Insufficient stock for additional quantity in size {cart_item.size}")
        elif quantity_delta < 0:
            # If decreasing quantity, add back to stock (optional, but consistent)
            if cart_item.size == "S":
                price_stock.S_stock += abs(quantity_delta)
            elif cart_item.size == "M":
                price_stock.M_stock += abs(quantity_delta)
            elif cart_item.size == "L":
                price_stock.L_stock += abs(quantity_delta)

        # Update quantity (set to provided value)
        existing_cart_item.quantity = cart_item.quantity
        db.commit()
        db.refresh(existing_cart_item)
        db.refresh(price_stock)
        return existing_cart_item

    # For new item: Verify and deduct full stock
    if cart_item.size == "S" and price_stock.S_stock >= cart_item.quantity:
        price_stock.S_stock -= cart_item.quantity
    elif cart_item.size == "M" and price_stock.M_stock >= cart_item.quantity:
        price_stock.M_stock -= cart_item.quantity
    elif cart_item.size == "L" and price_stock.L_stock >= cart_item.quantity:
        price_stock.L_stock -= cart_item.quantity
    else:
        raise HTTPException(status_code=400, detail=f"Insufficient stock for size {cart_item.size}")

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
    db.refresh(price_stock)
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
        price_stock = db.query(models.PriceAndStock).filter(models.PriceAndStock.product_id == item.product_id).first()
        if not price_stock:
            raise HTTPException(status_code=400, detail=f"No stock data for product {item.product_id}")

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
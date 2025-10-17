from jose import JWTError, jwt
from fastapi import FastAPI, Depends, HTTPException, status, Form, Query, Response, Cookie
from sqlalchemy.orm import Session
from typing import Annotated, List, Optional 
from datetime import timedelta
from fastapi.middleware.cors import CORSMiddleware
import models, schemas, crud, auth, database
import os
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

models.Base.metadata.create_all(bind=database.engine)

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    os.getenv("FRONTEND_URL", "https://rangista.vercel.app"),
]

app = FastAPI(title='User Management API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Signup
@app.post("/signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(auth.get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_email = crud.get_user_by_email(db, user.email)
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)

# Signin (login)
@app.post("/signin", response_model=schemas.Token)
async def signin(
    response: Response,
    form_data: Annotated[auth.OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(auth.get_db),
):
    logger.debug(f"Signin attempt for username: {form_data.username}")
    user = await auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.error("Authentication failed: Incorrect login credentials")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=30)  # Refresh token lasts 30 days
    access_token = auth.create_access_token(
        data={"sub": user.username, "type": "access"},
        expires_delta=access_token_expires
    )
    refresh_token = auth.create_access_token(
        data={"sub": user.username, "type": "refresh"},
        expires_delta=refresh_token_expires
    )
    # Store both tokens in DB
    db_token = crud.create_token(db, user.id, access_token, "access")
    if not db_token:
        logger.error("Failed to store access token in database")
        raise HTTPException(status_code=500, detail="Failed to store access token in database")
    db_refresh_token = crud.create_token(db, user.id, refresh_token, "refresh")
    if not db_refresh_token:
        logger.error("Failed to store refresh token in database")
        raise HTTPException(status_code=500, detail="Failed to store refresh token in database")
    logger.debug(f"Tokens created for user_id: {user.id}, access: {access_token[:10]}..., refresh: {refresh_token[:10]}...")
    # Set HTTP-only cookies
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # Set to True in production
        samesite="lax",
        max_age=int(access_token_expires.total_seconds())
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,  # Set to True in production
        samesite="lax",
        max_age=int(refresh_token_expires.total_seconds())
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Refresh token
@app.post("/refresh", response_model=schemas.Token)
async def refresh_token(
    response: Response,
    refresh_token: Optional[str] = Cookie(None),
    db: Session = Depends(auth.get_db)
):
    logger.debug("Refresh token attempt")
    if not refresh_token:
        logger.error("No refresh token provided")
        raise HTTPException(status_code=401, detail="No refresh token provided")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        username = payload.get("sub")
        token_type = payload.get("type")
        if username is None or token_type != "refresh":
            logger.error("Invalid refresh token payload")
            raise credentials_exception
    except JWTError as e:
        logger.error(f"Refresh token validation failed: {str(e)}")
        raise credentials_exception
    user = crud.get_user_by_username(db, username)
    if not user:
        logger.error("User not found for refresh token")
        raise credentials_exception
    # Verify refresh token exists in DB
    db_token = crud.get_token(db, refresh_token, "refresh")
    if not db_token:
        logger.error("Refresh token not found in database")
        raise credentials_exception
    # Generate new access token
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username, "type": "access"},
        expires_delta=access_token_expires
    )
    # Store new access token
    db_access_token = crud.create_token(db, user.id, access_token, "access")
    if not db_access_token:
        logger.error("Failed to store new access token")
        raise HTTPException(status_code=500, detail="Failed to store new access token")
    logger.debug(f"New access token created for user_id: {user.id}, token: {access_token[:10]}...")
    # Set new access token cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # Set to True in production
        samesite="lax",
        max_age=int(access_token_expires.total_seconds())
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Logout
@app.post("/logout")
async def logout(
    response: Response,
    current_user: Annotated[schemas.UserResponse, Depends(auth.get_current_active_user)],
    db: Session = Depends(auth.get_db),
    access_token: Optional[str] = Cookie(None),
    refresh_token: Optional[str] = Cookie(None)
):
    logger.debug(f"Logout attempt for user: {current_user.username}")
    if access_token:
        logger.debug(f"Deleting access token: {access_token[:10]}...")
        crud.delete_token(db, access_token, "access")
    else:
        logger.warning("No access_token cookie found during logout")
    if refresh_token:
        logger.debug(f"Deleting refresh token: {refresh_token[:10]}...")
        crud.delete_token(db, refresh_token, "refresh")
    else:
        logger.warning("No refresh_token cookie found during logout")
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    logger.debug("Logout successful, cookies cleared")
    return {"message": "Logout successful"}

# Check authentication status
@app.get("/check-auth", response_model=schemas.UserResponse)
async def check_auth(current_user: Annotated[schemas.UserResponse, Depends(auth.get_current_active_user)]):
    """
    Check if user is authenticated via cookie token.
    Returns user data if authenticated, else raises 401.
    """
    return current_user

# Get all users
@app.get("/users", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(auth.get_db)):
    users = crud.get_all_users(db)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

# Protected route
@app.get("/users/me", response_model=schemas.UserResponse)
async def read_users_me(
    current_user: Annotated[schemas.UserResponse, Depends(auth.get_current_active_user)]
):
    return current_user

@app.put("/users/me", response_model=schemas.UserResponse)
async def update_my_profile(
    updates: schemas.UserUpdate,
    db: Session = Depends(auth.get_db),
    current_user: schemas.UserResponse = Depends(auth.get_current_active_user)
):
    db_user = crud.get_user_by_username(db, current_user.username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = crud.update_user(db, db_user, updates)
    return updated_user

# -------------------------
# PRODUCTS ROUTE
# -------------------------
@app.get("/products", response_model=list[schemas.ProductResponse])
def read_all_products(db: Session = Depends(auth.get_db)):
    """
    Fetch all products with total number of reviews and average rating.
    """
    products = crud.get_all_products_with_reviews(db)
    return products

# -------------------------
# GET ALL REVIEWS FOR A PRODUCT
# -------------------------
@app.get("/products/{product_id}/reviews", response_model=list[schemas.ReviewDetail])
def get_product_reviews(product_id: str, db: Session = Depends(auth.get_db)):
    reviews = crud.get_reviews_by_product(db, product_id)
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found for this product.")
    return reviews

# -------------------------
# GET USER CART ENDPOINT
# -------------------------
@app.get("/cart/{user_id}", response_model=schemas.CartResponse)
def get_user_cart(user_id: int, db: Session = Depends(auth.get_db)):
    """
    Fetch all products in a user's cart along with:
    - product name
    - collection
    - size
    - quantity
    - image
    - total number of products
    """
    cart_data = crud.get_user_cart(db, user_id)
    if not cart_data.items:
        raise HTTPException(status_code=404, detail="No items found in cart")
    return cart_data

# -------------------------
# GET ALL ORDERS
# -------------------------
@app.get("/orders", response_model=List[schemas.OrderResponse])
def read_all_orders(db: Session = Depends(auth.get_db)):
    orders = crud.get_all_orders(db)
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")
    return orders

# -------------------------
# GET ALL ORDERS OF A USER
# -------------------------
@app.get("/users/{user_id}/orders", response_model=List[schemas.OrderResponse])
def read_user_orders(user_id: int, db: Session = Depends(auth.get_db)):
    orders = crud.get_user_orders(db, user_id)
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")
    return orders

# -------------------------
# UPDATE ORDER STATUS
# -------------------------
@app.put("/orders/{order_id}/status", response_model=schemas.OrderResponse)
def update_order_status(order_id: int, update: schemas.OrderUpdate, db: Session = Depends(auth.get_db)):
    order = crud.update_order_status(db, order_id, update.status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return crud.get_order(db, order_id)

# -------------------------
# CREATE REVIEW
# -------------------------
@app.post("/reviews/", response_model=schemas.ReviewDetail)
def create_product_review(review: schemas.ReviewCreate, db: Session = Depends(auth.get_db)):
    db_review = crud.create_review(db, review)
    if not db_review:
        raise HTTPException(status_code=400, detail="Could not create review")
    return crud.get_review_detail(db, db_review.id)

# -------------------------
# UPDATE CART QUANTITY
# -------------------------
@app.put("/cart/{user_id}/{product_id}", response_model=schemas.CartResponse)
def update_cart_quantity(user_id: int, product_id: str, cart_update: schemas.CartUpdate, db: Session = Depends(auth.get_db)):
    updated = crud.update_cart_quantity(db, user_id, product_id, cart_update.size, cart_update.quantity)
    if not updated:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return crud.get_user_cart(db, user_id)

# -------------------------
# REMOVE FROM CART
# -------------------------
@app.delete("/cart/{user_id}/{product_id}", response_model=schemas.CartResponse)
def remove_from_cart(user_id: int, product_id: str, size: str = Query(...), db: Session = Depends(auth.get_db)):
    removed = crud.remove_from_cart(db, user_id, product_id, size)
    if not removed:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return crud.get_user_cart(db, user_id)

# -------------------------
# ADD TO CART
# -------------------------
@app.post("/cart/", response_model=schemas.CartResponse)
def add_to_cart(cart_item: schemas.CartCreate, db: Session = Depends(auth.get_db)):
    """
    Add a product to the user's cart with user_id, product_id, size, and quantity (default=1).
    Returns the updated cart.
    """
    added = crud.add_to_cart(db, cart_item)
    if not added:
        raise HTTPException(status_code=400, detail="Could not add item to cart")
    return crud.get_user_cart(db, cart_item.user_id)

# -------------------------
# CREATE ORDER FROM CART
# -------------------------
@app.post("/orders/from-cart/", response_model=List[schemas.OrderResponse])
def create_order_from_cart(order: schemas.OrderCreate, db: Session = Depends(auth.get_db)):
    """
    Create a new order for a user using all items in their cart.
    Clears the cart after order creation and returns the user's updated list of orders.
    """
    orders = crud.create_order_from_cart(db, order)
    if not orders:
        raise HTTPException(status_code=400, detail="Could not create order")
    return orders

@app.get("/reviews/check")
def check_review(
    user_id: int = Query(...),
    order_id: int = Query(...),
    product_id: str = Query(...),
    size: Optional[str] = Query(None),
    db: Session = Depends(auth.get_db)
):
    """
    Check if a user has reviewed a specific product (ignores order_id and size as reviews are per product).
    Returns {'reviewed': True/False}.
    """
    reviewed = crud.has_user_reviewed_product(db, user_id, product_id)
    return {"reviewed": reviewed}

@app.get("/")
def read_root():
    return {"message": "Server is running!"}
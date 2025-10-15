# from pydantic import BaseModel, EmailStr
# from typing import Optional, List
# from datetime import date

# # -------------------------
# # USER SCHEMAS
# # -------------------------
# class UserBase(BaseModel):
#     name: Optional[str] = None
#     username: str
#     email: EmailStr
#     contact_number: str 
#     permanent_address: str 
#     country: str 
#     city: str 
#     contact_number_2: Optional[str] = None

# class UserCreate(UserBase):
#     password: str

# class UserResponse(UserBase):
#     id: int
#     disabled: bool

#     class Config:
#         from_attributes = True

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class TokenData(BaseModel):
#     username: Optional[str] = None

# class UserUpdate(BaseModel):
#     email: Optional[EmailStr] = None
#     full_name: Optional[str] = None
#     disabled: Optional[bool] = None
#     contact_number: Optional[str] = None 
#     permanent_address: Optional[str] = None 
#     country: Optional[str] = None 
#     city: Optional[str] = None 
#     contact_number_2: Optional[str] = None

# # -------------------------
# # PRODUCT & REVIEW SCHEMAS
# # -------------------------
# class ReviewBase(BaseModel):
#     stars: float
#     time: str
#     user_id: int
#     product_id: str

# class ReviewResponse(ReviewBase):
#     id: int

#     class Config:
#         from_attributes = True

# class ProductBase(BaseModel):
#     id: str
#     name: str
#     image: str
#     images: Optional[List[str]] = None
#     collection: str

# class ProductResponse(ProductBase):
#     total_reviews: int
#     average_rating: Optional[float] = 0.0
#     S_price: int
#     M_price: int
#     L_price: int
#     S_stock: float
#     M_stock: float
#     L_stock: float
#     kids: Optional[bool] = None

#     class Config:
#         from_attributes = True

# # -------------------------
# # REVIEW SCHEMAS
# # -------------------------
# class ReviewDetail(BaseModel):
#     username: str
#     stars: float
#     text: Optional[str] = None
#     time: date

#     class Config:
#         from_attributes = True

# # -------------------------
# # CART RESPONSE SCHEMA
# # -------------------------
# class CartProduct(BaseModel):
#     product_name: str
#     collection: str
#     size: str
#     quantity: int
#     image: str
#     user_id: int
#     product_id: str
#     price: int

#     class Config:
#         from_attributes = True

# class CartResponse(BaseModel):
#     total_products: int
#     items: List[CartProduct]

# # -------------------------
# # ORDER RESPONSE SCHEMA
# # -------------------------
# class OrderProduct(BaseModel):
#     product_name: str
#     quantity: int
#     size: str
#     product_id: str
#     price: int  # Added price field

# class OrderResponse(BaseModel):
#     order_id: int
#     user_id: int  # Added user_id field
#     username: str
#     status: str
#     total_products: int
#     total_price: int  # Added total_price field
#     products: List[OrderProduct]
#     order_time: date

#     class Config:
#         from_attributes = True

# # -------------------------
# # NEW SCHEMAS
# # -------------------------
# class ReviewCreate(BaseModel):
#     user_id: int
#     product_id: str
#     stars: float
#     text: Optional[str] = None
#     time: str

# class OrderUpdate(BaseModel):
#     status: str

# class CartUpdate(BaseModel):
#     size: str
#     quantity: int
    
# class CartCreate(BaseModel):
#     user_id: int
#     product_id: str
#     size: str
#     quantity: int = 1

# # -------------------------
# # ORDER CREATE SCHEMA
# # -------------------------
# class OrderCreate(BaseModel):
#     user_id: int
#     order_time: str





from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date

# -------------------------
# USER SCHEMAS
# -------------------------
class UserBase(BaseModel):
    name: Optional[str] = None
    username: str
    email: EmailStr
    contact_number: str 
    permanent_address: str 
    country: str 
    city: str 
    contact_number_2: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    disabled: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    contact_number: Optional[str] = None 
    permanent_address: Optional[str] = None 
    country: Optional[str] = None 
    city: Optional[str] = None 
    contact_number_2: Optional[str] = None

# -------------------------
# PRODUCT & REVIEW SCHEMAS
# -------------------------
class ReviewBase(BaseModel):
    stars: float
    time: str
    user_id: int
    product_id: str

class ReviewResponse(ReviewBase):
    id: int

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    id: str
    name: str
    image: str
    images: Optional[List[str]] = None
    collection: str

class ProductResponse(ProductBase):
    total_reviews: int
    average_rating: Optional[float] = 0.0
    XS_price: int
    S_price: int
    M_price: int
    L_price: int
    XL_price: int
    XXL_price: int
    XS_stock: float
    S_stock: float
    M_stock: float
    L_stock: float
    XL_stock: float
    XXL_stock: float
    kids: Optional[bool] = None

    class Config:
        from_attributes = True

# -------------------------
# REVIEW SCHEMAS
# -------------------------
class ReviewDetail(BaseModel):
    username: str
    stars: float
    text: Optional[str] = None
    time: date

    class Config:
        from_attributes = True

# -------------------------
# CART RESPONSE SCHEMA
# -------------------------
class CartProduct(BaseModel):
    product_name: str
    collection: str
    size: str
    quantity: int
    image: str
    user_id: int
    product_id: str
    price: int

    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    total_products: int
    items: List[CartProduct]

# -------------------------
# ORDER RESPONSE SCHEMA
# -------------------------
class OrderProduct(BaseModel):
    product_name: str
    quantity: int
    size: str
    product_id: str
    price: int  # Added price field

class OrderResponse(BaseModel):
    order_id: int
    user_id: int  # Added user_id field
    username: str
    status: str
    total_products: int
    total_price: int  # Added total_price field
    products: List[OrderProduct]
    order_time: date

    class Config:
        from_attributes = True

# -------------------------
# NEW SCHEMAS
# -------------------------
class ReviewCreate(BaseModel):
    user_id: int
    product_id: str
    stars: float
    text: Optional[str] = None
    time: str

class OrderUpdate(BaseModel):
    status: str

class CartUpdate(BaseModel):
    size: str
    quantity: int
    
class CartCreate(BaseModel):
    user_id: int
    product_id: str
    size: str
    quantity: int = 1

# -------------------------
# ORDER CREATE SCHEMA
# -------------------------
class OrderCreate(BaseModel):
    user_id: int
    order_time: str
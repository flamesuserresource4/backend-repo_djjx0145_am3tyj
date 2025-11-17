"""
Database Schemas for Wishbloom

Each Pydantic model represents a collection in MongoDB. The collection name is the lowercase of the class name.

Collections:
- User
- Event
- Guest
- Gift
- Vendor
- Memory
"""

from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import Optional, List, Literal
from datetime import datetime

# ---------------------------------
# Core Schemas
# ---------------------------------

class User(BaseModel):
    user_id: Optional[str] = Field(None, description="External user id if any")
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    role: Literal["host", "guest", "vendor", "admin"] = Field("host")
    preferences: dict = Field(default_factory=dict, description="User preferences and settings")

class Event(BaseModel):
    event_id: Optional[str] = Field(None, description="External event id if any")
    host_id: str = Field(..., description="User id of the host")
    title: str
    type: Literal["wedding", "birthday", "corporate", "other"] = "other"
    theme: Optional[str] = None
    date: datetime
    location: Optional[str] = None
    description: Optional[str] = None
    invitee_count: Optional[int] = None

class Guest(BaseModel):
    guest_id: Optional[str] = None
    event_id: str
    name: str
    email: Optional[EmailStr] = None
    rsvp_status: Literal["pending", "yes", "no", "maybe"] = "pending"
    contribution: Optional[float] = None

class GiftContributor(BaseModel):
    name: str
    amount: float

class Gift(BaseModel):
    gift_id: Optional[str] = None
    event_id: str
    item_name: str
    price: float
    link: Optional[HttpUrl] = None
    contributor_list: List[GiftContributor] = Field(default_factory=list)

class Vendor(BaseModel):
    vendor_id: Optional[str] = None
    category: Literal["decor", "photography", "catering", "music", "venue", "other"] = "other"
    rating: Optional[float] = Field(None, ge=0, le=5)
    service_details: Optional[str] = None
    kyc_status: Literal["pending", "verified", "rejected"] = "pending"
    name: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    phone: Optional[str] = None

class Memory(BaseModel):
    media_id: Optional[str] = None
    event_id: str
    uploader_id: Optional[str] = None
    media_url: HttpUrl
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Keep file import-friendly: FastAPI can import these types for validation and OpenAPI

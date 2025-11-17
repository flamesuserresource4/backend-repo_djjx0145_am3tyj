import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from database import create_document, get_documents, db
from schemas import User, Event, Guest, Gift, Vendor, Memory

app = FastAPI(title="Wishbloom API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Health & Utility
# -----------------------------

@app.get("/")
def read_root():
    return {"message": "Wishbloom backend is running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = getattr(db, 'name', None) or ("✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set")
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    return response

@app.get("/schema")
def get_schema_summary():
    return {
        "collections": ["user", "event", "guest", "gift", "vendor", "memory"],
        "models": {
            "User": User.model_json_schema(),
            "Event": Event.model_json_schema(),
            "Guest": Guest.model_json_schema(),
            "Gift": Gift.model_json_schema(),
            "Vendor": Vendor.model_json_schema(),
            "Memory": Memory.model_json_schema(),
        }
    }

# -----------------------------
# Users
# -----------------------------

@app.post("/users")
def create_user(user: User):
    try:
        inserted_id = create_document("user", user)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------
# Events
# -----------------------------

@app.post("/events")
def create_event(event: Event):
    try:
        inserted_id = create_document("event", event)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/events")
def list_events(host_id: Optional[str] = Query(None, description="Filter by host_id")):
    try:
        filter_dict = {"host_id": host_id} if host_id else {}
        docs = get_documents("event", filter_dict, limit=50)
        # Convert ObjectId to string for JSON safety
        for d in docs:
            if "_id" in d:
                d["_id"] = str(d["_id"])
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------
# Guests
# -----------------------------

@app.post("/guests")
def add_guest(guest: Guest):
    try:
        inserted_id = create_document("guest", guest)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/guests")
def list_guests(event_id: Optional[str] = Query(None)):
    try:
        filter_dict = {"event_id": event_id} if event_id else {}
        docs = get_documents("guest", filter_dict, limit=200)
        for d in docs:
            if "_id" in d:
                d["_id"] = str(d["_id"])
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------
# Gifts
# -----------------------------

@app.post("/gifts")
def add_gift(gift: Gift):
    try:
        inserted_id = create_document("gift", gift)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/gifts")
def list_gifts(event_id: Optional[str] = Query(None)):
    try:
        filter_dict = {"event_id": event_id} if event_id else {}
        docs = get_documents("gift", filter_dict, limit=200)
        for d in docs:
            if "_id" in d:
                d["_id"] = str(d["_id"])
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------
# Vendors
# -----------------------------

@app.post("/vendors")
def add_vendor(vendor: Vendor):
    try:
        inserted_id = create_document("vendor", vendor)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/vendors")
def list_vendors(category: Optional[str] = Query(None)):
    try:
        filter_dict = {"category": category} if category else {}
        docs = get_documents("vendor", filter_dict, limit=200)
        for d in docs:
            if "_id" in d:
                d["_id"] = str(d["_id"])
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------
# Memories
# -----------------------------

@app.post("/memories")
def add_memory(memory: Memory):
    try:
        inserted_id = create_document("memory", memory)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/memories")
def list_memories(event_id: Optional[str] = Query(None)):
    try:
        filter_dict = {"event_id": event_id} if event_id else {}
        docs = get_documents("memory", filter_dict, limit=200)
        for d in docs:
            if "_id" in d:
                d["_id"] = str(d["_id"])
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

from fastapi import FastAPI, Header, HTTPException, Depends, Path
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal, engine
from app.models import Base, WebhookEvent
from app.schemas import WebhookResponse, WebhookOut
from app.config import SHARED_SECRET

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Webhook Receiver Service")

# ---------------- DB Dependency ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- GET ALL WEBHOOKS ----------------
@app.get("/webhooks", response_model=List[WebhookOut])
def get_all_webhooks(db: Session = Depends(get_db)):
    return db.query(WebhookEvent).order_by(WebhookEvent.created_at.desc()).all()

# ---------------- GET SINGLE WEBHOOK ----------------
@app.get("/webhooks/{event_id}", response_model=WebhookOut)
def get_webhook_by_event_id(
    event_id: str = Path(..., example="evt_1001"),
    db: Session = Depends(get_db)
):
    event = db.query(WebhookEvent).filter_by(event_id=event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

# ---------------- RECEIVE WEBHOOK ----------------
@app.post("/webhook", response_model=WebhookResponse)
def receive_webhook(
    payload: dict,
    x_signature: str = Header(...),
    db: Session = Depends(get_db)
):
    # 🔐 Validate signature
    if x_signature != SHARED_SECRET:
        raise HTTPException(status_code=401, detail="Invalid signature")

    # 🆔 Idempotency check
    event_id = payload.get("event_id")
    if not event_id:
        raise HTTPException(status_code=400, detail="event_id is required")

    exists = db.query(WebhookEvent).filter_by(event_id=event_id).first()
    if exists:
        return {"status": "ignored", "message": "Duplicate event"}

    event = WebhookEvent(event_id=event_id, payload=payload)
    db.add(event)
    db.commit()

    return {"status": "success", "message": "Webhook stored"}

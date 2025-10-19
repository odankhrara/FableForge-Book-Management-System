from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import httpx, os

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/ai", tags=["ai"])

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")

async def call_ollama(prompt: str) -> str:
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            r = await client.post(url, json=payload)
            r.raise_for_status()
            return r.json().get("response", "")
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Ollama error: {e}")

@router.post("/chat/", response_model=schemas.ChatOut, status_code=status.HTTP_201_CREATED)
async def chat(payload: schemas.ChatIn, db: Session = Depends(get_db)):
    if payload.conversation_id:
        convo = db.get(models.Conversation, payload.conversation_id)
        if not convo:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        convo = models.Conversation(user_id=payload.user_id, title=payload.title or "New chat")
        db.add(convo); db.commit(); db.refresh(convo)

    db.add(models.Message(conversation_id=convo.id, role="user", content=payload.message))
    db.commit()

    msgs = (
        db.query(models.Message)
        .filter(models.Message.conversation_id == convo.id)
        .order_by(models.Message.id.asc())
        .all()
    )
    prompt = "".join(f"{m.role.upper()}: {m.content}\n" for m in msgs[-10:]) + "ASSISTANT:"
    reply = await call_ollama(prompt)
    db.add(models.Message(conversation_id=convo.id, role="assistant", content=reply))
    db.commit()

    return schemas.ChatOut(conversation_id=convo.id, reply=reply)

@router.get("/conversations/", response_model=list[schemas.ConversationOut])
def list_conversations(user_id: int = Query(..., ge=1), db: Session = Depends(get_db)):
    return (
        db.query(models.Conversation)
        .filter(models.Conversation.user_id == user_id)
        .order_by(models.Conversation.id.desc())
        .all()
    )

@router.get("/messages/{conversation_id}", response_model=schemas.MessagesOut)
def list_messages(conversation_id: int, db: Session = Depends(get_db)):
    convo = db.get(models.Conversation, conversation_id)
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")
    msgs = (
        db.query(models.Message)
        .filter(models.Message.conversation_id == conversation_id)
        .order_by(models.Message.id.asc())
        .all()
    )
    return schemas.MessagesOut(conversation_id=conversation_id, messages=msgs)

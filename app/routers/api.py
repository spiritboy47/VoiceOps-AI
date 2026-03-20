# app/routers/api.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.conversation_engine import process_conversation

from app.intent_engine import process_intent
from app.alert_engine import check_alerts

router = APIRouter()


class ChatRequest(BaseModel):
    text: str


#@router.post("/chat")
#def chat(req: ChatRequest):

#    result = process_intent(req.text)

#    return {
#        "response": result["message"],
#        "cpu": result["cpu"],
#        "memory": result["memory"],
#        "disk": result["disk"]
#    }

@router.post("/chat")
def chat(req: ChatRequest):

    # Check if it's general conversation
    convo = process_conversation(req.text)

    if convo:
        return {
            "response": convo,
            "cpu": None,
            "memory": None,
            "disk": None
        }

    # Otherwise process monitoring intent
    result = process_intent(req.text)

    return {
        "response": result["message"],
        "cpu": result["cpu"],
        "memory": result["memory"],
        "disk": result["disk"]
    }


# ==============================
# ALERT API
# ==============================

@router.get("/alerts")
def get_alerts():

    alerts = check_alerts()

    return {
        "alerts": alerts
    }
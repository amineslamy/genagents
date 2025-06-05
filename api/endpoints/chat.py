from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from genagents.genagents import GenerativeAgent

router = APIRouter()

# مسیر ایجنت‌ها
AGENTS_DIR = "agent_bank/custom_agents"

# 📦 مدل ورودی برای چت
class ChatRequest(BaseModel):
    agent_id: str
    user_message: str

# 📦 مدل خروجی برای چت
class ChatResponse(BaseModel):
    response: str
    agent_id: str
    agent_name: str

# 📦 مدل ورودی برای ذخیره حافظه
class MemorySaveRequest(BaseModel):
    agent_id: str
    memory_content: str

# ✅ اندپوینت: چت با ایجنت
@router.post("/message", response_model=ChatResponse)
def chat_with_agent(payload: ChatRequest):
    agent_folder = os.path.join(AGENTS_DIR, payload.agent_id)
    if not os.path.exists(agent_folder):
        raise HTTPException(status_code=404, detail="Agent not found.")
    
    try:
        agent = GenerativeAgent.load(agent_folder)
        reply = agent.generate_dialogue_response(payload.user_message)
        return {
            "response": reply,
            "agent_id": payload.agent_id,
            "agent_name": agent.get_fullname()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error chatting with agent: {str(e)}")

# ✅ اندپوینت: ذخیره حافظه
@router.post("/save-memory")
def save_memory(payload: MemorySaveRequest):
    agent_folder = os.path.join(AGENTS_DIR, payload.agent_id)
    if not os.path.exists(agent_folder):
        raise HTTPException(status_code=404, detail="Agent not found.")

    try:
        agent = GenerativeAgent.load(agent_folder)
        agent.memory.save_memory(payload.memory_content)
        agent.save(agent_folder)

        return {
            "status": "success",
            "message": "حافظه با موفقیت ذخیره شد."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطا در ذخیره حافظه: {str(e)}")

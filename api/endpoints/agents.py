from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os, uuid, json, shutil
from genagents.genagents import GenerativeAgent
from typing import List, Optional, Dict


router = APIRouter()
AGENTS_DIR = "agent_bank/custom_agents"

# ---------- مدل‌های API ----------

class AgentCreateRequest(BaseModel):
    first_name: str
    last_name: str
    age: int
    occupation: str
    interests: list[str]
    tags: Optional[List[str]] = []
    personality_traits: Optional[List[str]] = []
    gss_summary: Optional[List[str]] = []
    behavioral_summary: Optional[List[str]] = []
    character_sentences: Optional[str] = None


class AgentUpdateRequest(BaseModel):
    age: int | None = None
    occupation: str | None = None
    interests: list[str] | None = None

class AgentInfo(BaseModel):
    id: str
    full_name: str
    age: int
    occupation: str
    interests: list[str]
    tags: Optional[List[str]] = []
    personality_traits: Optional[List[str]] = []
    gss_summary: Optional[List[str]] = []
    behavioral_summary: Optional[List[str]] = []
    character_sentences: Optional[List[str]] = []

# ---------- لیست ایجنت‌ها ----------

@router.get("/")
def list_agents():
    agents = []
    for folder in os.listdir(AGENTS_DIR):
        path = os.path.join(AGENTS_DIR, folder, 'scratch.json')
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                agents.append({
                    "id": folder,
                    "full_name": f"{data.get('first_name')} {data.get('last_name')}",
                    "age": data.get("age"),
                    "occupation": data.get("occupation"),
                    "interests": data.get("interests", []),
                    "tags": data.get("tags", []),
                    "personality_traits": data.get("personality_traits", []),
                    "gss_summary": data.get("gss_summary", []),
                    "behavioral_summary": data.get("behavioral_summary", []),
                    "character_sentences": data.get("character_sentences", []),
                })
    return agents

# ---------- ایجاد ایجنت جدید ----------

@router.post("/create")
def create_agent(agent_data: AgentCreateRequest):
    try:
        agent = GenerativeAgent()
        data = agent_data.dict()
        agent.update_scratch(data)

        agent_id = f"{agent_data.first_name.lower()}_{agent_data.last_name.lower()}_{uuid.uuid4().hex[:6]}"
        folder_path = os.path.join(AGENTS_DIR, agent_id)
        os.makedirs(folder_path, exist_ok=True)

        agent.save(folder_path)

        # افزودن یک observation اولیه (نام، نام خانوادگی، سن، شغل، علایق)
        personal_info_obs = f"نام: {data['first_name']}، نام خانوادگی: {data['last_name']}، سن: {data['age']}، شغل: {data['occupation']}، علایق: {', '.join(data['interests'])}"
        agent.remember(personal_info_obs)

        # برچسب‌ها در یک observation جداگانه
        if data.get('tags'):
            tags_obs = f"برچسب‌ها: {', '.join(data['tags'])}"
            agent.remember(tags_obs)

        # هر پاسخ کاربر به صورت observation جداگانه ذخیره شود
        for trait in data.get("personality_traits", []):
            agent.remember(trait)
        for gss in data.get("gss_summary", []):
            agent.remember(gss)
        for beh in data.get("behavioral_summary", []):
            agent.remember(beh)
        # اگر character_sentences لیست است
        char_sents = data.get("character_sentences", [])
        if isinstance(char_sents, list):
            for sent in char_sents:
                agent.remember(sent)
        elif isinstance(char_sents, str):
            agent.remember(char_sents)

        # اجرای بازتاب فکری کلی (اختیاری)
        anchor = json.dumps(agent.scratch, ensure_ascii=False)
        agent.reflect(anchor)
        agent.save(folder_path)

        return {
            "status": "success",
            "agent_id": agent_id,
            "message": f"شخصیت '{agent.get_fullname()}' با موفقیت ساخته شد و بازتاب فکری انجام شد."
        }
    except Exception as e:
        print(f"[ERROR] خطا در ثبت شخصیت: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"خطا در ثبت شخصیت: {str(e)}")

# ---------- دریافت اطلاعات یک ایجنت ----------

@router.get("/{agent_id}")
def get_agent(agent_id: str):
    folder = os.path.join(AGENTS_DIR, agent_id)
    scratch_path = os.path.join(folder, "scratch.json")
    if not os.path.exists(scratch_path):
        raise HTTPException(status_code=404, detail="Agent not found")

    with open(scratch_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return {
        "id": agent_id,
        "full_name": f"{data.get('first_name')} {data.get('last_name')}",
        "age": data.get("age"),
        "occupation": data.get("occupation"),
        "interests": data.get("interests", []),
        "tags": data.get("tags", []),
        "personality_traits": data.get("personality_traits", []),
        "gss_summary": data.get("gss_summary", []),
        "behavioral_summary": data.get("behavioral_summary", []),
        "character_sentences": data.get("character_sentences", []),
    }

# ---------- به‌روزرسانی اطلاعات ایجنت ----------

@router.put("/{agent_id}/update")
def update_agent(agent_id: str, updates: AgentUpdateRequest):
    folder = os.path.join(AGENTS_DIR, agent_id)
    if not os.path.exists(folder):
        raise HTTPException(status_code=404, detail="Agent not found")

    agent = GenerativeAgent.load(folder)
    current = agent.scratch

    # فقط فیلدهایی که تغییر کردند، به‌روزرسانی می‌شن
    new_data = current.copy()
    if updates.age is not None:
        new_data["age"] = updates.age
    if updates.occupation is not None:
        new_data["occupation"] = updates.occupation
    if updates.interests is not None:
        new_data["interests"] = updates.interests

    agent.update_scratch(new_data)
    agent.save(folder)

    return {
        "status": "success",
        "message": f"اطلاعات شخصیت '{agent.get_fullname()}' به‌روزرسانی شد."
    }

# ---------- حذف ایجنت ----------

@router.delete("/{agent_id}")
def delete_agent(agent_id: str):
    folder = os.path.join(AGENTS_DIR, agent_id)
    if not os.path.exists(folder):
        raise HTTPException(status_code=404, detail="Agent not found")

    shutil.rmtree(folder)
    return {
        "status": "success",
        "message": f"شخصیت '{agent_id}' حذف شد."
    }

#---------بازتاب فکری ایجنت ها----------
@router.post("/{agent_id}/reflect")
def reflect_agent(agent_id: str):
    folder = os.path.join(AGENTS_DIR, agent_id)
    if not os.path.exists(folder):
        raise HTTPException(status_code=404, detail="Agent not found")

    try:
        agent = GenerativeAgent.load(folder)
        # استفاده از کل محتوای scratch به عنوان anchor
        anchor = json.dumps(agent.scratch, ensure_ascii=False)
        reflection = agent.reflect(anchor)
        agent.save(folder)

        return {
            "status": "success",
            "message": f"بازتاب فکری برای '{agent.get_fullname()}' انجام شد.",
            "output": reflection  # خروجی ممکن است None یا متن باشد
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطا در بازتاب فکری: {str(e)}")
#----------مصاحبه با ایجنت---------
class InterviewRequest(BaseModel):
    questions: list[str]

@router.post("/{agent_id}/interview")
def interview_agent(agent_id: str, request: InterviewRequest):
    folder = os.path.join(AGENTS_DIR, agent_id)
    if not os.path.exists(folder):
        raise HTTPException(status_code=404, detail="Agent not found")

    try:
        agent = GenerativeAgent.load(folder)
        responses = []

        for q in request.questions:
            response = agent.generate_dialogue_response(q)
            responses.append(response)

        return {
            "status": "success",
            "agent": agent.get_fullname(),
            "responses": responses
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطا در مصاحبه: {str(e)}")
#-----------نظرسنجی از ایجنت--------
class SurveyRequest(BaseModel):
    question: str

@router.post("/{agent_id}/survey")
def survey_agent(agent_id: str, request: SurveyRequest):
    folder = os.path.join(AGENTS_DIR, agent_id)
    if not os.path.exists(folder):
        raise HTTPException(status_code=404, detail="Agent not found")

    try:
        agent = GenerativeAgent.load(folder)
        answer = agent.generate_dialogue_response(request.question)

        return {
            "status": "success",
            "question": request.question,
            "answer": answer
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطا در نظرسنجی: {str(e)}")


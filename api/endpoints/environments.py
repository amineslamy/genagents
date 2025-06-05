from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from datetime import datetime, timedelta
from genagents.genagents import GenerativeAgent
import json,random

router = APIRouter()

ENVIRONMENTS_DIR = "agent_bank/environments"
AGENTS_DIR = "agent_bank/custom_agents"

class EnvironmentCreateRequest(BaseModel):
    name: str
    description: str = ""

class AddAgentRequest(BaseModel):
    agent_id: str

@router.get("/")
def list_environments():
    if not os.path.exists(ENVIRONMENTS_DIR):
        return []
    
    envs = []
    for folder in os.listdir(ENVIRONMENTS_DIR):
        path = os.path.join(ENVIRONMENTS_DIR, folder, "state.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                import json
                data = json.load(f)
                envs.append({
                    "id": folder,
                    "name": data.get("name"),
                    "description": data.get("description", "")
                })
    return envs

@router.post("/create")
def create_environment(data: EnvironmentCreateRequest):
    env_id = data.name.lower().replace(" ", "_")
    folder_path = os.path.join(ENVIRONMENTS_DIR, env_id)

    if os.path.exists(folder_path):
        raise HTTPException(status_code=400, detail="Environment already exists")

    os.makedirs(folder_path, exist_ok=True)
    
    # ذخیره state.json
    with open(os.path.join(folder_path, "state.json"), "w", encoding="utf-8") as f:
        import json
        json.dump({
            "name": data.name,
            "description": data.description
        }, f, indent=2, ensure_ascii=False)

    # فایل agents.txt برای لیست ایجنت‌ها
    open(os.path.join(folder_path, "agents.txt"), "w").close()

    return {
        "status": "success",
        "message": f"محیط '{data.name}' ایجاد شد.",
        "id": env_id
    }

@router.put("/{env_id}/add-agent")
def add_agent_to_environment(env_id: str, request: AddAgentRequest):
    env_path = os.path.join(ENVIRONMENTS_DIR, env_id)
    agent_path = os.path.join(AGENTS_DIR, request.agent_id)

    if not os.path.exists(env_path):
        raise HTTPException(status_code=404, detail="Environment not found")
    if not os.path.exists(agent_path):
        raise HTTPException(status_code=404, detail="Agent not found")

    agents_file = os.path.join(env_path, "agents.txt")
    with open(agents_file, "a+", encoding="utf-8") as f:
        f.seek(0)
        existing = f.read().splitlines()
        if request.agent_id not in existing:
            f.write(request.agent_id + "\n")

    return {
        "status": "success",
        "message": f"ایجنت '{request.agent_id}' به محیط '{env_id}' اضافه شد."
    }

@router.get("/{env_id}")
def get_environment_info(env_id: str):
    path = os.path.join(ENVIRONMENTS_DIR, env_id, "state.json")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Environment not found")

    with open(path, "r", encoding="utf-8") as f:
        import json
        return json.load(f)

@router.get("/{env_id}/agents")
def list_agents_in_environment(env_id: str):
    path = os.path.join(ENVIRONMENTS_DIR, env_id, "agents.txt")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Environment not found")

    with open(path, "r", encoding="utf-8") as f:
        agent_ids = f.read().splitlines()
    return {"agents": agent_ids}
class SimulationRequest(BaseModel):
    rounds: int = 1  # تعداد دفعات تعامل (مثلاً ۲ گفتگو در هر نوبت)
from genagents.genagents import GenerativeAgent
import random

@router.post("/{env_id}/simulate")
def simulate_interaction(env_id: str, data: SimulationRequest):
    env_path = os.path.join(ENVIRONMENTS_DIR, env_id)
    agents_file = os.path.join(env_path, "agents.txt")
    if not os.path.exists(agents_file):
        raise HTTPException(status_code=404, detail="Environment not found")

    with open(agents_file, "r", encoding="utf-8") as f:
        agent_ids = f.read().splitlines()

    if len(agent_ids) < 2:
        raise HTTPException(status_code=400, detail="At least 2 agents are required.")

    log_file = os.path.join(env_path, "interactions.log")
    log_lines = []

    for _ in range(data.rounds):
        a1, a2 = random.sample(agent_ids, 2)
        a1_path = os.path.join(AGENTS_DIR, a1)
        a2_path = os.path.join(AGENTS_DIR, a2)

        agent1 = GenerativeAgent.load(a1_path)
        agent2 = GenerativeAgent.load(a2_path)

        message = f"سلام، حالت چطوره؟"
        response = agent2.generate_dialogue_response(message)

        line1 = f"{agent1.get_fullname()} -> {agent2.get_fullname()}: {message}"
        line2 = f"{agent2.get_fullname()}: {response}"
        log_lines.extend([line1, line2])

    with open(log_file, "a", encoding="utf-8") as f:
        for line in log_lines:
            f.write(line + "\n")

    return {
        "status": "success",
        "message": f"{data.rounds} تعامل با موفقیت شبیه‌سازی شد.",
        "log": log_lines
    }
@router.get("/{env_id}/interactions")
def get_interaction_logs(env_id: str):
    log_file = os.path.join(ENVIRONMENTS_DIR, env_id, "interactions.log")
    if not os.path.exists(log_file):
        return {"interactions": []}

    with open(log_file, "r", encoding="utf-8") as f:
        return {"interactions": f.read().splitlines()}
#---------بازتاب فکری ایجنت ها--------
@router.post("/{env_id}/reflect")
def reflect_all_agents(env_id: str):
    env_path = os.path.join(ENVIRONMENTS_DIR, env_id)
    agents_file = os.path.join(env_path, "agents.txt")

    if not os.path.exists(agents_file):
        raise HTTPException(status_code=404, detail="Environment not found")

    with open(agents_file, "r", encoding="utf-8") as f:
        agent_ids = f.read().splitlines()

    if not agent_ids:
        raise HTTPException(status_code=400, detail="No agents in environment")

    results = []
    for agent_id in agent_ids:
        try:
            agent_path = os.path.join(AGENTS_DIR, agent_id)
            agent = GenerativeAgent.load(agent_path)
            reflection = agent.reflect()
            agent.save(agent_path)
            results.append({
                "agent_id": agent_id,
                "name": agent.get_fullname(),
                "reflection": reflection
            })
        except Exception as e:
            results.append({
                "agent_id": agent_id,
                "error": str(e)
            })

    return {
        "status": "completed",
        "results": results
    }
#--------مدیریت و جلو بردن ساعت محیط--------
class AdvanceTimeRequest(BaseModel):
    hours: int = 1



@router.post("/{env_id}/advance-time")
def advance_time(env_id: str, data: AdvanceTimeRequest):
    env_path = os.path.join(ENVIRONMENTS_DIR, env_id)
    state_path = os.path.join(env_path, "state.json")
    agents_file = os.path.join(env_path, "agents.txt")
    log_file = os.path.join(env_path, "interactions.log")

    if not os.path.exists(state_path) or not os.path.exists(agents_file):
        raise HTTPException(status_code=404, detail="Environment not found")

    with open(state_path, "r", encoding="utf-8") as f:
        state = json.load(f)

    # افزایش زمان
    current_time = state.get("current_time", "08:00")
    dt = datetime.strptime(current_time, "%H:%M")
    dt += timedelta(hours=data.hours)
    new_time = dt.strftime("%H:%M")
    state["current_time"] = new_time

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    # تعامل و بازتاب هوشمند
    with open(agents_file, "r", encoding="utf-8") as f:
        agent_ids = f.read().splitlines()

    if len(agent_ids) < 2:
        return {
            "status": "warning",
            "message": f"زمان جلو رفت ولی تعداد ایجنت کافی برای تعامل نبود.",
            "new_time": new_time
        }

    log_lines = []
    reflection_results = []

    for _ in range(2):  # دو تعامل
        a1, a2 = random.sample(agent_ids, 2)
        a1_path = os.path.join(AGENTS_DIR, a1)
        a2_path = os.path.join(AGENTS_DIR, a2)

        agent1 = GenerativeAgent.load(a1_path)
        agent2 = GenerativeAgent.load(a2_path)

        msg = f"سلام! الان ساعت {new_time} هست، چه خبر؟"
        reply = agent2.generate_dialogue_response(msg)

        log_lines.append(f"{agent1.get_fullname()} -> {agent2.get_fullname()}: {msg}")
        log_lines.append(f"{agent2.get_fullname()}: {reply}")

        agent1.save(a1_path)
        agent2.save(a2_path)

    # ذخیره تعاملات
    with open(log_file, "a", encoding="utf-8") as f:
        for line in log_lines:
            f.write(line + "\n")

    # انجام بازتاب فکری برای هر ایجنت
    for aid in agent_ids:
        try:
            apath = os.path.join(AGENTS_DIR, aid)
            agent = GenerativeAgent.load(apath)
            output = agent.reflect()
            agent.save(apath)
            reflection_results.append({
                "agent_id": aid,
                "reflection": output or "بدون خروجی قابل ثبت"
            })
        except Exception as e:
            reflection_results.append({
                "agent_id": aid,
                "error": str(e)
            })

    return {
        "status": "success",
        "message": f"زمان به مدت {data.hours} ساعت جلو رفت، تعامل و بازتاب انجام شد.",
        "new_time": new_time,
        "interactions": log_lines,
        "reflections": reflection_results
    }

#--------گزارش گیری از رفتار ایجنت ها در یک محیط------
@router.get("/{env_id}/report")
def get_environment_report(env_id: str):
    import collections
    import json

    env_path = os.path.join(ENVIRONMENTS_DIR, env_id)
    state_path = os.path.join(env_path, "state.json")
    agents_file = os.path.join(env_path, "agents.txt")
    log_file = os.path.join(env_path, "interactions.log")

    if not os.path.exists(state_path):
        raise HTTPException(status_code=404, detail="Environment not found")

    # ساعت فعلی محیط
    with open(state_path, "r", encoding="utf-8") as f:
        state = json.load(f)
    current_time = state.get("current_time", "08:00")

    # لیست ایجنت‌ها
    agent_ids = []
    if os.path.exists(agents_file):
        with open(agents_file, "r", encoding="utf-8") as f:
            agent_ids = f.read().splitlines()

    # تحلیل تعاملات
    interactions = []
    talk_count = collections.Counter()

    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            for line in f:
                interactions.append(line.strip())
                if "->" in line:
                    speaker = line.split("->")[0].strip()
                    talk_count[speaker] += 1

    report = {
        "current_time": current_time,
        "agent_count": len(agent_ids),
        "total_interactions": len(interactions) // 2,
        "top_speakers": talk_count.most_common(5),
    }

    return {
        "status": "success",
        "report": report
    }

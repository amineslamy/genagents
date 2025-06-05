# main.py
from fastapi import FastAPI
import datetime

# --- شروع بخش اصلاح شده برای وارد کردن ماژول‌ها ---
# ماژول‌ها و کلاس‌های اصلی پروژه شما
# این مسیرها بر اساس ساختار پروژه شما تنظیم شده‌اند.

# از پکیج genagents، ماژول genagents، کلاس GenerativeAgent را وارد کن
# (فرض بر این است که کلاسی به نام GenerativeAgent در فایل genagents/genagents.py وجود دارد)
from genagents.genagents import GenerativeAgent

# از پکیج simulation_engine، ماژول global_methods را وارد کن
# (شما در terminal_chat.py از from simulation_engine.global_methods import * استفاده کرده بودید)
# بسته به نیاز، می‌توانید کل ماژول یا توابع/کلاس‌های خاصی را وارد کنید.
# مثلاً: from simulation_engine import global_methods
# یا اگر کلاس SimulationEngine در فایل دیگری در این پوشه است، مسیر آن را مشخص کنید.
# فعلاً یک placeholder برای SimulationEngine می‌گذاریم، باید بررسی کنیم این کلاس کجاست.
# from simulation_engine.some_module import SimulationEngine # نیاز به بررسی دارد

# از پکیج environment، ماژول environment، کلاس Environment را وارد کن
# (فرض بر این است که کلاسی به نام Environment در فایل environment/environment.py وجود دارد)
# from environment.environment import Environment # اگر چنین کلاسی دارید

# --- پایان بخش اصلاح شده ---

app = FastAPI(
    title="GenAgents API",
    description="API برای مدیریت و تعامل با شخصیت‌های مبتنی بر هوش مصنوعی (Generative Agents - فارسی)",
    version="0.1.0",
)

@app.get("/")
async def read_root():
    """
    اندپوینت ریشه که یک پیام خوشامدگویی ساده برمی‌گرداند.
    """
    return {
        "message": "به API پروژه GenAgents خوش آمدید!",
        "timestamp": datetime.datetime.now().isoformat(),
        "documentation_url": "/docs"
    }

@app.get("/greet/{name}")
async def greet_person(name: str):
    """
    یک اندپوینت ساده برای خوشامدگویی به یک شخص با نام مشخص.
    """
    return {"greeting": f"سلام، {name} عزیز! از API پروژه GenAgents."}

# --- اندپوینت آزمایشی برای تست بارگذاری GenerativeAgent ---
# این اندپوینت را برای تست اضافه می‌کنیم.
# لطفاً مطمئن شوید که یک ایجنت نمونه در مسیر مشخص شده وجود دارد
# یا مسیر را به یک ایجنت معتبر در پروژه خود تغییر دهید.
AGENT_EXAMPLE_FOLDER = "agent_bank/populations/single_agent/01fd7d2a-0357-4c1b-9f3e-8eade2d537ae"

@app.get("/test-load-agent/")
async def test_load_agent():
    """
    یک اندپوینت آزمایشی برای بررسی اینکه آیا GenerativeAgent به درستی وارد و نمونه‌سازی می‌شود.
    """
    try:
        # فرض می‌کنیم سازنده GenerativeAgent یک پارامتر agent_folder می‌گیرد
        # همانطور که در terminal_chat.py دیده شد.
        agent = GenerativeAgent(agent_folder=AGENT_EXAMPLE_FOLDER)
        agent_name = agent.get_fullname() # فرض می‌کنیم متد get_fullname() وجود دارد
        return {
            "status": "success",
            "message": f"عامل '{agent_name}' با موفقیت بارگذاری شد.",
            "agent_details": {
                "name": agent_name,
                # می‌توانید اطلاعات بیشتری از ایجنت را اینجا برگردانید
                # "description": agent.description, # اگر چنین ویژگی‌ای دارد
            }
        }
    except FileNotFoundError as e:
        return {
            "status": "error",
            "error_type": "FileNotFoundError",
            "message": f"فایل‌های مورد نیاز برای عامل در مسیر '{AGENT_EXAMPLE_FOLDER}' یافت نشد. جزئیات: {str(e)}"
        }
    except ImportError as e:
        return {
            "status": "error",
            "error_type": "ImportError",
            "message": f"خطا در وارد کردن ماژول‌های مورد نیاز GenerativeAgent. جزئیات: {str(e)}"
        }
    except Exception as e:
        # گرفتن هرگونه خطای دیگر هنگام نمونه‌سازی یا استفاده از ایجنت
        return {
            "status": "error",
            "error_type": type(e).__name__,
            "message": f"خطایی هنگام بارگذاری یا استفاده از عامل رخ داد: {str(e)}"
        }

# -------------------------------------------------------------

if __name__ == "__main__":
    print("برای اجرای این برنامه FastAPI، از دستور زیر در ترمینال استفاده کنید:")
    print("uvicorn main:app --reload")
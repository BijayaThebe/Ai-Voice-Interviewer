# app/conversation/thinking_simulator.py
import asyncio
import random
from .memory import InterviewMemory

async def simulate_thinking_delay():
    # Humans pause 0.8s–2.2s before complex responses
    delay = random.uniform(0.8, 2.2)
    await asyncio.sleep(delay)

def analyze_for_follow_up(user_response: str, memory: InterviewMemory) -> str:
    # Lightweight logic (or call small LLM) to decide next move
    if "team conflict" in user_response.lower():
        return "Can you share how you resolved that conflict?"
    return ""
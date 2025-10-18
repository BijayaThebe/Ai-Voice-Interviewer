# # app/events.py
# import asyncio
# import random
# from flask import request
# from flask_socketio import emit
# from .llm.providers import call_llm
# from .llm.utils import sanitize_input

# # Global session store (use Redis in production)
# sessions = {}

# def register_socketio_events(socketio):
#     @socketio.on('start_voice_interview')
#     def handle_start(data):
#         sid = request.sid
#         api_key = data.get('api_key', '').strip()
#         provider = data.get('provider', 'groq').lower()
#         job_role = sanitize_input(data.get('job_role', ''))
#         job_desc = sanitize_input(data.get('job_desc', ''))

#         if not api_key or not job_role or not job_desc:
#             emit('error', {'msg': '❌ Please provide API key, job role, and description.'})
#             return

#         sessions[sid] = {
#             'api_key': api_key,
#             'provider': provider,
#             'job_role': job_role,
#             'job_desc': job_desc,
#             'questions_asked': 0,
#             'max_questions': 5,
#             'history': []  # Will store Q&A pairs
#         }

#         welcome = (
#             f"Hello! Welcome to your {job_role} interview. I'm really looking forward to learning more about you. "
#             f"To get us started—could you tell me a bit about yourself and your background?"
#         )
#         emit('ai_speak', {'text': welcome})

#     @socketio.on('user_spoke')
#     def handle_user_answer(data):
#         sid = request.sid
#         session = sessions.get(sid)
#         if not session:
#             emit('error', {'msg': 'Session expired. Please restart the interview.'})
#             return

#         user_answer = sanitize_input(data.get('text', ''))
#         if not user_answer or len(user_answer.strip()) < 5:
#             emit('ai_speak', {'text': "I didn’t quite catch that. Could you say it again a bit more clearly?"})
#             return

#         # Store full context for smarter follow-ups later
#         session['history'].append({
#             'answer': user_answer
#         })

#         # Simulate human-like "thinking" pause (0.8s – 1.8s)
#         # Note: Flask-SocketIO is synchronous by default; use sleep for simplicity
#         # In async mode, you'd use await asyncio.sleep()
#         socketio.sleep(random.uniform(0.8, 1.8))

#         # Build context from past answers (for smarter questioning)
#         history_text = "\n".join([f"Answer {i+1}: {h['answer']}" 
#                                   for i, h in enumerate(session['history'][-3:])])  # last 3 answers

#         # Generate feedback + next question in one call (more coherent)
#         prompt = f"""
# You are a professional, empathetic hiring manager for a {session['job_role']} role.
# Job description: {session['job_desc'][:200]}

# Previous candidate answers:
# {history_text}

# Latest answer: "{user_answer}"

# Instructions:
# - First, give ONE short, encouraging sentence of feedback (e.g., "That’s a great example of initiative.").
# - Then, ask ONE thoughtful, open-ended follow-up question that digs deeper into their experience, skills, or behavior.
# - Do NOT repeat previous topics.
# - Keep total response under 35 words.
# - Sound natural—like a real person speaking aloud.
#         """.strip()

#         response = call_llm(
#             session['api_key'],
#             user_message=prompt,
#             system_prompt="You are a human-like, thoughtful interviewer.",
#             provider=session['provider']
#         )

#         session['questions_asked'] += 1

#         # Handle interview end
#         if session['questions_asked'] >= session['max_questions']:
#             closing = f"{response} That’s all the questions I have for today. Thank you so much for your time—your insights were really valuable!"
#             emit('ai_speak', {'text': closing})
#             emit('interview_complete', {'history': session['history']})
#             sessions.pop(sid, None)
#         else:
#             # Optional: Wrap in SSML later for TTS pauses
#             emit('ai_speak', {'text': response})





# app/events.py
import asyncio
import random
import re
from flask import request
from flask_socketio import emit
from .llm.providers import call_llm
from .llm.utils import sanitize_input

# Global session store (use Redis in production)
sessions = {}

# --- NEW: Sentiment keywords for analysis ---
POSITIVE_INDICATORS = [
    "excited", "love", "passionate", "enjoy", "thrilled", "proud", 
    "accomplished", "satisfied", "motivated", "inspired"
]
NEGATIVE_INDICATORS = [
    "frustrated", "disappointed", "struggled", "challenged", "difficult", 
    "tough", "stress", "overwhelmed", "hard", "struggle"
]
CONFIDENCE_INDICATORS = [
    "definitely", "clearly", "absolutely", "confidently", "certainly", 
    "undoubtedly", "without a doubt", "sure"
]
VAGUE_INDICATORS = [
    "kind of", "sort of", "maybe", "a bit", "somewhat", "pretty much", 
    "thing is", "well", "um", "uh"
]

def register_socketio_events(socketio):
    @socketio.on('start_voice_interview')
    def handle_start(data):
        sid = request.sid
        api_key = data.get('api_key', '').strip()
        provider = data.get('provider', 'groq').lower()
        job_role = sanitize_input(data.get('job_role', ''))
        job_desc = sanitize_input(data.get('job_desc', ''))

        if not api_key or not job_role or not job_desc:
            emit('error', {'msg': '❌ Please provide API key, job role, and description.'})
            return

        sessions[sid] = {
            'api_key': api_key,
            'provider': provider,
            'job_role': job_role,
            'job_desc': job_desc,
            'questions_asked': 0,
            'max_questions': 5,
            'history': [],
            'candidate_sentiment_trend': []  # Track mood changes
        }

        welcome = (
            f"Hello! Welcome to your {job_role} interview. I'm really looking forward to learning more about you. "
            f"To get us started—could you tell me a bit about yourself and your background?"
        )
        # Emit with SSML pause
        emit('ai_speak', {'text': welcome, 'ssml': f'<speak>{welcome}<break time="600ms"/></speak>'})

    @socketio.on('user_spoke')
    def handle_user_answer(data):
        sid = request.sid
        session = sessions.get(sid)
        if not session:
            emit('error', {'msg': 'Session expired. Please restart the interview.'})
            return

        user_answer = sanitize_input(data.get('text', ''))
        if not user_answer or len(user_answer.strip()) < 5:
            emit('ai_speak', {'text': "I didn’t quite catch that. Could you say it again a bit more clearly?", 
                              'ssml': '<speak>I didn’t quite catch that. Could you say it again a bit more clearly?<break time="600ms"/></speak>'})
            return

        # --- ANALYTICAL TASKS ---
        # 1. Sentiment Analysis
        sentiment_score = analyze_sentiment(user_answer)
        session['candidate_sentiment_trend'].append(sentiment_score)

        # 2. Detect vagueness, confidence, etc.
        is_vague = any(v in user_answer.lower() for v in VAGUE_INDICATORS)
        is_confident = any(c in user_answer.lower() for c in CONFIDENCE_INDICATORS)

        # 3. Adjust pause based on complexity
        pause_duration = calculate_thinking_pause(user_answer, is_vague)
        socketio.sleep(pause_duration)

        # Store full context
        session['history'].append({
            'answer': user_answer,
            'sentiment': sentiment_score,
            'vague': is_vague,
            'confident': is_confident
        })

        # --- CRITICAL THINKING LOGIC ---
        # Build context from past answers
        history_text = "\n".join([f"Answer {i+1}: {h['answer']}" 
                                  for i, h in enumerate(session['history'][-3:])])

        # Adjust system prompt based on candidate's mood
        emotional_tone = "empathetic and encouraging" if sentiment_score < 0 else "professional and probing"
        if is_vague:
            emotional_tone += " and probing for more detail"

        # Enhanced prompt for analytical depth
        prompt = f"""
You are a {emotional_tone} senior hiring manager for a {session['job_role']} role.
Job description: {session['job_desc'][:200]}

Previous candidate answers:
{history_text}

Latest answer: "{user_answer}"

Instructions:
- First, acknowledge their answer with 1 sentence (adjust tone based on mood).
- If they were vague, ask for a specific example or detail.
- If they mentioned a challenge, ask how they felt or what they learned.
- Then ask a thoughtful follow-up question that shows you were listening.
- Do NOT repeat previous topics.
- Keep total response under 40 words.
- Sound like a real person—use natural pauses and transitions.
        """.strip()

        response = call_llm(
            session['api_key'],
            user_message=prompt,
            system_prompt="You are a human-like, thoughtful, and analytical interviewer. Always probe deeper.",
            provider=session['provider']
        )

        session['questions_asked'] += 1

        # Add SSML for natural pauses in TTS
        ssml_response = f"""
        <speak>
            {response}
            <break time="{random.randint(400, 800)}ms"/>
        </speak>
        """

        # Handle interview end
        if session['questions_asked'] >= session['max_questions']:
            closing = f"{response} That’s all the questions I have for today. Thank you so much for your time—your insights were really valuable!"
            emit('ai_speak', {'text': closing, 
                              'ssml': f'<speak>{closing}<break time="800ms"/></speak>'})
            emit('interview_complete', {'history': session['history']})
            sessions.pop(sid, None)
        else:
            emit('ai_speak', {'text': response, 'ssml': ssml_response})


# --- NEW: Sentiment Analysis Function ---
def analyze_sentiment(text: str) -> int:
    """Returns: -1 (negative), 0 (neutral), 1 (positive)"""
    text_lower = text.lower()
    pos_count = sum(1 for word in POSITIVE_INDICATORS if word in text_lower)
    neg_count = sum(1 for word in NEGATIVE_INDICATORS if word in text_lower)
    
    if pos_count > neg_count:
        return 1
    elif neg_count > pos_count:
        return -1
    else:
        return 0  # Neutral


# --- NEW: Dynamic Pause Calculation ---
def calculate_thinking_pause(text: str, is_vague: bool) -> float:
    """Calculate a natural pause based on content length and clarity."""
    word_count = len(text.split())
    base_pause = 0.6  # Base human thinking time
    
    # Longer answers = more pause
    length_factor = min(word_count / 20, 1.2)  # Cap at 1.2s for long answers
    
    # Vague answers = longer pause (as if confused)
    vagueness_factor = 0.8 if is_vague else 0.0
    
    # Random variation for realism
    random_factor = random.uniform(-0.2, 0.2)
    
    total_pause = base_pause + length_factor + vagueness_factor + random_factor
    return max(0.5, min(total_pause, 2.5))  # Between 0.5s and 2.5s
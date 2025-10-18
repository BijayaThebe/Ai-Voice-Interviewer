from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import requests
import time
import re
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'voice-ai-interview-free'
socketio = SocketIO(app, cors_allowed_origins="*")

sessions = {}

def sanitize_input(text: str) -> str:
    """Remove problematic characters to avoid prompt corruption."""
    return re.sub(r'[<>"{}]', '', text.strip())[:500]

# ============================================
# OPTION 1: GROQ API (FASTEST & FREE)
# ============================================
def call_groq_llm(api_key: str, user_message: str, system_prompt: str = "") -> str:
    """
    Groq Cloud - FREE & SUPER FAST (100+ tokens/sec)
    Get API key: https://console.groq.com/keys
    """
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.1-8b-instant",  # Fast and smart
        "messages": [
            {"role": "system", "content": system_prompt or "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 150
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            return f"Groq Error {response.status_code}: {response.text[:100]}"
    except Exception as e:
        return f"Groq Error: {str(e)[:100]}"

# ============================================
# OPTION 2: TOGETHER AI (FREE TIER)
# ============================================
def call_together_llm(api_key: str, user_message: str, system_prompt: str = "") -> str:
    """
    Together AI - FREE tier with multiple models
    Get API key: https://api.together.xyz/settings/api-keys
    """
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta-llama/Llama-3-8b-chat-hf",
        "messages": [
            {"role": "system", "content": system_prompt or "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 150
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            return f"Together Error {response.status_code}: {response.text[:100]}"
    except Exception as e:
        return f"Together Error: {str(e)[:100]}"

# ============================================
# OPTION 3: OPENROUTER (MULTIPLE FREE MODELS)
# ============================================
def call_openrouter_llm(api_key: str, user_message: str, system_prompt: str = "") -> str:
    """
    OpenRouter - Access to multiple free models
    Get API key: https://openrouter.ai/keys
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "Voice AI Interviewer"
    }
    payload = {
        "model": "meta-llama/llama-3.1-8b-instruct:free",  # Free model
        "messages": [
            {"role": "system", "content": system_prompt or "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 150
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            return f"OpenRouter Error {response.status_code}: {response.text[:100]}"
    except Exception as e:
        return f"OpenRouter Error: {str(e)[:100]}"

# ============================================
# OPTION 4: PERPLEXITY AI (FREE TIER)
# ============================================
def call_perplexity_llm(api_key: str, user_message: str, system_prompt: str = "") -> str:
    """
    Perplexity AI - Good free tier
    Get API key: https://www.perplexity.ai/settings/api
    """
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [
            {"role": "system", "content": system_prompt or "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 150
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            return f"Perplexity Error {response.status_code}: {response.text[:100]}"
    except Exception as e:
        return f"Perplexity Error: {str(e)[:100]}"

# ============================================
# MAIN FUNCTION - AUTO DETECT PROVIDER
# ============================================
def call_llm(api_key: str, user_message: str, system_prompt: str = "", provider: str = "groq") -> str:
    """
    Main function that routes to the selected provider
    """
    user_message = sanitize_input(user_message)
    system_prompt = sanitize_input(system_prompt) or "You are a helpful assistant."
    
    providers = {
        "groq": call_groq_llm,
        "together": call_together_llm,
        "openrouter": call_openrouter_llm,
        "perplexity": call_perplexity_llm
    }
    
    if provider.lower() in providers:
        return providers[provider.lower()](api_key, user_message, system_prompt)
    else:
        return "Invalid provider. Choose: groq, together, openrouter, or perplexity"

@socketio.on('start_voice_interview')
def handle_start(data):
    sid = request.sid
    api_key = data.get('api_key', '').strip()
    provider = data.get('provider', 'groq').lower()  # Default to Groq
    job_role = sanitize_input(data.get('job_role', ''))
    job_desc = sanitize_input(data.get('job_desc', ''))

    print(f"[INFO] Starting interview with {provider.upper()}")
    print(f"[INFO] Role: {job_role}")

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
        'difficulty_level': 'introduction',  # Start with introduction
        'history': []
    }

    # Start with warm introduction
    welcome = (
        f"Hello! Welcome to your {job_role} interview. I'm excited to learn more about you today. "
        f"Let's start with a simple question: Can you tell me a bit about yourself and your background?"
    )
    emit('ai_speak', {'text': welcome})

@socketio.on('user_spoke')
def handle_user_answer(data):
    sid = request.sid
    session = sessions.get(sid)
    
    if not session:
        emit('error', {'msg': 'Session expired. Please restart.'})
        return

    user_answer = sanitize_input(data.get('text', ''))
    
    if not user_answer:
        emit('ai_speak', {'text': "I didn't catch that. Could you repeat?"})
        return

    session['questions_asked'] += 1
    session['history'].append({
        'question_index': session['questions_asked'],
        'answer': user_answer
    })

    # Generate feedback
    feedback = call_llm(
        session['api_key'],
        f"Give brief positive feedback (one sentence) on: '{user_answer}'",
        "You are a supportive interviewer.",
        session['provider']
    )

    if session['questions_asked'] >= 5:
        closing = f"{feedback} That's all for today. Thank you!"
        emit('ai_speak', {'text': closing})
        emit('interview_complete', {'history': session['history']})
        sessions.pop(sid, None)
    else:
        next_question = call_llm(
            session['api_key'],
            f"Ask a different interview question for {session['job_role']}. Return only the question.",
            "You are an interviewer.",
            session['provider']
        )
        response = f"{feedback} Next question: {next_question}"
        emit('ai_speak', {'text': response})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return {'status': 'healthy', 'message': 'Voice AI Interviewer is running'}

if __name__ == '__main__':
    print("=" * 60)
    print("✅ Voice AI Interviewer - Multiple Provider Support")
    print("=" * 60)
    print("🚀 Supported Providers:")
    print("   1. GROQ (Recommended) - https://console.groq.com/keys")
    print("   2. Together AI - https://api.together.xyz/settings/api-keys")
    print("   3. OpenRouter - https://openrouter.ai/keys")
    print("   4. Perplexity - https://www.perplexity.ai/settings/api")
    print("=" * 60)
    print(f"🔗 Local: http://localhost:5000")
    print("=" * 60)
    
    # Get port from environment (for deployment)
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False)


import requests
from .utils import sanitize_input

# ------------------ GROQ ------------------
def call_groq_llm(api_key: str, user_message: str, system_prompt: str = "") -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.1-8b-instant",
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

# ------------------ TOGETHER AI ------------------
def call_together_llm(api_key: str, user_message: str, system_prompt: str = "") -> str:
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
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

# ------------------ OPENROUTER ------------------
def call_openrouter_llm(api_key: str, user_message: str, system_prompt: str = "") -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "Voice AI Interviewer"
    }
    payload = {
        "model": "meta-llama/llama-3.1-8b-instruct:free",
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

# ------------------ PERPLEXITY ------------------
def call_perplexity_llm(api_key: str, user_message: str, system_prompt: str = "") -> str:
    url = "https://api.perplexity.ai/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
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

# ------------------ MAIN DISPATCHER ------------------
def call_llm(api_key: str, user_message: str, system_prompt: str = "", provider: str = "groq") -> str:
    user_message = sanitize_input(user_message)
    system_prompt = sanitize_input(system_prompt) or "You are a helpful assistant."
    
    providers = {
        "groq": call_groq_llm,
        "together": call_together_llm,
        "openrouter": call_openrouter_llm,
        "perplexity": call_perplexity_llm
    }
    
    func = providers.get(provider.lower())
    if func:
        return func(api_key, user_message, system_prompt)
    else:
        return "Invalid provider. Choose: groq, together, openrouter, or perplexity"
    





 # Alias for compatibility with events.py
def get_llm_response(prompt: str, system_prompt: str = "", provider: str = "groq") -> str:
    """
    Unified interface for LLM calls. Uses GROQ by default.
    """
    from flask import current_app
    try:
        api_key = current_app.config.get("LLM_API_KEY")
        if not api_key:
            return "Error: LLM API key not configured."
        return call_llm(api_key, prompt, system_prompt, provider)
    except Exception as e:
        return f"LLM call failed: {str(e)[:100]}"   
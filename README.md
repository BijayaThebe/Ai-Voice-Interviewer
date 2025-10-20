
# Voice AI Interviewer
   The Voice AI Interviewer is an intelligent, voice-first application that simulates realistic job interviews using large language models (LLMs) and dynamic conversation management. Designed with a clean, modular architecture, it goes beyond simple Q&A by maintaining context, detecting inconsistencies, and generating thoughtful follow-up questions—just like a human interviewer would.

At its core, the system uses events.py as the main integration point, coordinating voice input/output, LLM responses, and real-time conversation logic. The new conversation/ module handles interview state, memory, and even simulates natural “thinking” pauses to create a more authentic experience. Meanwhile, prompt_engine.py provides carefully designed, human-like prompts that guide the AI toward engaging, relevant, and adaptive dialogue.

<img width="1066" height="896" alt="image" src="https://github.com/user-attachments/assets/93fbd0d2-b2a8-4a6e-88af-5d9b43b36155" />
<img width="767" height="839" alt="image" src="https://github.com/user-attachments/assets/dab186ce-892e-4787-a18f-76db880baa2b" />

# 🚨 Things to Remember
###  1. Render.com Deployment (Test URL Only)
   https://ai-voice-interviewer-1.onrender.com/

The hosted URL on Render.com is meant only for testing purposes.

It may be slow and might not return accurate or real-time responses.

For the best performance and full functionality, use the local setup instead.

### 2. Local Testing Requirements

To ensure smooth testing and optimal results when running locally:

✅ Use a high-performance laptop or PC (fast CPU, enough RAM).

✅ Use a good-quality microphone for accurate voice input.

✅ Avoid background noise to improve speech recognition.


## Key Features of This Architecture:
### Event-driven core:
- events.py coordinates real-time voice interaction.
### Stateful conversation:
- Memory persists across turns to enable intelligent follow-ups.
### Pluggable LLMs:
- providers.py abstracts model backends.
### Human-like pacing:
- thinking_simulator.py adds natural delays.
### Full voice pipeline:
- User → STT → LLM → TTS → user
### Secure config: 
- Secrets in .env, app config in instance/.


## 🚀 Local Project Setup

Follow the steps below to run the project locally:

### 1️⃣ Create a Virtual Environment
```bash
python -m venv .venv
```

### 2️⃣ Activate the Virtual Environment
```bash
.\.venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application
```bash
python run.py
```

## Project Architecture Structure
```mermaid
graph TD
    subgraph "Voice AI Interviewer"
        direction TB

        subgraph "Core Application (app/)"
            Events["events.py\n>Main Integration Point"] 
            Routes["routes.py"]
            LLM["llm/"]
            Conversation["conversation/\n>Interview State & Memory"]
            Templates["templates/\n>index.html"]
        end

        subgraph "LLM Module (app/llm/)"
            Providers["providers.py\n>LLM API Integration"]
            PromptEngine["prompt_engine.py\n>Human-like Prompt Templates"]
            Utils["utils.py"]
        end

        subgraph "Conversation Engine (app/conversation/)"
            Memory["memory.py\n>Tracks context,\nfollow-ups, contradictions"]
            Thinking["thinking_simulator.py\n>Simulates 'thinking' delays\n& response analysis"]
        end

        Config["instance/config.py"]
        Env[".env\n>Secrets & Config"]
        Run["run.py\n>Entry Point"]
    end

    %% Connections
    Run --> Events
    Events --> Routes
    Events --> LLM
    Events --> Conversation
    LLM --> Providers
    LLM --> PromptEngine
    LLM --> Utils
    Conversation --> Memory
    Conversation --> Thinking
    Events --> Templates
    Run --> Config
    Run --> Env
```
## Ai-Voice-Interviewer
Ai Powered Voice Interview System 
      Certainly! Below is a realistic engineering architecture diagram in Mermaid format that reflects not just the file structure, but the runtime components, data flow, and system interactions of the Voice AI Interviewer—as it would operate in a production-like environment.

This version models:

- User interaction (voice input/output),
- Web server (Flask),
- Event-driven orchestration,
- LLM integration,
- Conversation state management,
- External services (e.g., speech-to-text, text-to-speech),
- Configuration and secrets.

```mermaid
graph TD
    %% === External Actors ===
    User["User\n(Voice In/Out)"]

    %% === Frontend ===
    Frontend["Frontend\n(index.html + JS\nWebRTC/MediaRecorder)"]

    %% === Core Backend ===
    WebServer["Flask Web Server\n(run.py)"]
    Routes["routes.py\n(HTTP Endpoints)"]
    Events["events.py\n>Main Orchestrator\n(Async Event Hub)"]

    %% === Conversation Subsystem ===
    Memory["memory.py\n>Interview state,\n>follow-ups,\n>contradiction tracking"]
    Thinking["thinking_simulator.py\n>Simulated latency\n>Response planning"]

    %% === LLM Subsystem ===
    PromptEngine["prompt_engine.py\n>Human-like\n>dynamic prompts"]
    Providers["providers.py\n>LLM abstraction\n(OpenAI, etc.)"]

    %% === External Services ===
    STT["Speech-to-Text\n(e.g., Whisper API)"]
    TTS["Text-to-Speech\n(e.g., ElevenLabs)"]
    LLM["LLM Provider\n(e.g., OpenAI GPT-4)"]

    %% === Configuration ===
    Env[".env\n>Secrets\n>API keys"]
    Config["instance/config.py\n>Flask settings"]

    %% === Data Flow ===
    User -->|Voice| Frontend
    Frontend -->|WebSocket / HTTP| Routes
    Routes --> Events

    Events -->|Read/Write| Memory
    Events -->|Invoke| Thinking
    Events -->|Build prompt| PromptEngine
    PromptEngine -->|Send to| Providers
    Providers -->|Call| LLM
    LLM -->|Return| Providers
    Providers -->|Parse & return| Events

    Events -->|Send text| TTS
    TTS -->|Audio stream| Frontend
    Frontend -->|Play| User

    Frontend -->|Send audio| STT
    STT -->|Return text| Events

    WebServer --> Env
    WebServer --> Config
```

# Conclusion
      The Voice AI Interviewer delivers a realistic, voice-driven interview experience by combining dynamic conversation memory, human-like prompting, and simulated thinking behavior—all orchestrated through a clean, modular architecture. Built for extensibility and grounded in real engineering practices, it’s a practical step toward intelligent, empathetic AI interviewers.



# Voice AI Interviewer
   The Voice AI Interviewer is an intelligent, voice-first application that simulates realistic job interviews using large language models (LLMs) and dynamic conversation management. Designed with a clean, modular architecture, it goes beyond simple Q&A by maintaining context, detecting inconsistencies, and generating thoughtful follow-up questions—just like a human interviewer would.

At its core, the system uses events.py as the main integration point, coordinating voice input/output, LLM responses, and real-time conversation logic. The new conversation/ module handles interview state, memory, and even simulates natural “thinking” pauses to create a more authentic experience. Meanwhile, prompt_engine.py provides carefully designed, human-like prompts that guide the AI toward engaging, relevant, and adaptive dialogue.



## Project Setup Locally
1. Create a virtual environment:
   python -m venv .venv
   .\.venv\Scripts\activate

2. Install dependencies:
   pip install -r requirements.txt

3. Run the app:
   python run.py

## Architecture Structure

```mermaid
graph TD
    A[Voice AI Interviewer] --> B[app/]
    A --> C[instance/]
    A --> D[.env]
    A --> E[requirements.txt]
    A --> F[run.py]
    A --> G[README.md]

    B --> B1[__init__.py]
    B --> B2[routes.py]
    B --> B3[events.py\n**MAIN INTEGRATION POINT**]
    B --> B4[llm/]
    B --> B5[conversation/\n**Manages interview state & memory**]
    B --> B6[templates/]

    B4 --> B4a[__init__.py]
    B4 --> B4b[providers.py]
    B4 --> B4c[utils.py]
    B4 --> B4d[prompt_engine.py\n**Human-like prompt templates**]

    B5 --> B5a[__init__.py]
    B5 --> B5b[memory.py\nTracks context, follow-ups, contradictions]
    B5 --> B5c[thinking_simulator.py\nSimulates 'thinking' delays & analysis]

    B6 --> B6a[index.html]

    C --> C1[config.py]
```

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

=======
# Ai-Voice-Interviewer
Ai Powered Voice Interview System


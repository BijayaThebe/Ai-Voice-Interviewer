from app import create_app, socketio
import os

app = create_app()

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

    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
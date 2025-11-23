# backend/agent.py
import os
import asyncio
import json
import openai
import requests
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MURF_API_KEY = os.getenv("MURF_API_KEY")
LIVEKIT_URL = os.getenv("LIVEKIT_URL")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")

openai.api_key = OPENAI_API_KEY

# Simple in-memory order state
class CoffeeOrderState:
    def __init__(self):
        self.name = None
        self.items = []  # list of dicts: {"item": "Latte", "qty": 1}

    def add_item(self, item, qty=1):
        self.items.append({"item": item, "qty": qty})

    def summary(self):
        if not self.items:
            return "You haven't ordered anything yet."
        lines = [f"{it['qty']} x {it['item']}" for it in self.items]
        return "Your order: " + ", ".join(lines)


# --- Helpers ---
def call_gpt_for_order(text):
    """
    Call OpenAI to parse an order from user text.
    Use a small chat completion/gpt-4o-mini style call and ask for JSON output.
    """
    system = "You are a helpful assistant that extracts coffee orders (item and qty) from user text. Only output JSON like: {\"item\":\"Latte\",\"qty\":2} or {\"none\":true} if no order."
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": text}
        ],
        max_tokens=150,
        temperature=0
    )
    content = resp.choices[0].message["content"].strip()
    # Try to parse JSON inside content (robust)
    try:
        # If model returns plain JSON, parse it
        parsed = json.loads(content)
        return parsed
    except Exception:
        # Try to find a JSON substring
        for start in range(len(content)):
            try:
                sub = content[start:]
                parsed = json.loads(sub)
                return parsed
            except:
                continue
    return {"none": True}

def speak_with_murf(text):
    """
    Use Murf Falcon HTTP API to synthesize speech.
    This example writes response.mp3 and returns filename.
    """
    url = "https://api.murf.ai/v1/speech/generate"  # hypothetical endpoint format
    headers = {
        "accept": "audio/mpeg",
        "Content-Type": "application/json",
        "api-key": MURF_API_KEY
    }
    payload = {
        "voiceId": "falcon",
        "text": text,
        "format": "mp3"
    }
    r = requests.post(url, json=payload, headers=headers, timeout=30)
    if r.status_code == 200:
        out = "response.mp3"
        with open(out, "wb") as f:
            f.write(r.content)
        return out
    else:
        print("Murf TTS failed:", r.status_code, r.text)
        return None

# --- Minimal mock event loop to simulate an agent (replace with LiveKit agent loop if using their SDK) ---
async def main_loop():
    print("Starbucks-style Barista Agent (mock). Type text input to simulate a user speaking.")
    state = CoffeeOrderState()

    while True:
        text = input("\nYou: ").strip()
        if not text:
            continue

        # Name detection
        if state.name is None:
            # ask name in a friendly way
            if "my name is" in text.lower() or "i am" in text.lower():
                # quick naive name extraction
                parts = text.split()
                state.name = parts[-1].capitalize()
                reply = f"Nice to meet you, {state.name}! What can I get you today?"
                print("Barista:", reply)
                speak_with_murf(reply)
                continue
            else:
                # proceed, but we can ask for name later
                pass

        # Check for summary or done
        if text.lower() in ["summary", "order summary"]:
            reply = state.summary()
            print("Barista:", reply)
            speak_with_murf(reply)
            continue
        if text.lower() in ["done", "that's all", "finish", "complete", "i'm done"]:
            reply = "Thanks for visiting Starbucks Café! Your order will be ready shortly. ☕"
            print("Barista:", reply)
            speak_with_murf(reply)
            break

        # Ask GPT to extract order
        parsed = call_gpt_for_order(text)
        if parsed.get("none"):
            reply = "Sorry, I couldn't catch the order. Could you please repeat the item and quantity?"
            print("Barista:", reply)
            speak_with_murf(reply)
            continue

        item = parsed.get("item")
        qty = int(parsed.get("qty", 1))
        state.add_item(item, qty)
        reply = f"Great — I've added {qty} {item}(s) to your order. Anything else?"
        print("Barista:", reply)
        speak_with_murf(reply)

if __name__ == "__main__":
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        print("Agent stopped.")

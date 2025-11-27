# agent.py

import os
from dotenv import load_dotenv
from livekit import agents
from utils.fraud_patterns import FRAUD_KEYWORDS
from state import FraudState
from fraud_task import FraudTask
from db import init_db
import openai

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


async def main():
    init_db()

    state = FraudState()
    fraud_tool = FraudTask(state)

    instructions = f"""
You are a serious and concise Fraud Alert Voice Agent for a bank like HDFC.

Your goals:
- Listen to what the caller says.
- If they describe anything suspicious (OTP sharing, unknown transactions, scam calls, etc.),
  you MUST call the `fraud_task` tool with:
  - user_id: some identifier string (e.g., "user-001")
  - description: short description of the suspicious activity in plain English.
- After the tool runs, reassure the user and suggest safe next steps.
- If they just ask general questions, calmly explain fraud prevention best practices.

Fraud topics to pay attention to (examples): {FRAUD_KEYWORDS}

Keep responses short, clear, and non-technical.
Never ask the user to share OTP, CVV, PIN, passwords, or full card numbers.
"""

    async with agents.RealtimeAgent(
        url=os.getenv("LIVEKIT_URL"),
        api_key=os.getenv("LIVEKIT_API_KEY"),
        api_secret=os.getenv("LIVEKIT_API_SECRET"),
        model="gpt-4o-realtime",
        voice="falcon",  # Murf Falcon TTS on LiveKit side
        instructions=instructions,
        tools=[fraud_tool],
    ) as agent:
        print("🚨 Fraud Alert Voice Agent (HDFC style) is LIVE")

        # Simple console-style loop; with `python agent.py console` in LiveKit it will be voice.
        while True:
            msg = await agent.receive_text()
            text = msg.text.strip()

            lower = text.lower()
            if lower in ["bye", "exit", "quit", "stop", "thank you"]:
                await agent.send_text("Thank you for contacting us. Stay safe and vigilant. 👋")
                break

            if "summary" in lower:
                await agent.send_text(state.summary())
                continue

            # If message contains any fraud keyword, call the tool
            if any(k in lower for k in FRAUD_KEYWORDS):
                await agent.call_tool(
                    "fraud_task",
                    {
                        "user_id": "user-001",
                        "description": text,
                    },
                )
            else:
                # General guidance fallback
                await agent.send_text(
                    "I am monitoring for suspicious activity. "
                    "Tell me if you received any unknown OTPs, scam calls, or unauthorized transactions."
                )


if __name__ == "__main__":
    # For local testing with console mode (per LiveKit examples):
    #   python agent.py console
    agents.run(main())

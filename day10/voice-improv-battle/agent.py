import os
from livekit import agents
from dotenv import load_dotenv
import openai

from state import ImprovState
from improv_task import ImprovTask

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


async def main():
    state = ImprovState()
    improv_tool = ImprovTask(state)

    instructions = """
You are a **Voice Improv Battle Partner**.

Your job:
- Start fun improv scenes.
- Continue the story after the user's line.
- Match the energy (funny, dramatic, chaotic, etc.).
- Keep replies short (1–2 sentences).
- Encourage the user to keep going.
- End the scene gracefully when asked.

Tool usage:
- When user says things like "start", "start improv", "let's begin" →
  call improv_task with {"action": "start"}.

- While a scene is active, for every user line →
  call improv_task with {"action": "continue", "line": "<user text>"}.

- When user says "end", "stop", "wrap up" →
  call improv_task with {"action": "end"}.

Always stay in character as a high-energy improv partner.
"""

    async with agents.RealtimeAgent(
        url=os.getenv("LIVEKIT_URL"),
        api_key=os.getenv("LIVEKIT_API_KEY"),
        api_secret=os.getenv("LIVEKIT_API_SECRET"),
        model="gpt-4o-realtime",
        voice="falcon",  # Murf Falcon TTS
        instructions=instructions,
        tools=[improv_tool],
    ) as agent:
        print("🎭 Voice Improv Battle Agent is LIVE!")

        while True:
            msg = await agent.receive_text()
            text = msg.text.lower()

            # End conversation completely
            if any(x in text for x in ["quit challenge", "exit agent"]):
                await agent.send_text("Exiting the improv agent. Bye! 👋")
                break

            # Map plain user text to tool actions
            if any(x in text for x in ["start", "begin", "improv"]):
                await agent.call_tool("improv_task", {"action": "start"})
            elif any(x in text for x in ["end", "stop", "wrap up"]):
                await agent.call_tool("improv_task", {"action": "end"})
                break
            else:
                await agent.call_tool(
                    "improv_task",
                    {"action": "continue", "line": msg.text},
                )


if __name__ == "__main__":
    agents.run(main())

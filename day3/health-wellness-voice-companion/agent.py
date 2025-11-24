import os
from livekit import agents
from dotenv import load_dotenv
import openai

from state import WellnessState
from wellness_task import WellnessTask
from utils.tips import DAILY_TIPS

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

async def main():

    state = WellnessState()
    wellness_tool = WellnessTask(state)

    instructions = f"""
You are a Health & Wellness Voice Companion.

What you can track:
- Water intake
- Steps
- Workouts

TOOLS:
wellness_task:
- add_water(amount)
- add_steps(count)
- add_workout(workout)
- summary()

If a user asks for a tip, respond with a wellness tip.
"""

    async with agents.RealtimeAgent(
        url=os.getenv("LIVEKIT_URL"),
        api_key=os.getenv("LIVEKIT_API_KEY"),
        api_secret=os.getenv("LIVEKIT_API_SECRET"),
        model="gpt-4o-realtime",
        voice="falcon",
        instructions=instructions,
        tools=[wellness_tool],
    ) as agent:

        print("🧘 Wellness Agent Running...")

        while True:
            msg = await agent.receive_text()

            if msg.text.lower() == "tip":
                await agent.send_text("✨ Wellness Tip: " + DAILY_TIPS.get_random())
                continue

            if msg.text.lower() in ["bye", "stop", "exit"]:
                await agent.send_text("Goodbye! Stay healthy 💚")
                break


if __name__ == "__main__":
    agents.run(main())

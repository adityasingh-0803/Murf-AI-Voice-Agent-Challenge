import os
from livekit import agents
from dotenv import load_dotenv
import openai

from state import OrderState
from order_task import OrderTask
from utils.menu import MENU
from utils.suggestions import random_suggestion

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

async def main():
    state = OrderState()
    order_tool = OrderTask(state)

    instructions = f"""
You are a Food & Grocery Ordering Voice Agent.

Your responsibilities:
- Take user orders from this grocery menu: {MENU}
- Add or remove items using order_task
- Provide suggestions
- Give cart summary on request
- Checkout when the user says 'checkout'

Available Tool Actions:
1. order_task(add_item) → requires item, qty
2. order_task(remove_item) → requires item
3. order_task(summary)

Speak like a friendly Swiggy Instamart assistant!
"""

    async with agents.RealtimeAgent(
        url=os.getenv("LIVEKIT_URL"),
        api_key=os.getenv("LIVEKIT_API_KEY"),
        api_secret=os.getenv("LIVEKIT_API_SECRET"),
        model="gpt-4o-realtime",
        voice="falcon",
        instructions=instructions,
        tools=[order_tool],
    ) as agent:

        print("🛒 Food & Grocery Ordering Agent is LIVE!")

        while True:
            msg = await agent.receive_text()
            text = msg.text.lower()

            if "suggest" in text:
                await agent.send_text(random_suggestion())
                continue

            if "checkout" in text:
                await agent.send_text(state.summary())
                await agent.send_text("Order placed! Thank you for shopping 🛒✨")
                break

            await agent.send_text("Tell me what to add or remove from your cart!")
            

if __name__ == "__main__":
    agents.run(main())

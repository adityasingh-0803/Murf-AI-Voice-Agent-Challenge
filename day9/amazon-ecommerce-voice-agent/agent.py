import os
from livekit import agents
from dotenv import load_dotenv
import openai

from state import CommerceState
from commerce_task import CommerceTask
from utils.products import PRODUCTS
from utils.suggestions import random_suggestion

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


async def main():
    state = CommerceState()
    commerce_tool = CommerceTask(state, PRODUCTS)

    instructions = f"""
You are an E-commerce Voice Agent for an Amazon-style store.

Your job:
- Help the user browse products
- Lookup prices
- Add/remove items from cart using SKUs
- Read out cart summary
- Guide them to checkout

You have access to one tool: commerce_task

Tool actions:
- add: add an item to cart → needs "sku" and optional "qty"
- remove: remove an item from cart → needs "sku"
- lookup: lookup price & details → needs "sku"
- summary: read the current cart summary

Product catalog (for reference):
{PRODUCTS}

If the user says things like:
- "Add Echo Dot to my cart" → first infer SKU then call tool with action "add"
- "Remove the T-shirt" → infer SKU and call "remove"
- "What's the price of the headphones?" → infer SKU and call "lookup"
- "What's in my cart?" → call "summary"
- "Checkout" → call "summary", then say a final confirmation line.

Always respond as a friendly Amazon-style shopping assistant.
Keep answers short and clear.
"""

    async with agents.RealtimeAgent(
        url=os.getenv("LIVEKIT_URL"),
        api_key=os.getenv("LIVEKIT_API_KEY"),
        api_secret=os.getenv("LIVEKIT_API_SECRET"),
        model="gpt-4o-realtime",
        voice="falcon",          # Murf Falcon TTS
        instructions=instructions,
        tools=[commerce_tool],
    ) as agent:

        print("🛍️ Amazon-style E-commerce Voice Agent LIVE!")

        while True:
            msg = await agent.receive_text()
            text = msg.text.lower()

            if "suggest" in text or "recommend" in text:
                await agent.send_text(random_suggestion())
                continue

            if "checkout" in text:
                # Final summary + goodbye
                await agent.send_text(state.summary(PRODUCTS))
                await agent.send_text(
                    "Your order has been placed in this demo flow. "
                    "Thanks for shopping with our AI assistant! 🛍️"
                )
                break

            # Let the model handle understanding & tool calls
            await agent.send_text(
                "Tell me what you're looking for, or ask me to add/remove items from your cart."
            )


if __name__ == "__main__":
    agents.run(main())

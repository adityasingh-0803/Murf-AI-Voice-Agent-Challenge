import os
from livekit import agents, rtc
from dotenv import load_dotenv
import openai
import json
from utils.menu import COFFEE_MENU

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MURF_API_KEY = os.getenv("MURF_API_KEY")

openai.api_key = OPENAI_API_KEY


class CoffeeOrderState:
    def __init__(self):
        self.order = []
        self.user_name = None

    def add_item(self, item, qty):
        self.order.append({"item": item, "qty": qty})

    def summary(self):
        if not self.order:
            return "You have not ordered anything yet."
        s = "Here is your order summary:\n"
        for i in self.order:
            s += f"- {i['qty']} × {i['item']}\n"
        return s


async def main():
    state = CoffeeOrderState()

    async def agent_callback(event: rtc.Event):
        pass  # No WebRTC event logic needed for model-only agent

    # ------ REALTIME AGENT -------
    async with agents.RealtimeAgent(
        url=os.getenv("LIVEKIT_URL"),
        api_key=os.getenv("LIVEKIT_API_KEY"),
        api_secret=os.getenv("LIVEKIT_API_SECRET"),
        on_event=agent_callback,
        voice="falcon",          # Murf Falcon TTS
        model="gpt-4o-realtime", # OpenAI Realtime Model
        instructions=f"""
You are a friendly and enthusiastic Coffee Shop Barista. Keep responses short and sweet.

Your tasks:
- Ask name (once)
- Take coffee orders from menu: {json.dumps(COFFEE_MENU)}
- Clarify size, quantity if missing
- Add items to an internal Python state
- If user says "summary", read back items
- When they say "done", close the order politely

ALWAYS stay in character as a Barista who LOVES coffee.
""",
    ) as agent:

        print("☕ Coffee Barista Agent is LIVE!")
        print("Speak to your barista...")

        while True:
            msg = await agent.receive_text()

            if msg.text.lower() == "summary":
                await agent.send_text(state.summary())
                continue

            if msg.text.lower() in ["done", "complete", "finish"]:
                await agent.send_text("Thanks for visiting our coffee shop! Have a great day ☕✨")
                break

            # Process order using GPT
            order_struct = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Extract coffee order and quantity."},
                    {"role": "user", "content": msg.text},
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "coffee_order",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "item": {"type": "string"},
                                "qty": {"type": "integer"},
                            },
                            "required": ["item", "qty"],
                        },
                    },
                }
            )

            try:
                item = order_struct.choices[0].message["parsed"]["item"]
                qty = order_struct.choices[0].message["parsed"]["qty"]

                if item.lower() in COFFEE_MENU:
                    state.add_item(item, qty)
                    await agent.send_text(f"Great! Added {qty} × {item} to your order.")
                else:
                    await agent.send_text("Sorry, that item is not on the menu.")
            except:
                await agent.send_text("Got it! Tell me your order again?")

        print("Agent ended.")


if __name__ == "__main__":
    agents.run(main())

from livekit.agents import llm

class OrderTask(llm.Task):
    def __init__(self, state):
        self.state = state

    async def run(self, input, ctx):
        action = input["action"]
        item = input.get("item")
        qty = input.get("qty", 1)

        if action == "add_item":
            self.state.add_item(item, qty)
            await ctx.send_text(f"Added {qty} × {item} to your cart.")

        elif action == "remove_item":
            self.state.remove_item(item)
            await ctx.send_text(f"Removed {item} from your cart.")

        elif action == "summary":
            await ctx.send_text(self.state.summary())

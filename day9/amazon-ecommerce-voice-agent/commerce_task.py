from livekit.agents import llm

class CommerceTask(llm.Task):
    """
    Tool used by the model to perform commerce actions:
    - add
    - remove
    - lookup
    - summary
    """

    def __init__(self, state, catalog):
        self.state = state
        self.catalog = catalog

    async def run(self, input, ctx):
        action = input["action"]

        if action == "add":
            sku = input["sku"]
            qty = int(input.get("qty", 1))
            if sku not in self.catalog:
                await ctx.send_text("That SKU does not exist in the catalog.")
                return
            self.state.add_item(sku, qty)
            item = self.catalog[sku]
            await ctx.send_text(
                f"Added {qty} × {item['name']} to your cart."
            )

        elif action == "remove":
            sku = input["sku"]
            if sku not in self.catalog:
                await ctx.send_text("That SKU does not exist in the catalog.")
                return
            self.state.remove_item(sku)
            item = self.catalog[sku]
            await ctx.send_text(f"Removed {item['name']} from your cart.")

        elif action == "lookup":
            sku = input["sku"]
            item = self.catalog.get(sku)
            if not item:
                await ctx.send_text("I couldn't find that product in the catalog.")
                return
            await ctx.send_text(
                f"{item['name']} costs ₹{item['price']} in the {item['category']} category."
            )

        elif action == "summary":
            await ctx.send_text(self.state.summary(self.catalog))

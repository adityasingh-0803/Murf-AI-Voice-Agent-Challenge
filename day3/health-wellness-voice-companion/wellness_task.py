from livekit.agents import llm

class WellnessTask(llm.Task):
    def __init__(self, state):
        self.state = state

    async def run(self, input, ctx):
        action = input.get("action")

        if action == "add_water":
            amount = input["amount"]
            self.state.add_water(amount)
            await ctx.send_text(f"Added {amount} ml of water 💧")

        elif action == "add_steps":
            count = input["count"]
            self.state.add_steps(count)
            await ctx.send_text(f"Logged {count} steps 👣 Keep going!")

        elif action == "add_workout":
            workout = input["workout"]
            self.state.add_workout(workout)
            await ctx.send_text(f"Added {workout} workout 💪")

        elif action == "summary":
            await ctx.send_text("Here is your wellness summary:\n" + self.state.daily_summary())

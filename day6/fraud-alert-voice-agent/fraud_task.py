# fraud_task.py

from livekit.agents import llm
from state import FraudState
from db import insert_alert
from utils.fraud_patterns import SAFETY_TIPS
import random


class FraudTask(llm.Task):
    """
    Tool: logs a suspicious event for a specific user,
    updates in-memory state + SQLite DB, and returns a short response.
    """

    def __init__(self, state: FraudState):
        self.state = state

    async def run(self, input, ctx):
        user_id = input.get("user_id", "user-001")
        description = input.get("description", "Suspicious activity")

        self.state.set_user(user_id)
        self.state.add_event(description)
        insert_alert(user_id, description)

        tip = random.choice(SAFETY_TIPS)

        await ctx.send_text(
            f"⚠️ Fraud alert recorded for {user_id}.\n"
            f"Details: {description}\n\n"
            f"Safety tip: {tip}"
        )

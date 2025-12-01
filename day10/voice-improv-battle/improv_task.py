from livekit.agents import llm
import openai
import random
from utils.scenes import SCENES


class ImprovTask(llm.Task):
    def __init__(self, state):
        self.state = state

    async def run(self, input, ctx):
        action = input.get("action")

        # Start a new random scene
        if action == "start":
            selected = random.choice(SCENES)
            self.state.start_scene(
                selected["scene"],
                selected["characters"],
                selected["mood"],
            )

            await ctx.send_text(
                "🎭 Voice Improv Battle begins!\n"
                f"Setting: {selected['scene']}\n"
                f"Characters: {', '.join(selected['characters'])}\n"
                f"Mood: {selected['mood']}\n\n"
                "You start! Say the first line of the scene. 🎙️"
            )
            return

        # Continue the scene based on user's line
        if action == "continue":
            user_line = input.get("line", "")

            if not self.state.scene:
                await ctx.send_text("No active scene yet. Say 'start improv' to begin!")
                return

            prompt = f"""
Continue this improv scene with creativity.

Scene description: {self.state.scene}
Characters involved: {', '.join(self.state.characters)}
Current mood: {self.state.mood}

User's latest line: "{user_line}"

You are the AI improv partner. Reply with the **next line only** in the conversation.
Keep it short (1–2 sentences), high energy, and build the story forward.
Avoid narration like 'he said / she said', just speak as one of the characters.
"""

            resp = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
            )

            next_line = resp.choices[0].message.content
            self.state.update()

            await ctx.send_text(next_line)
            return

        # End scene
        if action == "end":
            if not self.state.scene:
                await ctx.send_text("There is no active scene to end.")
                return

            self.state.end()
            await ctx.send_text(
                "🎤 Improv Battle wrapped up! That was fun. "
                "Thanks for playing, superstar! 🌟"
            )
            return

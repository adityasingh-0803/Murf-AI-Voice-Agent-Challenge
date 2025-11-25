from livekit.agents import llm
import openai

class QuestionTask(llm.Task):
    def __init__(self, state):
        self.state = state

    async def run(self, input, ctx):
        topic = input["topic"]

        prompt = f"""
        Generate one Active Recall question on: {topic}.
        Respond in JSON:
        {{
            "question": "...",
            "answer": "..."
        }}
        """

        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )

        parsed = ctx.parse_json(resp.choices[0].message["content"])

        self.state.set_question(parsed["question"], parsed["answer"])

        await ctx.send_text(f"Here’s your question:\n{parsed['question']}")

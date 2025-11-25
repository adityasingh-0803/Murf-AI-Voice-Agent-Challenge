from livekit.agents import llm
import openai

class EvaluationTask(llm.Task):
    def __init__(self, state):
        self.state = state

    async def run(self, input, ctx):
        user_answer = input["user_answer"]
        correct = self.state.correct_answer

        prompt = f"""
        Compare:
        User: {user_answer}
        Correct: {correct}

        JSON:
        {{
            "is_correct": true/false,
            "explanation": "..."
        }}
        """

        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )

        data = ctx.parse_json(resp.choices[0].message["content"])

        # Update score
        self.state.update_score(data["is_correct"])

        if data["is_correct"]:
            await ctx.send_text("Correct! 🎉 Great job!")
        else:
            await ctx.send_text("Not quite. Here's why:\n" + data["explanation"])

        # Handoff for next question
        await ctx.handoff(tool="question_task", input={"topic": self.state.topic})

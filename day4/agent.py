import os
from livekit import agents
from dotenv import load_dotenv
import openai

from state import RecallState
from question_task import QuestionTask
from evaluation_task import EvaluationTask

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

async def main():
    state = RecallState()
    question_tool = QuestionTask(state)
    eval_tool = EvaluationTask(state)

    instructions = """
You are an Active Recall Tutor.

When user says:
"start on <topic>" → call question_task(topic)
When user answers → call evaluation_task(user_answer)

TOOLS:
- question_task(topic)
- evaluation_task(user_answer)

Be encouraging, concise, and tutor-like.
"""

    async with agents.RealtimeAgent(
        url=os.getenv("LIVEKIT_URL"),
        api_key=os.getenv("LIVEKIT_API_KEY"),
        api_secret=os.getenv("LIVEKIT_API_SECRET"),
        model="gpt-4o-realtime",
        voice="falcon",  # MURF FALCON TTS
        instructions=instructions,
        tools=[question_tool, eval_tool],
    ) as agent:

        print("📘 Active Recall Tutor is LIVE!")

        while True:
            msg = await agent.receive_text()
            text = msg.text.lower().strip()

            if text.startswith("start on"):
                topic = text.replace("start on", "").strip()
                state.set_topic(topic)
                await agent.call_tool("question_task", {"topic": topic})
                continue

            elif state.current_question:
                await agent.call_tool("evaluation_task", {"user_answer": msg.text})
                continue

            elif text in ["stop", "bye", "exit"]:
                await agent.send_text("Goodbye! Keep learning 📘✨")
                break


if __name__ == "__main__":
    agents.run(main())

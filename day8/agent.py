import os
from livekit import agents
from dotenv import load_dotenv
import openai

from state import GameState
from game_task import GameTask

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


async def main():
    state = GameState()
    game_tool = GameTask(state)

    instructions = """
You are a fun, high-energy VOICE GAME MASTER.

You support two games:
- 'trivia'
- 'riddle'

User commands:
- "start trivia"  → start trivia game
- "start riddle"  → start riddle game
- When the user answers, you should check their answer.
- The user can say "quit" or "end game" to stop.

TOOLS:
You have one tool: game_task

Use it in these ways:

1) To ask a new question:
   game_task with:
   {
     "mode": "ask",
     "game": "trivia" or "riddle"
   }

2) To check a user's answer:
   game_task with:
   {
     "mode": "check",
     "game": current_game,
     "user_answer": "<user's answer>"
   }

Keep responses short, playful and game-like.
After each round, tell the user their score.
"""

    async with agents.RealtimeAgent(
        url=os.getenv("LIVEKIT_URL"),
        api_key=os.getenv("LIVEKIT_API_KEY"),
        api_secret=os.getenv("LIVEKIT_API_SECRET"),
        voice="falcon",  # Murf Falcon TTS
        model="gpt-4o-realtime",
        instructions=instructions,
        tools=[game_tool],
    ) as agent:

        print("🎮 Voice Game Master is LIVE!")
        await agent.send_text(
            "Welcome to Voice Game Master! Say 'start trivia' or 'start riddle' to begin."
        )

        while True:
            msg = await agent.receive_text()
            text = (msg.text or "").lower().strip()

            if any(kw in text for kw in ["quit", "exit", "end game", "stop game"]):
                state.end_game()
                await agent.send_text("Game ended. Thanks for playing! 🎮")
                break

            # Start trivia
            if "start trivia" in text:
                state.start_game("trivia")
                await agent.call_tool("game_task", {"mode": "ask", "game": "trivia"})
                continue

            # Start riddle
            if "start riddle" in text:
                state.start_game("riddle")
                await agent.call_tool("game_task", {"mode": "ask", "game": "riddle"})
                continue

            # If in a game, treat input as answer
            if state.game_active:
                await agent.call_tool(
                    "game_task",
                    {
                        "mode": "check",
                        "game": state.current_game,
                        "user_answer": text,
                    },
                )
                # After checking, automatically ask next question
                await agent.call_tool(
                    "game_task",
                    {"mode": "ask", "game": state.current_game},
                )
            else:
                await agent.send_text(
                    "Say 'start trivia' or 'start riddle' to play a game!"
                )


if __name__ == "__main__":
    agents.run(main())

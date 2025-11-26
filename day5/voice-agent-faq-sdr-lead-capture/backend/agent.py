from livekit.agents import AutoAgent, llm
from faq_store import FAQStore
from tools import create_lead

faq_store = None

SYSTEM_PROMPT = """
You are Nova, an SDR for NovaCRM.

Your job:
1. Answer FAQs using the provided FAQ context.
2. Ask 1–2 discovery questions.
3. When the user shows interest, capture a lead using the create_lead tool.
4. Keep responses short and conversational.
5. Never guess details outside the FAQ.
"""

def prewarm():
    global faq_store
    embed_model = llm.GeminiEmbeddingModel(model="text-embedding-004")
    faq_store = FAQStore("backend/data/nova_faq.json", embed_model)
    print("FAQ store loaded ✔")


def handler(ctx: AutoAgent.Context):
    user_msg = ctx.input_text

    # Search top-matching FAQ answers
    faqs = faq_store.search(user_msg, top_k=3)
    faq_context = "\n".join(
        [f"Q: {f.question}\nA: {f.answer}" for f in faqs]
    )

    # Build final prompt
    ctx.output_text = (
        SYSTEM_PROMPT
        + "\n\nRelevant FAQs:\n"
        + faq_context
        + "\n\nUser message: "
        + user_msg
    )


# Build agent
agent = AutoAgent(
    system_instructions=SYSTEM_PROMPT,
    tools=[create_lead],
    prewarm=prewarm,
    handler=handler
)

if __name__ == "__main__":
    agent.run()

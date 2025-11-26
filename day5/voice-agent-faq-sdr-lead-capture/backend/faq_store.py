import json
import numpy as np
from dataclasses import dataclass
from livekit.agents import llm

@dataclass
class FAQItem:
    id: str
    question: str
    answer: str
    embedding: np.ndarray


class FAQStore:
    def __init__(self, path: str, embed_model: llm.EmbeddingModel):
        self.embed_model = embed_model
        self.faqs = []
        self._load(path)

    def _load(self, path: str):
        with open(path, "r") as f:
            data = json.load(f)

        texts = [f"Q: {d['question']} A: {d['answer']}" for d in data]
        embeddings = self.embed_model.embed(texts)

        for d, e in zip(data, embeddings):
            self.faqs.append(
                FAQItem(
                    id=d["id"],
                    question=d["question"],
                    answer=d["answer"],
                    embedding=np.array(e)
                )
            )

    def search(self, query: str, top_k: int = 3):
        q_emb = np.array(self.embed_model.embed([query])[0])
        scored = []

        for faq in self.faqs:
            sim = float(
                np.dot(q_emb, faq.embedding)
                / ((np.linalg.norm(q_emb) * np.linalg.norm(faq.embedding)) + 1e-9)
            )
            scored.append((sim, faq))

        scored.sort(reverse=True, key=lambda x: x[0])
        return [f for _, f in scored[:top_k]]

# state.py

class FraudState:
    def __init__(self):
        self.user_id = None
        self.suspicious_events = []

    def set_user(self, user_id: str):
        self.user_id = user_id

    def add_event(self, event: str):
        self.suspicious_events.append(event)

    def summary(self) -> str:
        if not self.suspicious_events:
            return "No suspicious activity detected for this account."

        lines = [f"Fraud Activity Summary for {self.user_id or 'current user'}:"]
        for idx, e in enumerate(self.suspicious_events, start=1):
            lines.append(f"{idx}. {e}")
        return "\n".join(lines)

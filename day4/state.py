class RecallState:
    def __init__(self):
        self.topic = None
        self.current_question = None
        self.correct_answer = None
        self.score = 0
        self.total_questions = 0
        self.started = False

    def set_topic(self, topic):
        self.topic = topic
        self.started = True

    def set_question(self, q, a):
        self.current_question = q
        self.correct_answer = a
        self.total_questions += 1

    def update_score(self, correct):
        if correct:
            self.score += 1

    def summary(self):
        return (
            f"Topic: {self.topic}\n"
            f"Questions attempted: {self.total_questions}\n"
            f"Correct answers: {self.score}\n"
        )

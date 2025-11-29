class GameState:
    def __init__(self):
        self.game_active = False
        self.current_game = None
        self.score = 0
        self.total_rounds = 0
        self.expected_answer = None

    def start_game(self, game_name: str):
        self.current_game = game_name
        self.game_active = True
        self.score = 0
        self.total_rounds = 0
        self.expected_answer = None

    def end_game(self):
        self.game_active = False
        self.current_game = None
        self.expected_answer = None

    def record_round(self):
        self.total_rounds += 1

    def correct_answer(self):
        self.score += 1

    def summary(self) -> str:
        if self.total_rounds == 0:
            return "No rounds played yet."
        return f"Score: {self.score} / {self.total_rounds}"

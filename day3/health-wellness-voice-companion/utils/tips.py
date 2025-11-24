import random

TIPS = [
    "Drink a glass of water every hour.",
    "Take a quick 5-minute stretch break!",
    "A short walk can boost your mood.",
    "Practice deep breathing for 60 seconds.",
]

class DAILY_TIPS:
    @staticmethod
    def get_random():
        return random.choice(TIPS)

import random

SUGGESTIONS = [
    "Bananas are fresh today! Want to add some?",
    "Would you like to add bread?",
    "We have a discount on paneer today!",
    "Coffee is on sale today!"
]

def random_suggestion():
    return random.choice(SUGGESTIONS)

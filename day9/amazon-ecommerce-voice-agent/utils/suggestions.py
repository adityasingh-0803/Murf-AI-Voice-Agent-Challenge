import random

SUGGESTIONS = [
    "Customers who bought headphones also looked at smart speakers.",
    "Running shoes are selling fast today!",
    "Fashion deals are live on T-shirts.",
    "Home & Living products have lightning deals right now.",
]

def random_suggestion():
    return random.choice(SUGGESTIONS)

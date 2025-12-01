class ImprovState:
    def __init__(self):
        self.scene = None
        self.characters = []
        self.mood = "neutral"
        self.turns = 0
        self.ended = False

    def start_scene(self, scene, characters, mood):
        self.scene = scene
        self.characters = characters
        self.mood = mood
        self.turns = 0
        self.ended = False

    def update(self, mood=None):
        self.turns += 1
        if mood:
            self.mood = mood

    def end(self):
        self.ended = True

class WellnessState:
    def __init__(self):
        self.water_intake_ml = 0
        self.steps = 0
        self.workouts = []

    def add_water(self, amount):
        self.water_intake_ml += amount

    def add_steps(self, count):
        self.steps += count

    def add_workout(self, workout):
        self.workouts.append(workout)

    def daily_summary(self):
        return (
            f"🥤 Water: {self.water_intake_ml} ml\n"
            f"👣 Steps: {self.steps}\n"
            f"💪 Workouts: {', '.join(self.workouts) if self.workouts else 'None'}"
        )

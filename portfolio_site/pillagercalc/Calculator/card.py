class Card:
    def __init__(self, effect, cost):
        self.cost = cost
        self.name = effect
        self.is_spell = False
        self.is_combo = False
        self.is_targeted = False
        if effect in ("tenwu", "step"):
            self.is_targeted = True
        if effect in ("potion", "prep", "coin", "step"):
            self.is_spell = True
        if effect in ("scabbs", "pillager"):
            self.is_combo = True

    def set_cost_to_default(self):
        if self.name in ("prep", "coin", "step"):
            self.cost = 0
        elif self.name in ("foxy", "tenwu", "dancer"):
            self.cost = 2
        elif self.name in ("scabbs", "shark", "potion"):
            self.cost = 4
        elif self.name == "pillager":
            self.cost = 6

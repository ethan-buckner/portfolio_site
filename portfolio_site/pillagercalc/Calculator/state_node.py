from . import card


class StateNode:
    def __init__(self, explored, previous, played, targeted, mana, cards_played,
                 next_combo_reduction, next_spell_reduction, next_card_reduction, next_next_card_reduction,
                 life_total, hand, battlefield):
        self.explored = explored
        self.previous = previous
        self.played = played
        self.targeted = targeted
        self.mana = int(mana)
        self.cards_played = int(cards_played)
        self.next_combo_reduction = next_combo_reduction
        self.next_spell_reduction = next_spell_reduction
        self.next_card_reduction = next_card_reduction
        self.next_next_card_reduction = next_next_card_reduction
        self.life_total = int(life_total)
        self.hand = hand
        self.battlefield = battlefield

    @classmethod
    def from_parent(cls, parent, last_played, last_target):
        previous = parent
        played = last_played
        targeted = last_target
        cards_played = previous.cards_played
        life_total = previous.life_total
        modifiedCost = played.cost - (
                (previous.next_combo_reduction if played.is_combo else 0) +
                (previous.next_spell_reduction if played.is_spell else 0) +
                previous.next_card_reduction)
        if modifiedCost < 0:
            modifiedCost = 0
        mana = parent.mana - modifiedCost
        hand = parent.hand.copy()
        hand.remove(played)
        battlefield = parent.battlefield.copy()
        shark = False
        for minion in battlefield:
            if minion.name == "shark":
                shark = True
        target = None
        if last_target != "untargeted":
            for minion in battlefield:
                if minion.name == targeted:
                    target = minion
        next_combo_reduction = 0 if played.is_combo else previous.next_combo_reduction
        next_spell_reduction = 0 if played.is_spell else previous.next_spell_reduction
        next_card_reduction = previous.next_next_card_reduction
        next_next_card_reduction = 0
        if played.name == "pillager":
            life_total -= cards_played * (2 if shark else 1)
        elif played.name == "scabbs":
            if cards_played > 0:
                next_card_reduction = 6 if shark else 3
                next_next_card_reduction = 6 if shark else 3
        elif played.name == "foxy":
            next_combo_reduction += 4 if shark else 2
        elif played.name == "step":
            battlefield.remove(target)
            new_card = card.Card(target.name, 0)
            new_card.set_cost_to_default()
            new_card.cost -= 2
            hand.append(new_card)
        elif played.name == "prep":
            next_spell_reduction = 2
        elif played.name == "potion":
            for minion in battlefield:
                if len(hand) >= 10:
                    break
                hand.append(card.Card(minion.name, 1))
        elif played.name == "tenwu":
            battlefield.remove(target)
            hand.append(card.Card(target.name, 1))
        elif played.name == "dancer":
            reps = 2 if shark else 1
            for i in range(reps):
                if len(hand) < 10:
                    hand.append(card.Card("coin", 0))
        elif played.name == "coin":
            mana += 1
        cards_played += 1
        if not played.is_spell:
            battlefield.append(played)
        return cls(False, previous, played, targeted, int(mana), cards_played, next_combo_reduction,
                   next_spell_reduction, next_card_reduction, next_next_card_reduction,
                   life_total, hand, battlefield)

    def generate_children(self):
        child_list = []
        for choice in self.hand:
            if choice.name == "coin" and self.next_spell_reduction == 0 and self.next_card_reduction == 0:
                child_list.append(self.from_parent(self, choice, "untargeted"))
                return child_list
            modified_cost = choice.cost - ((self.next_combo_reduction if choice.is_combo else 0)
                                           + (self.next_spell_reduction if choice.is_spell else 0)
                                           + self.next_card_reduction)
            if modified_cost < 0:
                modified_cost = 0
            if modified_cost <= int(self.mana):
                if choice.is_spell or len(self.battlefield) < 7:
                    if choice.is_targeted:
                        for minion in self.battlefield:
                            child_list.append(self.from_parent(self, choice, minion.name))
                    else:
                        child_list.append(self.from_parent(self, choice, "untargeted"))
        return child_list

    def backtrack(self):
        out_string = ""
        selected = self
        while selected is not None and selected.played is not None:
            if selected.targeted != "untargeted":
                out_string = selected.played.name + "(" + selected.targeted + ") " + out_string
            else:
                out_string = selected.played.name + " " + out_string
            selected = selected.previous
        return out_string

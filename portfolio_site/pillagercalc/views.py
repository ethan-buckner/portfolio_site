from django.http import HttpResponse
from django.shortcuts import render
from .Calculator import card, game_tree, state_node


# Create your views here.

def index(request):
    return render(request, 'pillagercalc/about.html')


def input_combo(request):
    return render(request, 'pillagercalc/input_combo.html')


def result(request):
    shark = request.GET.get("shark")
    scabbs = request.GET.get("scabbs")
    tenwu = request.GET.get("tenwu")
    foxy = request.GET.get("foxy")
    dancer = request.GET.get("dancer")
    pillager = request.GET.get("pillager")
    potion = request.GET.get("potion")
    step = request.GET.get("step")
    prep = request.GET.get("prep")
    coins = request.GET.get("coins")
    mana = request.GET.get("mana")
    life_total = request.GET.get("life_total")
    cards_played = request.GET.get("cards_played")

    if coins == "":
        coins = "0"

    if life_total == "":
        life_total = "30"

    if mana == "":
        mana = "0"

    if cards_played == "":
        cards_played = 0

    start_hand = []
    if shark == "1":
        start_hand.append(card.Card("shark", 4))
    if scabbs == "1":
        start_hand.append(card.Card("scabbs", 4))
    if tenwu == "1":
        start_hand.append(card.Card("tenwu", 2))
    if foxy == "1":
        start_hand.append(card.Card("foxy", 2))
    if dancer == "1":
        start_hand.append(card.Card("dancer", 2))
    for i in range(int(pillager)):
        start_hand.append(card.Card("pillager", 6))
    for i in range(int(potion)):
        start_hand.append(card.Card("potion", 4))
    for i in range(int(step)):
        start_hand.append(card.Card("step", 0))
    for i in range(int(prep)):
        start_hand.append(card.Card("prep", 0))
    for i in range(int(coins)):
        start_hand.append(card.Card("coin", 0))

    root = state_node.StateNode(False, None, None, "untargeted", mana, cards_played, 0, 0, 0, 0, int(life_total), start_hand, [])
    calc = game_tree.GameTree(root)
    lethal_node = calc.tree_search()
    if lethal_node is not None:
        combo = lethal_node.backtrack()
        context = {
            "combo": combo
        }
        return render(request, 'pillagercalc/result.html', context)
    return HttpResponse("Failed to find a combo with this hand")


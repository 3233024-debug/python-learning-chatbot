import random

GAME_TYPE = "janken"

hands = ["グー", "チョキ", "パー"]

wins = 0
losses = 0
draws = 0

def play(player):
    global wins, losses, draws

    computer = random.choice(hands)

    if player == computer:
        draws += 1
        return f"🤝 あいこ！ コンピューターも{computer}"

    elif (
        (player == "グー" and computer == "チョキ")
        or (player == "チョキ" and computer == "パー")
        or (player == "パー" and computer == "グー")
    ):
        wins += 1
        return f"🎉 あなたの勝ち！ コンピューターは{computer}"

    else:
        losses += 1
        return f"💦 あなたの負け！ コンピューターは{computer}"

def get_score():
    return {
        "wins": wins,
        "losses": losses,
        "draws": draws
    }

def reset_score():
    global wins, losses, draws
    wins = 0
    losses = 0
    draws = 0

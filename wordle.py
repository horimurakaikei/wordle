# -*- coding: utf-8 -*-
import random
import os
import sys

# Windows でのUTF-8出力を強制
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stdin.reconfigure(encoding="utf-8", errors="replace")

# 正確に5文字のカタカナ単語
WORDS_5 = [
    "ハンバーグ",  # ハ ン バ ー グ
    "オムライス",  # オ ム ラ イ ス
    "カレーパン",  # カ レ ー パ ン
    "バスケット",  # バ ス ケ ッ ト
    "コンサート",  # コ ン サ ー ト
    "プリンター",  # プ リ ン タ ー
    "カメラマン",  # カ メ ラ マ ン
    "ハリケーン",  # ハ リ ケ ー ン
    "バイオリン",  # バ イ オ リ ン
    "アルバイト",  # ア ル バ イ ト
    "オートバイ",  # オ ー ト バ イ
    "ストライキ",  # ス ト ラ イ キ
    "チャンネル",  # チ ャ ン ネ ル
    "タンバリン",  # タ ン バ リ ン
    "マンホール",  # マ ン ホ ー ル
    "スペシャル",  # ス ペ シ ャ ル
    "ランドセル",  # ラ ン ド セ ル
    "スイミング",  # ス イ ミ ン グ
    "ピクニック",  # ピ ク ニ ッ ク
    "マスコット",  # マ ス コ ッ ト
    "デザイナー",  # デ ザ イ ナ ー
    "ハーモニカ",  # ハ ー モ ニ カ
    "ランニング",  # ラ ン ニ ン グ
    "ジャングル",  # ジ ャ ン グ ル
    "タブレット",  # タ ブ レ ッ ト
    "ワンピース",  # ワ ン ピ ー ス
    "スキーヤー",  # ス キ ー ヤ ー
    "エレベーター"[:5],
    "コンピュータ",
    "アイスクリーム"[:5],
]

# 5文字のみ保証
WORDS_5 = [w for w in WORDS_5 if len(w) == 5]

GREEN  = "\033[42m\033[30m"
YELLOW = "\033[43m\033[30m"
GRAY   = "\033[100m\033[37m"
RESET  = "\033[0m"
BOLD   = "\033[1m"
CYAN   = "\033[96m"
RED    = "\033[91m"
GREEN_TEXT = "\033[92m"


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def color_feedback(guess, answer):
    answer_chars = list(answer)
    guess_chars  = list(guess)
    colors = ["gray"] * 5

    for i in range(5):
        if guess_chars[i] == answer_chars[i]:
            colors[i] = "green"
            answer_chars[i] = None

    for i in range(5):
        if colors[i] == "green":
            continue
        if guess_chars[i] in answer_chars:
            colors[i] = "yellow"
            answer_chars[answer_chars.index(guess_chars[i])] = None

    row = ""
    for i, char in enumerate(guess_chars):
        if colors[i] == "green":
            row += f"{GREEN} {char} {RESET}"
        elif colors[i] == "yellow":
            row += f"{YELLOW} {char} {RESET}"
        else:
            row += f"{GRAY} {char} {RESET}"

    return row, colors


def draw_board(guesses, feedbacks):
    print(f"\n{BOLD}{CYAN}+------------------------+{RESET}")
    print(f"{BOLD}{CYAN}|   W O R D L E  [JP]    |{RESET}")
    print(f"{BOLD}{CYAN}+------------------------+{RESET}\n")

    for i in range(6):
        if i < len(guesses):
            row, _ = feedbacks[i]
            print(f"  {row}")
        else:
            print(f"  {GRAY} ？ {RESET}{GRAY} ？ {RESET}{GRAY} ？ {RESET}{GRAY} ？ {RESET}{GRAY} ？ {RESET}")
    print()


def draw_legend():
    print(f"  {GREEN} 文 {RESET} 正しい位置  "
          f"{YELLOW} 文 {RESET} 位置が違う  "
          f"{GRAY} 文 {RESET} 含まれない\n")


def get_guess(attempt):
    while True:
        try:
            guess = input(f"  {BOLD}第{attempt}回 予想（5文字のカタカナ）: {RESET}").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return None
        if len(guess) == 5:
            return guess
        print(f"  {RED}5文字で入力してください（今: {len(guess)}文字）{RESET}")


def play():
    answer  = random.choice(WORDS_5)
    guesses  = []
    feedbacks = []
    won = False

    for attempt in range(1, 7):
        clear()
        draw_board(guesses, feedbacks)
        draw_legend()

        guess = get_guess(attempt)
        if guess is None:
            return False

        fb = color_feedback(guess, answer)
        guesses.append(guess)
        feedbacks.append(fb)

        if guess == answer:
            won = True
            break

    clear()
    draw_board(guesses, feedbacks)
    draw_legend()

    if won:
        attempts = len(guesses)
        star = "**" if attempts == 1 else ">>"
        print(f"  {star} {BOLD}{GREEN_TEXT}正解！「{answer}」{RESET}  ({attempts}回で当てました)\n")
    else:
        print(f"  xx 残念！正解は {BOLD}「{answer}」{RESET} でした。\n")

    return True


def main():
    print(f"\n{BOLD}{CYAN}  カタカナ Wordle へようこそ！{RESET}")
    print(f"  5文字のカタカナ単語を6回以内に当ててください。\n")
    input("  Enterキーでスタート...")

    while True:
        play()
        try:
            again = input("  もう一度遊びますか？ (y/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            break
        if again != "y":
            print(f"\n  またね！\n")
            break


if __name__ == "__main__":
    main()

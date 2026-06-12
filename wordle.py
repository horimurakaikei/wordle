import random
import os
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stdin.reconfigure(encoding="utf-8", errors="replace")

WORDS = [
    "apple", "brave", "chess", "dance", "earth",
    "flame", "grace", "happy", "index", "juice",
    "knife", "lemon", "magic", "night", "ocean",
    "piano", "queen", "river", "smile", "tiger",
    "ultra", "vivid", "water", "xenon", "yacht",
    "zebra", "alert", "blank", "crisp", "dirty",
    "eager", "faint", "giant", "hinge", "irony",
    "joker", "kneel", "light", "moist", "noble",
    "olive", "plumb", "quilt", "rugby", "shelf",
    "throw", "uncle", "valor", "witch", "xenon",
]

GREEN      = "\033[42m\033[30m"
YELLOW     = "\033[43m\033[30m"
GRAY       = "\033[100m\033[37m"
RESET      = "\033[0m"
BOLD       = "\033[1m"
CYAN       = "\033[96m"
RED        = "\033[91m"
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
            row += f"{GREEN} {char.upper()} {RESET}"
        elif colors[i] == "yellow":
            row += f"{YELLOW} {char.upper()} {RESET}"
        else:
            row += f"{GRAY} {char.upper()} {RESET}"

    return row, colors


def draw_board(guesses, feedbacks):
    print(f"\n{BOLD}{CYAN}+------------------------+{RESET}")
    print(f"{BOLD}{CYAN}|      W O R D L E       |{RESET}")
    print(f"{BOLD}{CYAN}+------------------------+{RESET}\n")

    for i in range(6):
        if i < len(guesses):
            row, _ = feedbacks[i]
            print(f"  {row}")
        else:
            print(f"  {GRAY} ? {RESET}{GRAY} ? {RESET}{GRAY} ? {RESET}{GRAY} ? {RESET}{GRAY} ? {RESET}")
    print()


def draw_legend():
    print(f"  {GREEN} A {RESET} correct position  "
          f"{YELLOW} A {RESET} wrong position  "
          f"{GRAY} A {RESET} not in word\n")


def get_guess(attempt):
    while True:
        try:
            guess = input(f"  {BOLD}Guess {attempt} (5-letter word): {RESET}").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return None
        if len(guess) == 5 and guess.isalpha():
            return guess
        print(f"  {RED}Please enter a 5-letter word (got: {len(guess)} characters){RESET}")


def play():
    answer   = random.choice(WORDS)
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
        print(f"  {BOLD}{GREEN_TEXT}Correct! The word was \"{answer.upper()}\" ({attempts}/6){RESET}\n")
    else:
        print(f"  {RED}Game over! The word was {BOLD}\"{answer.upper()}\"{RESET}\n")

    return True


def main():
    print(f"\n{BOLD}{CYAN}  Welcome to Wordle!{RESET}")
    print(f"  Guess the 5-letter word in 6 tries.\n")
    input("  Press Enter to start...")

    while True:
        play()
        try:
            again = input("  Play again? (y/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            break
        if again != "y":
            print(f"\n  Goodbye!\n")
            break


if __name__ == "__main__":
    main()

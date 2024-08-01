import random
import json

def choos_difficulty():
    while True:
        difficulty = input("Choose a difficulty level ( Noob / Player / Pro / Legend ) : ")
        if difficulty.lower() == "noob":
            return(1, 50, 15)
        elif difficulty.lower() == "player":
            return(1,50,8)
        elif difficulty.lower() == "pro":
            return(1,100,10)
        elif difficulty.lower() == "legend":
            return(1,100,7)
        else:
            print("Invalid choice. Please enter 'Noob' or 'Player' or 'Pro' or 'Legend'.")


def get_funny_comment(guess, number_to_guess):
    if guess < number_to_guess:
        comments = ["Aim higher, like your dreams!",
            "Too low! Try aiming a little higher.",
            "The number is higher than that. Don't be shy!",
            "Raise your sights a bit!"]
    else:
        comments = [ "Whoa there, too high! Bring it down.",
            "Too high! You're overshooting the mark.",
            "The number is lower. Try again, my friend.",
            "Lower it down a bit, you've got this!"]

    return random.choice(comments)


def load_high_score(file_name = "high_score,json"):
    try:
        with open(file_name,"r") as file:
            return json.load(file)
    except(FileNotFoundError, json.JSONDecodeError):
        return {"name": "Unknown", "score": float("inf")}


def save_high_score(name, score, file_name="high_score.json"):
    high_score_data = {"name": name, "score": score}
    with open(file_name, "w") as file:
        json.dump(high_score_data, file)


def play_game():
    print("\n<<<<<   Welcome to the Guess the Number Game   >>>>>\n")

    high_score = load_high_score()

    while True:
        print(f"........Current High Score : {high_score['name']} with {high_score['score']}.......")

        lb, ub, max_attempts = choos_difficulty()

        number_to_guess = random.randint(lb, ub)

        attempts = 0
        print(f"\nI'm thinking of a number between {lb} and {ub}. Can you guess it?")
        print(f"You've maximum {max_attempts} attempts. ")
        while attempts < max_attempts:
            try:
                guess = int(input("Enter your guess : "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            attempts +=1

            if guess < number_to_guess:
                print(get_funny_comment(guess, number_to_guess))
            elif guess > number_to_guess:
                print(get_funny_comment(guess, number_to_guess))
            else:
                print(f"congratulations! you've guessed the number {number_to_guess} in {attempts} attempts.")
                if attempts < high_score['score']:
                    name = input("you've set a new high score! Enter your name : ")
                    save_high_score(name, attempts)
                    high_score = {"name": name, "score": attempts}
                break

            print(f"You've {max_attempts - attempts} attempts to won this game!")

        if attempts == max_attempts:
            print(f"Sorry, you've run out of attempts. The number was {number_to_guess}.")

        play_again = input("Do you want to play again? (yes/no) : ").strip().lower()
        if play_again != "yes":
            print("Thanks for playing! Goodbye.....!")
            break


if __name__ == "__main__":
    play_game()
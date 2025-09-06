#!/usr/bin/env python3
"""
Level 1 Task 2: Number Guessing Game
A game where the user guesses a randomly generated number between 1 and 100.
"""

import random

class NumberGuessingGame:
    def __init__(self, min_number=1, max_number=100, max_attempts=10):
        """Initialize the game with configurable parameters"""
        self.min_number = min_number
        self.max_number = max_number
        self.max_attempts = max_attempts
        self.target_number = None
        self.attempts_used = 0
        self.game_won = False
    
    def generate_random_number(self):
        """Generate a random number within the specified range"""
        self.target_number = random.randint(self.min_number, self.max_number)
    
    def get_user_guess(self):
        """Get a valid guess from the user"""
        while True:
            try:
                guess = int(input(f"Enter your guess ({self.min_number}-{self.max_number}): "))
                if self.min_number <= guess <= self.max_number:
                    return guess
                else:
                    print(f"Please enter a number between {self.min_number} and {self.max_number}.")
            except ValueError:
                print("Invalid input! Please enter a valid number.")
    
    def provide_feedback(self, guess):
        """Provide feedback on the user's guess"""
        if guess == self.target_number:
            self.game_won = True
            print(f"Congratulations! You guessed it correctly!")
            print(f"The number was {self.target_number}")
            return True
        elif guess < self.target_number:
            print("Too low! Try a higher number.")
            return False
        else:
            print("Too high! Try a lower number.")
            return False
    
    def display_game_stats(self):
        """Display current game statistics"""
        remaining_attempts = self.max_attempts - self.attempts_used
        print(f"\nAttempts used: {self.attempts_used}/{self.max_attempts}")
        print(f"Remaining attempts: {remaining_attempts}")
    
    def play_round(self):
        """Play a single round of the game"""
        print(f"\n" + "="*50)
        print("NUMBER GUESSING GAME")
        print("="*50)
        print(f"I'm thinking of a number between {self.min_number} and {self.max_number}")
        print(f"You have {self.max_attempts} attempts to guess it!")
        print("="*50)
        
        # Generate random number for this round
        self.generate_random_number()
        
        while self.attempts_used < self.max_attempts and not self.game_won:
            self.attempts_used += 1
            print(f"\n--- Attempt {self.attempts_used} ---")
            
            guess = self.get_user_guess()
            correct = self.provide_feedback(guess)
            
            if correct:
                break
            
            if self.attempts_used < self.max_attempts:
                self.display_game_stats()
        
        # Game over
        if self.game_won:
            print(f"\nYou won in {self.attempts_used} attempts!")
            if self.attempts_used == 1:
                print("Amazing! You got it on the first try!")
            elif self.attempts_used <= 3:
                print("Excellent guessing!")
            elif self.attempts_used <= 6:
                print("Good job!")
            else:
                print("You made it just in time!")
        else:
            print(f"\nGame Over! You've used all {self.max_attempts} attempts.")
            print(f"The number was: {self.target_number}")
    
    def reset_game(self):
        """Reset game state for a new round"""
        self.target_number = None
        self.attempts_used = 0
        self.game_won = False
    
    def play(self):
        """Main game loop"""
        print("Welcome to the Number Guessing Game!")
        
        while True:
            self.play_round()
            
            # Ask if player wants to play again
            while True:
                play_again = input("\nDo you want to play again? (y/n): ").lower().strip()
                if play_again in ['y', 'yes']:
                    self.reset_game()
                    break
                elif play_again in ['n', 'no']:
                    print("Thanks for playing! Goodbye!")
                    return
                else:
                    print("Please enter 'y' for yes or 'n' for no.")

def main():
    """Main function to start the game"""
    # Create game with default settings
    game = NumberGuessingGame()
    
    # Optional: Allow user to customize difficulty
    print("Choose difficulty level:")
    print("1. Easy (1-50, 8 attempts)")
    print("2. Medium (1-100, 10 attempts) - Default")
    print("3. Hard (1-200, 12 attempts)")
    print("4. Expert (1-500, 15 attempts)")
    
    while True:
        try:
            choice = int(input("Enter your choice (1-4) or press Enter for default: ") or "2")
            if choice == 1:
                game = NumberGuessingGame(1, 50, 8)
                break
            elif choice == 2:
                game = NumberGuessingGame(1, 100, 10)
                break
            elif choice == 3:
                game = NumberGuessingGame(1, 200, 12)
                break
            elif choice == 4:
                game = NumberGuessingGame(1, 500, 15)
                break
            else:
                print("Invalid choice! Please enter 1, 2, 3, or 4.")
        except ValueError:
            print("Invalid input! Please enter a number.")
    
    # Start the game
    game.play()

if __name__ == "__main__":
    main()



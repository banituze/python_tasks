#!/usr/bin/env python3
"""
Level 1 Task 1: Simple Calculator
A basic calculator that performs four primary arithmetic operations.
"""

def add(x, y):
    """Addition function"""
    return x + y

def subtract(x, y):
    """Subtraction function"""
    return x - y

def multiply(x, y):
    """Multiplication function"""
    return x * y

def divide(x, y):
    """Division function with zero division handling"""
    if y == 0:
        raise ValueError("Error: Cannot divide by zero!")
    return x / y

def get_user_input():
    """Get valid numeric input from user"""
    while True:
        try:
            value = float(input("Enter a number: "))
            return value
        except ValueError:
            print("Invalid input! Please enter a valid number.")

def display_menu():
    """Display operation menu"""
    print("\n" + "="*40)
    print("           SIMPLE CALCULATOR")
    print("="*40)
    print("Select operation:")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    print("5. Exit")
    print("="*40)

def get_operation_choice():
    """Get valid operation choice from user"""
    while True:
        try:
            choice = int(input("Enter choice (1-5): "))
            if choice in [1, 2, 3, 4, 5]:
                return choice
            else:
                print("Invalid choice! Please enter a number between 1-5.")
        except ValueError:
            print("Invalid input! Please enter a number.")

def perform_calculation(choice, num1, num2):
    """Perform calculation based on user choice"""
    operations = {
        1: (add, "+"),
        2: (subtract, "-"),
        3: (multiply, "*"),
        4: (divide, "/")
    }
    
    func, symbol = operations[choice]
    
    try:
        result = func(num1, num2)
        print(f"\nResult: {num1} {symbol} {num2} = {result}")
        return result
    except ValueError as e:
        print(f"\n{e}")
        return None

def main():
    """Main calculator function"""
    print("Welcome to the Simple Calculator!")
    
    while True:
        display_menu()
        choice = get_operation_choice()
        
        if choice == 5:
            print("Thank you for using the calculator. Goodbye!")
            break
        
        print(f"\nYou selected: {['', 'Addition', 'Subtraction', 'Multiplication', 'Division'][choice]}")
        
        print("Enter the first number:")
        num1 = get_user_input()
        
        print("Enter the second number:")
        num2 = get_user_input()
        
        perform_calculation(choice, num1, num2)
        
        # Ask if user wants to continue
        while True:
            continue_calc = input("\nDo you want to perform another calculation? (y/n): ").lower().strip()
            if continue_calc in ['y', 'yes']:
                break
            elif continue_calc in ['n', 'no']:
                print("Thank you for using the calculator. Goodbye!")
                return
            else:
                print("Please enter 'y' for yes or 'n' for no.")

if __name__ == "__main__":
    main()



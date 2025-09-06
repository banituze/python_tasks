# Level 1 - Basic Python Tasks

This directory contains three foundational Python programming tasks designed to introduce core concepts and basic programming skills.

## Task 1: Simple Calculator (`calculator.py`)

A comprehensive calculator program that performs the four basic arithmetic operations.

### Features:
- Addition, subtraction, multiplication, and division
- Input validation and error handling
- Division by zero protection
- User-friendly interface with menu system
- Continuous operation support

### How to run:
```bash
python calculator.py
```

### Example usage:
```
Welcome to the Simple Calculator!

========================================
           SIMPLE CALCULATOR
========================================
Select operation:
1. Addition (+)
2. Subtraction (-)
3. Multiplication (*)
4. Division (/)
5. Exit
========================================
Enter choice (1-5): 1

You selected: Addition
Enter the first number: 15
Enter the second number: 25

Result: 15.0 + 25.0 = 40.0

Do you want to perform another calculation? (y/n): 
```

## Task 2: Number Guessing Game (`number_guessing_game.py`)

An interactive guessing game where users try to guess a randomly generated number.

### Features:
- Random number generation between 1-100
- Multiple difficulty levels (Easy, Medium, Hard, Expert)
- Limited attempts with feedback
- "Too high" or "too low" hints
- Score tracking and performance feedback
- Replay functionality

### How to run:
```bash
python number_guessing_game.py
```

### Difficulty levels:
- **Easy**: 1-50, 8 attempts
- **Medium**: 1-100, 10 attempts (default)
- **Hard**: 1-200, 12 attempts
- **Expert**: 1-500, 15 attempts

### Example usage:
```
Welcome to the Number Guessing Game!
Choose difficulty level:
1. Easy (1-50, 8 attempts)
2. Medium (1-100, 10 attempts) - Default
3. Hard (1-200, 12 attempts)
4. Expert (1-500, 15 attempts)
Enter your choice (1-4) or press Enter for default: 2

==================================================
NUMBER GUESSING GAME
==================================================
I'm thinking of a number between 1 and 100
You have 10 attempts to guess it!
==================================================

--- Attempt 1 ---
Enter your guess (1-100): 50
Too high! Try a lower number.

Attempts used: 1/10
Remaining attempts: 9
```

## Task 3: Word Counter (`word_counter.py`)

A comprehensive text analysis tool that counts words in text files with detailed statistics.

### Features:
- File reading with encoding detection
- Word counting and unique word analysis
- Character counting (with and without spaces)
- Line and paragraph counting
- Word frequency analysis with top N display
- Results export functionality
- Sample file generation for testing
- Comprehensive error handling

### How to run:
```bash
python word_counter.py
```

### Supported operations:
1. **Analyze a text file** - Complete analysis of any text file
2. **Create sample text file** - Generate test file for analysis
3. **Exit** - Close the application

### Example output:
```
TEXT ANALYSIS RESULTS
==================================================
File: sample_text.txt
Total Words: 156
Unique Words: 98
Total Characters: 1,023
Characters (no spaces): 847
Total Lines: 15
Total Paragraphs: 4
Average Word Length: 5.43 characters

TOP 10 MOST COMMON WORDS:
------------------------------
the             8 (5.1%)
and             6 (3.8%)
of              5 (3.2%)
is              4 (2.6%)
a               4 (2.6%)
to              3 (1.9%)
in              3 (1.9%)
text            3 (1.9%)
for             2 (1.3%)
with            2 (1.3%)
```

## Getting Started

### Prerequisites:
- Python 3.7 or higher
- No additional packages required (uses only standard library)

### Running the tasks:

1. **Calculator:**
   ```bash
   python calculator.py
   ```

2. **Number Guessing Game:**
   ```bash
   python number_guessing_game.py
   ```

3. **Word Counter:**
   ```bash
   python word_counter.py
   ```

## Learning Objectives

These tasks help you learn:

### Programming Concepts:
- Function definition and usage
- Input validation and error handling
- Conditional statements and loops
- File I/O operations
- Exception handling
- Data structures (lists, dictionaries, sets)

### Python-Specific Features:
- String manipulation and formatting
- Regular expressions
- Collections module (Counter)
- Random number generation
- Path handling with os module

### Best Practices:
- Code organization and modularity
- User-friendly interfaces
- Comprehensive error handling
- Documentation and comments
- Input validation

## Extension Ideas

### For Calculator:
- Add scientific operations (sin, cos, log, etc.)
- Implement expression parsing
- Add memory functions
- Create a graphical interface

### For Number Guessing Game:
- Add hint system with clues
- Implement multiplayer mode
- Add statistics tracking across sessions
- Create different game modes

### For Word Counter:
- Add support for multiple file formats
- Implement text similarity analysis
- Add readability scoring
- Create visualization of word frequencies

## Common Issues and Solutions

1. **File not found errors**: Ensure file paths are correct and files exist
2. **Permission errors**: Check file permissions and user access rights
3. **Encoding issues**: The word counter handles encoding detection automatically
4. **Input validation**: All programs include comprehensive input validation

These basic tasks provided me a solid foundation for more advanced Python programming concepts covered in Level 2 and Level 3.



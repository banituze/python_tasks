#!/usr/bin/env python3
"""
Level 1 Task 3: Word Counter
A program that reads a text file and counts the number of words in it.
"""

import os
import re
from collections import Counter

class WordCounter:
    def __init__(self):
        """Initialize the word counter"""
        self.file_path = None
        self.content = None
        self.word_count = 0
        self.unique_words = 0
        self.word_frequency = None
    
    def get_file_path(self):
        """Get file path from user input"""
        while True:
            file_path = input("Enter the path to the text file: ").strip()
            if file_path:
                # Handle relative paths
                if not os.path.isabs(file_path):
                    file_path = os.path.abspath(file_path)
                self.file_path = file_path
                return file_path
            else:
                print("Please enter a valid file path.")
    
    def read_file(self, file_path=None):
        """Read the content of the file with exception handling"""
        if file_path:
            self.file_path = file_path
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.content = file.read()
            print(f"Successfully read file: {self.file_path}")
            return True
        except FileNotFoundError:
            print(f"Error: File '{self.file_path}' not found.")
            print("Please check the file path and try again.")
            return False
        except PermissionError:
            print(f"Error: Permission denied to read '{self.file_path}'.")
            print("Please check file permissions and try again.")
            return False
        except UnicodeDecodeError:
            print(f"Error: Unable to decode the file '{self.file_path}'.")
            print("The file might be in a different encoding or be a binary file.")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False
    
    def count_words(self, content=None):
        """Count words in the content"""
        if content:
            self.content = content
        
        if not self.content:
            print("No content to count words from.")
            return 0
        
        # Split content into words using regex to handle punctuation
        # This regex finds sequences of word characters (letters, digits, underscores)
        words = re.findall(r'\b\w+\b', self.content.lower())
        
        self.word_count = len(words)
        self.unique_words = len(set(words))
        
        # Create word frequency dictionary
        self.word_frequency = Counter(words)
        
        return self.word_count
    
    def display_basic_stats(self):
        """Display basic statistics about the text"""
        if not self.content:
            print("No content to analyze.")
            return
        
        # Count additional statistics
        lines = self.content.split('\n')
        paragraphs = [p for p in self.content.split('\n\n') if p.strip()]
        characters = len(self.content)
        characters_no_spaces = len(self.content.replace(' ', ''))
        
        print("\n" + "="*50)
        print("TEXT ANALYSIS RESULTS")
        print("="*50)
        print(f"File: {os.path.basename(self.file_path)}")
        print(f"Total Words: {self.word_count:,}")
        print(f"Unique Words: {self.unique_words:,}")
        print(f"Total Characters: {characters:,}")
        print(f"Characters (no spaces): {characters_no_spaces:,}")
        print(f"Total Lines: {len(lines):,}")
        print(f"Total Paragraphs: {len(paragraphs):,}")
        
        if self.word_count > 0:
            avg_word_length = characters_no_spaces / self.word_count
            print(f"Average Word Length: {avg_word_length:.2f} characters")
    
    def display_word_frequency(self, top_n=10):
        """Display the most common words"""
        if not self.word_frequency:
            print("No word frequency data available.")
            return
        
        print(f"\nTOP {top_n} MOST COMMON WORDS:")
        print("-" * 30)
        
        for word, count in self.word_frequency.most_common(top_n):
            percentage = (count / self.word_count) * 100
            print(f"{word:<15} {count:>5} ({percentage:.1f}%)")
    
    def save_results(self):
        """Save analysis results to a file"""
        if not self.content:
            print("No analysis results to save.")
            return
        
        try:
            base_name = os.path.splitext(os.path.basename(self.file_path))[0]
            output_file = f"{base_name}_word_analysis.txt"
            
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write("WORD ANALYSIS RESULTS\n")
                file.write("="*50 + "\n")
                file.write(f"Source File: {self.file_path}\n")
                file.write(f"Total Words: {self.word_count:,}\n")
                file.write(f"Unique Words: {self.unique_words:,}\n")
                file.write(f"Analysis Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                file.write("WORD FREQUENCY (Top 50):\n")
                file.write("-" * 30 + "\n")
                for word, count in self.word_frequency.most_common(50):
                    percentage = (count / self.word_count) * 100
                    file.write(f"{word:<20} {count:>5} ({percentage:.1f}%)\n")
            
            print(f"Analysis results saved to: {output_file}")
        except Exception as e:
            print(f"Error saving results: {e}")
    
    def create_sample_file(self):
        """Create a sample text file for testing"""
        sample_content = """The quick brown fox jumps over the lazy dog.
This sentence contains every letter of the alphabet at least once.
It is commonly used as a typing exercise and font display.

Word counting is an important skill in text analysis.
Python makes it easy to process text files and extract meaningful statistics.
Regular expressions help us identify word boundaries accurately.

The art of programming involves breaking down complex problems into smaller parts.
Each function should have a single responsibility and be well-documented.
Error handling ensures our programs are robust and user-friendly.

This sample file contains multiple paragraphs with varying sentence structures.
It includes punctuation, numbers like 123, and UPPERCASE words.
Word frequency analysis reveals patterns in text usage."""
        
        sample_file = "sample_text.txt"
        try:
            with open(sample_file, 'w', encoding='utf-8') as file:
                file.write(sample_content)
            print(f"Sample file created: {sample_file}")
            return sample_file
        except Exception as e:
            print(f"Error creating sample file: {e}")
            return None

def main():
    """Main function to run the word counter"""
    counter = WordCounter()
    
    print("Welcome to the Word Counter!")
    print("This program analyzes text files and provides word statistics.")
    
    while True:
        print("\n" + "="*50)
        print("WORD COUNTER - MAIN MENU")
        print("="*50)
        print("1. Analyze a text file")
        print("2. Create sample text file")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            file_path = counter.get_file_path()
            
            if counter.read_file(file_path):
                word_count = counter.count_words()
                
                if word_count > 0:
                    counter.display_basic_stats()
                    
                    # Ask if user wants to see word frequency
                    while True:
                        show_freq = input("\nDo you want to see word frequency analysis? (y/n): ").lower().strip()
                        if show_freq in ['y', 'yes']:
                            try:
                                top_n = int(input("How many top words to display? (default: 10): ") or "10")
                                counter.display_word_frequency(top_n)
                            except ValueError:
                                counter.display_word_frequency()
                            break
                        elif show_freq in ['n', 'no']:
                            break
                        else:
                            print("Please enter 'y' for yes or 'n' for no.")
                    
                    # Ask if user wants to save results
                    while True:
                        save_results = input("\nDo you want to save the analysis results? (y/n): ").lower().strip()
                        if save_results in ['y', 'yes']:
                            counter.save_results()
                            break
                        elif save_results in ['n', 'no']:
                            break
                        else:
                            print("Please enter 'y' for yes or 'n' for no.")
                else:
                    print("The file appears to be empty or contains no readable words.")
        
        elif choice == '2':
            sample_file = counter.create_sample_file()
            if sample_file:
                print(f"You can now analyze the sample file by choosing option 1 and entering: {sample_file}")
        
        elif choice == '3':
            print("Thank you for using the Word Counter! Goodbye!")
            break
        
        else:
            print("Invalid choice! Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()



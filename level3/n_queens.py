#!/usr/bin/env python3
"""
Level 3 Task 3: N-Queens Problem
Solve the classic N-Queens problem using backtracking algorithm.
"""

import time
from typing import List, Tuple, Set
from collections import defaultdict

class NQueensSolver:
    """N-Queens problem solver using backtracking"""
    
    def __init__(self, n: int):
        """Initialize the solver for N x N board"""
        self.n = n
        self.board = [[0 for _ in range(n)] for _ in range(n)]
        self.solutions = []
        self.solution_count = 0
        self.backtrack_count = 0
        self.start_time = None
    
    def reset(self):
        """Reset the solver state"""
        self.board = [[0 for _ in range(self.n)] for _ in range(self.n)]
        self.solutions = []
        self.solution_count = 0
        self.backtrack_count = 0
    
    def is_safe(self, row: int, col: int) -> bool:
        """
        Check if placing a queen at position (row, col) is safe
        A position is safe if no other queen can attack it
        """
        # Check this column on upper rows
        for i in range(row):
            if self.board[i][col] == 1:
                return False
        
        # Check upper diagonal on left side
        i, j = row - 1, col - 1
        while i >= 0 and j >= 0:
            if self.board[i][j] == 1:
                return False
            i -= 1
            j -= 1
        
        # Check upper diagonal on right side
        i, j = row - 1, col + 1
        while i >= 0 and j < self.n:
            if self.board[i][j] == 1:
                return False
            i -= 1
            j += 1
        
        return True
    
    def is_safe_optimized(self, row: int, col: int, 
                         cols: Set[int], diag1: Set[int], diag2: Set[int]) -> bool:
        """
        Optimized safety check using sets for O(1) lookup
        diag1: row - col (for \ diagonal)
        diag2: row + col (for / diagonal)
        """
        return (col not in cols and 
                (row - col) not in diag1 and 
                (row + col) not in diag2)
    
    def solve_backtrack(self, row: int = 0) -> bool:
        """
        Solve N-Queens using backtracking (finds first solution)
        Returns True if solution exists, False otherwise
        """
        # Base case: if all queens are placed
        if row >= self.n:
            return True
        
        # Try placing queen in each column of this row
        for col in range(self.n):
            if self.is_safe(row, col):
                # Place queen
                self.board[row][col] = 1
                
                # Recursively place queens in remaining rows
                if self.solve_backtrack(row + 1):
                    return True
                
                # If placing queen doesn't lead to solution, backtrack
                self.board[row][col] = 0
                self.backtrack_count += 1
        
        # No solution found in this configuration
        return False
    
    def solve_all_backtrack(self, row: int = 0, 
                           cols: Set[int] = None, 
                           diag1: Set[int] = None, 
                           diag2: Set[int] = None):
        """
        Find all solutions using optimized backtracking
        Uses sets for O(1) conflict detection
        """
        if cols is None:
            cols = set()
        if diag1 is None:
            diag1 = set()
        if diag2 is None:
            diag2 = set()
        
        # Base case: all queens placed successfully
        if row == self.n:
            # Save current solution
            solution = []
            for r in range(self.n):
                for c in range(self.n):
                    if self.board[r][c] == 1:
                        solution.append((r, c))
            self.solutions.append(solution[:])
            self.solution_count += 1
            return
        
        # Try placing queen in each column of current row
        for col in range(self.n):
            if self.is_safe_optimized(row, col, cols, diag1, diag2):
                # Place queen
                self.board[row][col] = 1
                cols.add(col)
                diag1.add(row - col)
                diag2.add(row + col)
                
                # Recurse to next row
                self.solve_all_backtrack(row + 1, cols, diag1, diag2)
                
                # Backtrack
                self.board[row][col] = 0
                cols.remove(col)
                diag1.remove(row - col)
                diag2.remove(row + col)
                self.backtrack_count += 1
    
    def solve_iterative(self) -> bool:
        """
        Iterative solution using stack (alternative to recursion)
        """
        if self.n == 0:
            return True
        
        stack = [(0, 0)]  # (row, col)
        positions = []    # Track queen positions
        
        while stack:
            row, col = stack.pop()
            
            # If we've backtracked to a previous row, remove queens from later rows
            while len(positions) > row:
                old_row, old_col = positions.pop()
                self.board[old_row][old_col] = 0
            
            # Try to place queen starting from current column
            found = False
            for c in range(col, self.n):
                if self.is_safe(row, c):
                    self.board[row][c] = 1
                    positions.append((row, c))
                    found = True
                    
                    if row == self.n - 1:
                        # All queens placed successfully
                        return True
                    else:
                        # Move to next row
                        stack.append((row, c + 1))  # For backtracking
                        stack.append((row + 1, 0))  # Next row
                    break
            
            if not found:
                self.backtrack_count += 1
        
        return False
    
    def display_board(self, solution: List[Tuple[int, int]] = None):
        """Display the chess board with queens"""
        if solution:
            # Display specific solution
            temp_board = [[0 for _ in range(self.n)] for _ in range(self.n)]
            for row, col in solution:
                temp_board[row][col] = 1
            board_to_show = temp_board
        else:
            board_to_show = self.board
        
        print(f"\n{'='*4*self.n}")
        print(f"{'N-QUEENS SOLUTION':^{4*self.n}}")
        print(f"{'='*4*self.n}")
        
        # Column numbers
        print("   ", end="")
        for i in range(self.n):
            print(f"{i:3} ", end="")
        print()
        
        # Board with row numbers
        for i in range(self.n):
            print(f"{i:2} ", end="")
            for j in range(self.n):
                if board_to_show[i][j] == 1:
                    print(" Q  ", end="")
                else:
                    # Checkerboard pattern
                    if (i + j) % 2 == 0:
                        print(" ·  ", end="")
                    else:
                        print("    ", end="")
            print(f" {i}")
        
        # Column numbers at bottom
        print("   ", end="")
        for i in range(self.n):
            print(f"{i:3} ", end="")
        print()
        print(f"{'='*4*self.n}")
    
    def display_compact_board(self, solution: List[Tuple[int, int]] = None):
        """Display board in compact format"""
        if solution:
            temp_board = [[0 for _ in range(self.n)] for _ in range(self.n)]
            for row, col in solution:
                temp_board[row][col] = 1
            board_to_show = temp_board
        else:
            board_to_show = self.board
        
        for i in range(self.n):
            for j in range(self.n):
                if board_to_show[i][j] == 1:
                    print("Q", end=" ")
                else:
                    print("·", end=" ")
            print()
    
    def get_statistics(self) -> dict:
        """Get solving statistics"""
        return {
            'board_size': self.n,
            'solutions_found': self.solution_count,
            'backtrack_operations': self.backtrack_count,
            'time_taken': time.time() - self.start_time if self.start_time else 0
        }
    
    def validate_solution(self, solution: List[Tuple[int, int]]) -> bool:
        """Validate if a solution is correct"""
        if len(solution) != self.n:
            return False
        
        rows = set()
        cols = set()
        diag1 = set()
        diag2 = set()
        
        for row, col in solution:
            if (row in rows or col in cols or 
                (row - col) in diag1 or (row + col) in diag2):
                return False
            
            rows.add(row)
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
        
        return True

class NQueensAnalyzer:
    """Analyze N-Queens solutions and provide insights"""
    
    @staticmethod
    def get_known_solution_counts():
        """Return known solution counts for different N values"""
        return {
            1: 1, 2: 0, 3: 0, 4: 2, 5: 10, 6: 4, 7: 40, 8: 92,
            9: 352, 10: 724, 11: 2680, 12: 14200, 13: 73712, 14: 365596
        }
    
    @staticmethod
    def analyze_symmetry(solutions: List[List[Tuple[int, int]]], n: int):
        """Analyze symmetrical properties of solutions"""
        if not solutions:
            return
        
        print(f"\n SYMMETRY ANALYSIS FOR {n}-QUEENS:")
        print("-" * 40)
        
        # Group solutions by symmetry
        unique_solutions = set()
        for solution in solutions:
            # Convert to tuple of tuples for hashing
            solution_tuple = tuple(sorted(solution))
            unique_solutions.add(solution_tuple)
        
        print(f"Total solutions: {len(solutions)}")
        print(f"Unique solutions (ignoring symmetry): {len(unique_solutions)}")
        
        # For N=8, show the relationship with known facts
        if n == 8:
            print(f"Expected solutions: 92 ")
            print(f"Fundamental solutions (unique after symmetry): 12")
    
    @staticmethod
    def benchmark_different_sizes():
        """Benchmark solving time for different board sizes"""
        print("\n PERFORMANCE BENCHMARK:")
        print("-" * 50)
        print(f"{'N':<3} {'Solutions':<10} {'Time (s)':<10} {'Backtracks':<12}")
        print("-" * 50)
        
        known_counts = NQueensAnalyzer.get_known_solution_counts()
        
        for n in range(4, min(10, 15)):  # Test up to 9x9 for reasonable time
            solver = NQueensSolver(n)
            
            start_time = time.time()
            solver.start_time = start_time
            solver.solve_all_backtrack()
            end_time = time.time()
            
            expected = known_counts.get(n, "Unknown")
            status = "" if solver.solution_count == expected else ""
            
            print(f"{n:<3} {solver.solution_count:<10} {end_time-start_time:<10.4f} "
                  f"{solver.backtrack_count:<12} {status}")

def get_board_size():
    """Get board size from user with validation"""
    while True:
        try:
            n = int(input("Enter board size N (4-20): "))
            if 4 <= n <= 20:
                return n
            elif n < 4:
                print("Board size must be at least 4 for interesting solutions")
            else:
                print("Board size too large (may take very long time)")
        except ValueError:
            print("Please enter a valid number")

def get_solving_method():
    """Get solving method choice from user"""
    print("\n Choose solving method:")
    print("1.  Find first solution only (fast)")
    print("2.  Find all solutions (slower for large N)")
    print("3.  Iterative approach (first solution)")
    print("4.  Performance benchmark")
    
    while True:
        choice = input("Enter your choice (1-4): ").strip()
        if choice in ['1', '2', '3', '4']:
            return choice
        print("Invalid choice. Please enter 1, 2, 3, or 4.")

def main():
    """Main function"""
    print(" Welcome to the N-Queens Problem Solver!")
    print("This program solves the classic N-Queens problem using backtracking.")
    print("\nThe N-Queens problem: Place N queens on an N×N chessboard")
    print("such that no two queens threaten each other.")
    
    while True:
        try:
            method = get_solving_method()
            
            if method == '4':
                # Performance benchmark
                print("\n Running performance benchmark...")
                print("This will test different board sizes and measure performance.")
                NQueensAnalyzer.benchmark_different_sizes()
            
            else:
                n = get_board_size()
                solver = NQueensSolver(n)
                
                print(f"\n Solving {n}-Queens problem...")
                start_time = time.time()
                solver.start_time = start_time
                
                if method == '1':
                    # Find first solution
                    print("Finding first solution...")
                    if solver.solve_backtrack():
                        end_time = time.time()
                        print(f" Solution found in {end_time - start_time:.4f} seconds!")
                        solver.display_board()
                        
                        # Validate solution
                        solution = []
                        for r in range(n):
                            for c in range(n):
                                if solver.board[r][c] == 1:
                                    solution.append((r, c))
                        
                        if solver.validate_solution(solution):
                            print(" Solution is valid!")
                        else:
                            print(" Solution validation failed!")
                    else:
                        print(f" No solution exists for {n}-Queens")
                
                elif method == '2':
                    # Find all solutions
                    print("Finding all solutions...")
                    solver.solve_all_backtrack()
                    end_time = time.time()
                    
                    if solver.solutions:
                        print(f" Found {solver.solution_count} solutions in {end_time - start_time:.4f} seconds!")
                        
                        # Display statistics
                        stats = solver.get_statistics()
                        print(f"\n STATISTICS:")
                        print(f"Board size: {stats['board_size']}×{stats['board_size']}")
                        print(f"Solutions found: {stats['solutions_found']}")
                        print(f"Backtrack operations: {stats['backtrack_operations']}")
                        print(f"Time taken: {stats['time_taken']:.4f} seconds")
                        
                        # Show first few solutions
                        show_count = min(3, len(solver.solutions))
                        for i in range(show_count):
                            print(f"\n--- Solution {i+1} ---")
                            solver.display_compact_board(solver.solutions[i])
                        
                        if len(solver.solutions) > show_count:
                            print(f"\n... and {len(solver.solutions) - show_count} more solutions")
                        
                        # Analyze symmetry for smaller boards
                        if n <= 8:
                            NQueensAnalyzer.analyze_symmetry(solver.solutions, n)
                    else:
                        print(f" No solutions exist for {n}-Queens")
                
                elif method == '3':
                    # Iterative approach
                    print("Using iterative approach...")
                    if solver.solve_iterative():
                        end_time = time.time()
                        print(f" Solution found in {end_time - start_time:.4f} seconds!")
                        solver.display_board()
                    else:
                        print(f" No solution exists for {n}-Queens")
            
            # Ask to continue
            while True:
                continue_choice = input("\nDo you want to solve another N-Queens problem? (y/n): ").lower().strip()
                if continue_choice in ['y', 'yes']:
                    break
                elif continue_choice in ['n', 'no']:
                    print("Thank you for using the N-Queens Solver! ")
                    return
                else:
                    print("Please enter 'y' for yes or 'n' for no.")
        
        except KeyboardInterrupt:
            print("\n\n Program interrupted by user")
            break
        except Exception as e:
            print(f" An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()



#!/usr/bin/env python3
"""
Level 2 Task 1: To-Do List Application
A command-line to-do list application with persistent storage.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class Task:
    def __init__(self, id: int, title: str, description: str = "", completed: bool = False, 
                 created_at: str = None, completed_at: str = None, priority: str = "medium"):
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = created_at or datetime.now().isoformat()
        self.completed_at = completed_at
        self.priority = priority
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at,
            'completed_at': self.completed_at,
            'priority': self.priority
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """Create task from dictionary"""
        return cls(
            id=data['id'],
            title=data['title'],
            description=data.get('description', ''),
            completed=data.get('completed', False),
            created_at=data.get('created_at'),
            completed_at=data.get('completed_at'),
            priority=data.get('priority', 'medium')
        )
    
    def __str__(self) -> str:
        status = "" if self.completed else ""
        return f"[{self.id}] {status} {self.title}"

class TodoList:
    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self.tasks: List[Task] = []
        self.next_id = 1
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    self.tasks = [Task.from_dict(task_data) for task_data in data.get('tasks', [])]
                    self.next_id = data.get('next_id', 1)
                print(f" Loaded {len(self.tasks)} tasks from {self.filename}")
            else:
                print(f" No existing task file found. Starting fresh!")
        except json.JSONDecodeError:
            print(f" Error: Invalid JSON in {self.filename}. Starting with empty task list.")
        except Exception as e:
            print(f" Error loading tasks: {e}")
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        try:
            data = {
                'tasks': [task.to_dict() for task in self.tasks],
                'next_id': self.next_id,
                'last_saved': datetime.now().isoformat()
            }
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            print(f" Tasks saved to {self.filename}")
        except Exception as e:
            print(f" Error saving tasks: {e}")
    
    def add_task(self, title: str, description: str = "", priority: str = "medium") -> Task:
        """Add a new task"""
        if not title.strip():
            raise ValueError("Task title cannot be empty")
        
        task = Task(
            id=self.next_id,
            title=title.strip(),
            description=description.strip(),
            priority=priority
        )
        
        self.tasks.append(task)
        self.next_id += 1
        self.save_tasks()
        
        print(f" Added task: {task.title}")
        return task
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID"""
        task = self.find_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            print(f" Deleted task: {task.title}")
            return True
        else:
            print(f" Task with ID {task_id} not found")
            return False
    
    def complete_task(self, task_id: int) -> bool:
        """Mark a task as completed"""
        task = self.find_task_by_id(task_id)
        if task:
            if task.completed:
                print(f"ℹ Task '{task.title}' is already completed")
                return False
            else:
                task.completed = True
                task.completed_at = datetime.now().isoformat()
                self.save_tasks()
                print(f" Completed task: {task.title}")
                return True
        else:
            print(f" Task with ID {task_id} not found")
            return False
    
    def uncomplete_task(self, task_id: int) -> bool:
        """Mark a task as not completed"""
        task = self.find_task_by_id(task_id)
        if task:
            if not task.completed:
                print(f"ℹ Task '{task.title}' is already pending")
                return False
            else:
                task.completed = False
                task.completed_at = None
                self.save_tasks()
                print(f" Reopened task: {task.title}")
                return True
        else:
            print(f" Task with ID {task_id} not found")
            return False
    
    def find_task_by_id(self, task_id: int) -> Optional[Task]:
        """Find a task by its ID"""
        return next((task for task in self.tasks if task.id == task_id), None)
    
    def list_tasks(self, show_completed: bool = True, filter_priority: str = None):
        """Display all tasks"""
        if not self.tasks:
            print(" No tasks found. Add some tasks to get started!")
            return
        
        # Filter tasks
        filtered_tasks = self.tasks
        
        if not show_completed:
            filtered_tasks = [task for task in filtered_tasks if not task.completed]
        
        if filter_priority:
            filtered_tasks = [task for task in filtered_tasks if task.priority == filter_priority]
        
        if not filtered_tasks:
            print(" No tasks match the current filters.")
            return
        
        # Group tasks by status
        pending_tasks = [task for task in filtered_tasks if not task.completed]
        completed_tasks = [task for task in filtered_tasks if task.completed]
        
        print("\n" + "="*60)
        print(" TO-DO LIST")
        print("="*60)
        
        if pending_tasks:
            print(f"PENDING TASKS ({len(pending_tasks)}):")
            print("-" * 40)
            for task in sorted(pending_tasks, key=lambda t: t.priority == 'high', reverse=True):
                print(f"  {task}")
                if task.description:
                    print(f"      {task.description}")
        
        if completed_tasks and show_completed:
            print(f"\n COMPLETED TASKS ({len(completed_tasks)}):")
            print("-" * 40)
            for task in completed_tasks:
                print(f"  {task}")
                if task.description:
                    print(f"      {task.description}")
        
        # Summary
        total_tasks = len(self.tasks)
        completed_count = len([t for t in self.tasks if t.completed])
        pending_count = total_tasks - completed_count
        
        print(f"\n SUMMARY: {pending_count} pending, {completed_count} completed ({total_tasks} total)")
    
    def search_tasks(self, query: str):
        """Search tasks by title or description"""
        query = query.lower()
        matching_tasks = [
            task for task in self.tasks
            if query in task.title.lower() or query in task.description.lower()
        ]
        
        if matching_tasks:
            print(f"\n SEARCH RESULTS for '{query}' ({len(matching_tasks)} found):")
            print("-" * 50)
            for task in matching_tasks:
                print(f"  {task}")
                if task.description:
                    print(f"      {task.description}")
        else:
            print(f" No tasks found matching '{query}'")
    
    def get_statistics(self):
        """Display task statistics"""
        if not self.tasks:
            print(" No tasks to analyze.")
            return
        
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t.completed])
        pending = total - completed
        
        # Priority breakdown
        priority_counts = {"high": 0, "medium": 0, "low": 0}
        for task in self.tasks:
            priority_counts[task.priority] += 1
        
        # Completion rate
        completion_rate = (completed / total) * 100 if total > 0 else 0
        
        print("\n" + "="*50)
        print(" TASK STATISTICS")
        print("="*50)
        print(f"Total Tasks: {total}")
        print(f"Completed: {completed}")
        print(f"Pending: {pending}")
        print(f"Completion Rate: {completion_rate:.1f}%")
        print("\nPriority Breakdown:")
        print(f"   High: {priority_counts['high']}")
        print(f"  Medium: {priority_counts['medium']}")
        print(f"  Low: {priority_counts['low']}")

def get_user_input(prompt: str, required: bool = True) -> str:
    """Get user input with validation"""
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value
        print("This field is required. Please enter a value.")

def get_priority_choice() -> str:
    """Get priority choice from user"""
    while True:
        print("\nSelect priority:")
        print("1. High")
        print("2. Medium (default)")
        print("3. Low")
        
        choice = input("Enter choice (1-3) or press Enter for default: ").strip()
        
        if choice == "1":
            return "high"
        elif choice == "3":
            return "low"
        elif choice == "2" or choice == "":
            return "medium"
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def display_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print(" TO-DO LIST APPLICATION")
    print("="*50)
    print("1.  Add task")
    print("2.  List all tasks")
    print("3.  Mark task as completed")
    print("4.  Mark task as pending")
    print("5.  Delete task")
    print("6.  Search tasks")
    print("7.  Show statistics")
    print("8.  Settings")
    print("9.  Exit")
    print("="*50)

def main():
    """Main function"""
    todo_list = TodoList()
    
    print("Welcome to the To-Do List Application!")
    print("Manage your tasks efficiently with persistent storage.")
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-9): ").strip()
        
        try:
            if choice == "1":
                # Add task
                title = get_user_input("Enter task title: ")
                description = get_user_input("Enter task description (optional): ", required=False)
                priority = get_priority_choice()
                todo_list.add_task(title, description, priority)
            
            elif choice == "2":
                # List tasks
                print("\nDisplay options:")
                print("1. All tasks (default)")
                print("2. Pending tasks only")
                print("3. Filter by priority")
                
                display_choice = input("Enter choice (1-3) or press Enter for default: ").strip()
                
                if display_choice == "2":
                    todo_list.list_tasks(show_completed=False)
                elif display_choice == "3":
                    priority_filter = get_priority_choice()
                    todo_list.list_tasks(filter_priority=priority_filter)
                else:
                    todo_list.list_tasks()
            
            elif choice == "3":
                # Complete task
                todo_list.list_tasks(show_completed=False)
                if todo_list.tasks:
                    task_id = int(get_user_input("Enter task ID to complete: "))
                    todo_list.complete_task(task_id)
            
            elif choice == "4":
                # Uncomplete task
                completed_tasks = [t for t in todo_list.tasks if t.completed]
                if completed_tasks:
                    for task in completed_tasks:
                        print(f"  {task}")
                    task_id = int(get_user_input("Enter task ID to mark as pending: "))
                    todo_list.uncomplete_task(task_id)
                else:
                    print(" No completed tasks found.")
            
            elif choice == "5":
                # Delete task
                todo_list.list_tasks()
                if todo_list.tasks:
                    task_id = int(get_user_input("Enter task ID to delete: "))
                    confirm = get_user_input("Are you sure? (y/N): ").lower()
                    if confirm in ['y', 'yes']:
                        todo_list.delete_task(task_id)
                    else:
                        print(" Deletion canceled.")
            
            elif choice == "6":
                # Search tasks
                query = get_user_input("Enter search query: ")
                todo_list.search_tasks(query)
            
            elif choice == "7":
                # Statistics
                todo_list.get_statistics()
            
            elif choice == "8":
                # Settings
                print("\n Settings:")
                print(f"Current data file: {todo_list.filename}")
                print("1. Change data file")
                print("2. Export tasks")
                print("3. Import tasks")
                print("4. Clear all tasks")
                
                setting_choice = input("Enter choice (1-4): ").strip()
                
                if setting_choice == "1":
                    new_filename = get_user_input("Enter new filename: ")
                    todo_list.filename = new_filename
                    todo_list.load_tasks()
                
                elif setting_choice == "2":
                    export_file = get_user_input("Enter export filename: ")
                    todo_list.filename = export_file
                    todo_list.save_tasks()
                
                elif setting_choice == "4":
                    confirm = get_user_input("Are you sure you want to clear all tasks? (y/N): ").lower()
                    if confirm in ['y', 'yes']:
                        todo_list.tasks = []
                        todo_list.next_id = 1
                        todo_list.save_tasks()
                        print(" All tasks cleared.")
            
            elif choice == "9":
                # Exit
                print("Thank you for using the To-Do List Application! ")
                break
            
            else:
                print(" Invalid choice. Please enter a number between 1-9.")
        
        except ValueError:
            print(" Invalid input. Please enter a valid number.")
        except KeyboardInterrupt:
            print("\n\n Goodbye!")
            break
        except Exception as e:
            print(f" An error occurred: {e}")

if __name__ == "__main__":
    main()



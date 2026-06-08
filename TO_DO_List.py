def todo_list_app():
    tasks = []  # List to store the tasks
    
    while True:
        # Display Menu Header
        print("\n" + "=" * 40)
        print("📝 TO-DO LIST MANAGER 📝")
        print("=" * 40)
        print("1. ➕ Add Task")
        print("2. ❌ Delete Task")
        print("3. 👁️ View Tasks")
        print("4. 🚪 Exit")
        print("=" * 40)
        
        choice = input("Choose an option (1-4): ").strip()
        
        # Match-case syntax to execute the selected menu item
        match choice:
            case "1":
                new_task = input("\nEnter the task description: ").strip()
                if new_task:
                    tasks.append(new_task)
                    print(f"✅ Task '{new_task}' added successfully!")
                else:
                    print("⚠️ Task cannot be empty.")
                    
            case "2":
                if not tasks:
                    print("\n📭 Your list is already empty. Nothing to delete.")
                    continue
                
                # Show tasks with numbers so the user can pick one
                print("\nYour Current Tasks:")
                for index, task in enumerate(tasks, start=1):
                    print(f"{index}. {task}")
                    
                try:
                    task_num = int(input("\nEnter the number of the task to delete: "))
                    # Subtract 1 because Python lists start at index 0
                    if 1 <= task_num <= len(tasks):
                        removed = tasks.pop(task_num - 1)
                        print(f"🗑️ Removed task: '{removed}'")
                    else:
                        print("⚠️ Invalid number. No task was deleted.")
                except ValueError:
                    print("❌ Please enter a valid number.")
                    
            case "3":
                if not tasks:
                    print("\n📭 Your To-Do list is currently empty!")
                else:
                    print("\n📋 YOUR TO-DO LIST:")
                    print("-" * 20)
                    for index, task in enumerate(tasks, start=1):
                        print(f"{index}. {task}")
                    print("-" * 20)
                    
            case "4":
                print("\n👋 Goodbye! Have a productive day.")
                break  # Exit the loop and close the program
                
            case _:
                print("❌ Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    todo_list_app()

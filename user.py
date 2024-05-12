import random
import time

class Task:
    def __init__(self, task_name, target_value, unit):
        self.task_name = task_name
        self.target_value = target_value
        self.completed_value = 0
        self.unit = unit

    def update_progress(self, value):
        self.completed_value += value

    def is_completed(self):
        return self.completed_value >= self.target_value

class User:
    def __init__(self, name, level=1, num_points=0, goals=None, stats=None, attributes=None, limit=100):
        self.name = name
        self.level = level
        self.num_points = num_points
        self.goals = goals if goals else {}
        self.stats = stats if stats else {}
        self.attributes = attributes if attributes else {"probability": 0, "programming": 0, "machine learning": 0}
        self.limit = limit

    def assign_tasks(self):
        tasks = []
        for goal in self.goals:
            num_tasks = int(input(f"Enter the number of tasks for goal '{goal}': "))
            num_tasks = min(num_tasks, 3)  # Limit the number of tasks to a maximum of 3
            for i in range(num_tasks):
                task_name = input(f"Enter task {i+1} for goal '{goal}': ")
                target_value = int(input(f"Enter the target quantity for task '{task_name}': "))
                unit = input(f"Enter the unit of measurement for task '{task_name}': ")
                tasks.append(Task(task_name, target_value, unit))
        return tasks

    def complete_tasks(self, tasks):
        all_completed = True
        for task in tasks:
            if not task.is_completed():
                all_completed = False
                break
        if all_completed:
            self.num_points += 10  # Adjust points as needed
        return all_completed

    def apply_penalty(self):
        self.num_points -= 20  # Adjust penalty as needed
        print("Penalty applied for not completing tasks within 24 hours.")

    def level_up(self):
        if self.num_points >= self.limit:
            self.level += 1
            self.num_points -= self.limit
            self.num_points += 10
            self.limit += 12
            for attr in self.attributes:
                self.attributes[attr] += 1
            print("Good job! You leveled up.")

def get_user_input():
    name = input("Enter your name: ")
    goals = {}
    num_goals = int(input("Enter the number of goals: "))
    for i in range(num_goals):
        goal_name = input(f"Enter goal {i+1}: ")
        goals[goal_name] = 0
    return User(name, goals=goals)

def main():
    user = get_user_input()
    tasks = user.assign_tasks()
    start_time = time.time()

    while True:
        print(f"\nWelcome, {user.name}!")
        print(f"Level: {user.level}")
        print(f"Points: {user.num_points}")
        print("Goals:")
        for goal in user.goals:
            print(f"- {goal}")
        print("Tasks:")
        for i, task in enumerate(tasks, start=1):
            print(f"{i}. {task.task_name}: {task.completed_value}/{task.target_value} {task.unit}")

        # Check if 24 hours have passed
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time >= 24 * 60 * 60:  # 24 hours in seconds
            user.apply_penalty()
            # Create a new user with the information from the previous 24 hours
            user = User(user.name, user.level, user.num_points, user.goals, user.stats, user.attributes, user.limit)
            tasks = user.assign_tasks()
            start_time = current_time

        # Prompt user to select a task and update progress
        task_number = int(input("Enter the task number to update progress (or 0 to skip): "))
        if task_number > 0 and task_number <= len(tasks):
            task = tasks[task_number - 1]
            value = int(input(f"Enter progress for task '{task.task_name}' in {task.unit}: "))
            task.update_progress(value)

        # Check if all tasks are completed
        all_completed = user.complete_tasks(tasks)

        if all_completed:
            print("Congratulations! You completed all tasks.")
            user.level_up()
            tasks = user.assign_tasks()  # Assign new tasks for the next day
            start_time = time.time()  # Reset the timer for the next day
        else:
            print("Some tasks are still incomplete.")

        # Save user data and load it for the next day
        # ...

        choice = input("Enter 'q' to quit or any other key to continue: ")
        if choice.lower() == 'q':
            break

if __name__ == '__main__':
    main()

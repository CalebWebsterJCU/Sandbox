"""
Task Manager
by Caleb Webster
30/08/2020
This program functions as a task list. It allows the user to add, complete and view tasks to improve their workflow.
"""

from operator import itemgetter
MENU = """
MENU
L - List tasks
V - View task details
A - Add task
M - Mark task as completed
Q - Quit"""
FILE_NAME = "tasks.csv"
NAME_INDEX = 0
PRIORITY_INDEX = 1
COMPLETED_INDEX = 2
ESTIMATED_TIME_INDEX = 3
DETAILS_INDEX = 4
COMPLETED_VALUE = 'y'
UNCOMPLETED_VALUE = 'n'


def main():
    """Read tasks from file, then display, add, complete, or view details of tasks."""
    tasks = load_tasks(FILE_NAME)
    print(MENU)
    choice = input(">>> ").lower()
    while choice != 'q':
        if choice == 'l':
            if len(tasks) > 0:
                display_tasks(tasks)
            else:
                print("No tasks. Why not add a task?")
        elif choice == 'v':
            if len(tasks) > 0:
                display_tasks(tasks)
                view_task_details(tasks)
            else:
                print("No tasks. Why not add a task?")
        elif choice == 'a':
            add_task(tasks)
        elif choice == 'm':
            number_of_uncompleted_tasks = find_number_of_uncompleted_tasks(tasks)
            if len(tasks) == 0:
                print("No tasks. Why not add a task?")
            elif number_of_uncompleted_tasks > 0:
                display_tasks(tasks)
                mark_task_as_completed(tasks)
            else:
                print("All tasks are completed. Well done!")
        else:
            print("Invalid choice")
        print(MENU)
        choice = input(">>> ").lower()
    save_tasks(FILE_NAME, tasks)
    print("Have a nice day :)")


def load_tasks(file_name: str) -> list:
    """Read tasks from file and add them to a list."""
    tasks = []
    file_in = open(FILE_NAME, 'r')
    for line in file_in:
        task = line.strip().split(',')
        try:
            task[PRIORITY_INDEX] = int(task[PRIORITY_INDEX])
        except ValueError:
            print(f"Error with {file_name}. Check priority values.")
        tasks.append(task)
    file_in.close()
    return tasks


def display_tasks(tasks: list) -> None:
    """Display tasks."""
    tasks.sort(key=itemgetter(COMPLETED_INDEX, PRIORITY_INDEX))
    longest_name_length = 0
    for task in tasks:
        if len(task[NAME_INDEX]) > longest_name_length:
            longest_name_length = len(task[NAME_INDEX])
    for index, task in enumerate(tasks):
        uncompleted_marker = '*' if task[COMPLETED_INDEX] == UNCOMPLETED_VALUE else ' '
        print(f"{uncompleted_marker}{index + 1}. {task[NAME_INDEX]:{longest_name_length}} Priority {task[PRIORITY_INDEX]:3} ETA {task[ESTIMATED_TIME_INDEX]}")
    number_of_uncompleted_tasks = find_number_of_uncompleted_tasks(tasks)
    if number_of_uncompleted_tasks > 0:
        print(f"{len(tasks)} tasks. You still need to complete {number_of_uncompleted_tasks} tasks.")
    else:
        print("All tasks are completed. Well done!")


def view_task_details(tasks: list) -> None:
    """Get a task number and display the task details."""
    print("Enter the number of the task to view task details: ")
    task_number = get_positive_integer(">>> ")
    while task_number > len(tasks):
        print("Invalid task number")
        task_number = get_positive_integer(">>> ")
    print(tasks[task_number - 1][NAME_INDEX])
    if tasks[task_number - 1][DETAILS_INDEX] == "none":
        print("No details provided for this task")
    else:
        print(tasks[task_number - 1][DETAILS_INDEX])


def add_task(tasks: list) -> None:
    """Get task name, priority, eta, and details and add task to tasks."""
    name = get_nonempty_string("Name: ")
    priority = get_positive_integer("Priority: ")
    estimated_time = get_nonempty_string("Estimated time: ")
    details = get_nonempty_string("Details (if no details), enter \"none\": ")
    tasks.append([name, priority, UNCOMPLETED_VALUE, estimated_time, details])


def mark_task_as_completed(tasks: list) -> None:
    """Get number of task and change its state to completed."""
    print("Enter the number of the task to view task details: ")
    task_number = get_positive_integer(">>> ")
    while task_number > len(tasks):
        print("Invalid task number")
        task_number = get_positive_integer(">>> ")
    if tasks[task_number - 1][COMPLETED_INDEX] == COMPLETED_VALUE:
        print("That task is already completed")
    else:
        tasks[task_number - 1][COMPLETED_INDEX] = COMPLETED_VALUE
        print(f"Task \"{tasks[task_number - 1][NAME_INDEX]}\" Completed!")


def save_tasks(file_name: str, tasks: list) -> None:
    """Write tasks to file."""
    file_out = open(file_name, 'w')
    for task in tasks:
        print(f"{task[NAME_INDEX]},{task[PRIORITY_INDEX]},{task[COMPLETED_INDEX]},{task[ESTIMATED_TIME_INDEX]},{task[DETAILS_INDEX]}", file=file_out)
    file_out.close()
    print(f"{len(tasks)} tasks saved to {FILE_NAME}")


def find_number_of_uncompleted_tasks(tasks: list) -> int:
    """Find the number of tasks uncompleted."""
    number_of_uncompleted_tasks = 0
    for task in tasks:
        if task[COMPLETED_INDEX] == UNCOMPLETED_VALUE:
            number_of_uncompleted_tasks += 1
    return number_of_uncompleted_tasks


def get_positive_integer(prompt: str = "Number: ", error: str = "Invalid input; enter a valid number") -> int:
    """Get an integer greater than zero."""
    number = 0
    is_valid = False
    while not is_valid:
        try:
            number = int(input(prompt))
            if number > 0:
                is_valid = True
            else:
                print("Number must be > 0")
        except ValueError:
            print(error)
    return number


def get_nonempty_string(prompt: str = "String: ") -> str:
    """Get a string, making sure it's not empty."""
    string = input(prompt)
    while not string:
        print("Input cannot be blank")
        string = input(prompt)
    return string


main()

'''

Create an application that interfaces with the user via the CLI - prompt the user with a menu such as:

Please select from the following options (enter the number of the action you'd like to take):
1) Create a new account (POST)
2) View all your tasks (GET)
3) View your completed tasks (GET)
4) View only your incomplete tasks (GET)
5) Create a new task (POST)
6) Update an existing task (PATCH/PUT)
7) Delete a task (DELETE)

It is your responsibility to build out the application to handle all menu options above.


'''

import requests, pprint, sys
from http import HTTPStatus

def get_user_option():

    print()
    print("Please select from the following options:")
    print("1) Create a new account")
    print("2) View all your tasks")
    print("3) View your completed tasks")
    print("4) View only your incomplete tasks")
    print("5) Create a new task")
    print("6) Update an existing task")
    print("7) Delete a task")
    print("8) QUIT")
    print()

    while True:
        try:
            
            user_opt = int(input())

            if 1 <= user_opt <= 8:
                return user_opt
            else:
                print("Please input an integer between 1-8, inclusive.", file=sys.stderr)
            
        except ValueError:
            print("Invalid input. Please input an integer between 1-8, inclusive.", file=sys.stderr)

def check_url_resp(response, ok_status=HTTPStatus.OK):

    json = response.json()

    if response.status_code != ok_status:
        print(f"Error {response.status_code} - {json['error']['message']}", file=sys.stderr)
        return None
    else:
        return json["data"]

def exec_get(url):

    resp = requests.get(url)
    return check_url_resp(resp)

def exec_post(url, json_):

    resp = requests.post(url, json=json_)
    return check_url_resp(resp, HTTPStatus.CREATED) # No list, just return user dict 

def exec_put(url, json_):

    resp = requests.put(url, json=json_)
    return check_url_resp(resp)

def sign_in(url):

    print("Please enter your email:")
    email = input()

    user_data = exec_get(url + "?email=" + email)
    
    if user_data is not None:
        print()
        print(f"User [{user_data[0]['first_name']} {user_data[0]['last_name']}] is now signed in.")
        print()
        return user_data[0]
    else:
        print()
        print(f"User with email {email} could not be signed in.")
        print()
        return None

def print_task(task):
    print(f"Task ID: {task['id']}:")
    print(f"\tName: {task['name']}")
    print(f"\tDescription: {task['description']}")
    print(f"\tCompletion status: {task['completed']}")

def print_tasks(tasks, sort=True):

    if len(tasks) == 0:
        print("No tasks. Please create a task first.")
    else:
        
        if sort:
            tasks = sorted(tasks, key=lambda x: x["id"])

        print()
        for task in tasks:
            print_task(task)
        print()

    return tasks

def choose_task(url, userId):

    sorted_tasks = view_all_tasks(url, userId)

    if len(sorted_tasks) > 0:

        sorted_task_ids = tuple(task["id"] for task in sorted_tasks)
        task_id = None
        while True:
            
            task_id = input("Please input a Task ID from above: ")

            try:
                task_id = int(task_id)
                if task_id in sorted_task_ids:
                    break
                else:
                    print("Not a valid task ID. Try again", file=sys.stderr)
            except ValueError:
                print("Not a valid input. Try again", file=sys.stderr)
        
        task = exec_get(url + str(task_id))
        
        return task

def create_accnt(url):

    first_name = input("Please input a first name: ")
    last_name = input("Please input a last name: ")
    email = input("Please input an email: ")

    json = {"first_name": first_name, "last_name": last_name, "email": email}

    return exec_post(url, json)

def view_all_tasks(url, userId):
    
    tasks = exec_get(url + f"?userId={userId}")
    return print_tasks(tasks)

def view_comp_tasks(url, userId):
    
    tasks = exec_get(url + f"?userId={userId}&complete=true")
    return print_tasks(tasks)

def view_incomp_tasks(url, userId):
    
    tasks = exec_get(url + f"?userId={userId}&complete=false")
    return print_tasks(tasks)

def create_new_task(url, userId):
    
    print()
    name = input("Please input a name for this task: ")
    desc = input("Please provide a description (or leave blank): ")
    print()

    json = {"userId": userId, "name": name, "description": desc, "completed": False}

    resp = exec_post(url, json)
    if resp is not None:
        print("Task created:")
        pprint.pprint(resp)

def update_task(url, userId):
    
    task = choose_task(url, userId)

    if task is not None:

        task_url = url + str(task["id"])

        update_dict = {"userId": userId, "name": task["name"], "description": task["description"], "completed": task["completed"]}
        while True:
            
            update = input("What would you like to update? (n)ame, (d)escription, (c)ompletion status: ").lower()
            
            match update:
                case "n":
                    update_dict["name"] = input("Please input a new name for the task: ")
                case "d":
                    update_dict["description"] = input("Please input a new description for the task: ")
                case "c":
                    update_dict["completed"] = not task["completed"]
                case _:
                    print("Invalid value. Try again.", file=sys.stderr)
                    continue
            
            break
        
        resp = exec_put(task_url, update_dict)

        if resp is not None:
            print("Task successfully updated.")
            print_task(resp)
        
def del_task(url, userId):
    
    task = choose_task(url, userId)

    if task is not None:
        resp = requests.delete(url + str(task["id"]))
        resp = check_url_resp(resp)
    
#######################

if __name__ == "__main__":

    base_url = "http://demo.codingnomads.co:8080/tasks_api"
    users_url = base_url + "/users/"
    tasks_url = base_url + "/tasks/"

    print()
    print("Welcome to your task organizer.")

    user_data = None
    while True:
        
        user_opt = get_user_option()

        if user_opt == 1:
            user_data = create_accnt(users_url)
        elif user_data is None:
            print("Please sign in before accessing tasks.")
            user_data = sign_in(users_url)
        elif user_opt == 2:
            view_all_tasks(tasks_url, user_data["id"])
        elif user_opt == 3:
            view_comp_tasks(tasks_url, user_data["id"])
        elif user_opt == 4:
            view_incomp_tasks(tasks_url, user_data["id"])
        elif user_opt == 5:
            create_new_task(tasks_url, user_data["id"])
        elif user_opt == 6:
            update_task(tasks_url, user_data["id"])
        elif user_opt == 7:
            del_task(tasks_url, user_data["id"])
        else:
            break
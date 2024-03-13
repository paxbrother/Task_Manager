
#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"
dt = datetime.combine(date.today(), datetime.min.time())

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


#=====user-defined functions=======

def tasks_to_write():
    """
    Takes task lists and writes to tasks.txt, 
        for use in view_mine and add_task to update task_list
    """
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
                ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
        return


def reg_user():
        """
        Creates a new user via user inputs.
            User can't already exist in user.txt
                Password has to be confirmed or returns to menu.
                    Adds new user to user.txt
        """
        new_username = input("Please enter a new username: ")

        while new_username in username_password.keys():
            new_username = input("Username already exists, please enter a new username: ")
        else: 
            new_password = input("Please enter a new password: ")
            confirm_password = input("Confirm password: ")

            if new_password == confirm_password:
                print("New user added")
                username_password[new_username] = new_password
            else:
                print("Error - passwords do not match, please try again.")
                return
            
            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))



def add_task():
    """ 
    Creates a new task.
        Can assign user, shows registered users invalid
                user entered. Adds task to task_list,
                    then writes over tasks.txt
    """
    task_username = input("Username assigned to task: ")
    while task_username not in username_password.keys():
        users_list = []
        for k in username_password:
            users_list.append(k)
        task_username = input(f"User does not exist. Current users are {users_list}: \
please enter a valid username: ")
        
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            print("Task successfully added.")
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")
        
    curr_date = date.today()
    ''' Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
        }

    task_list.append(new_task)
    tasks_to_write()



def view_all():
    """ 
    displays full list of tasks across all users
        loops through dict of tasks and displays components 
            in string form 
    """

    print("\n\t\tComplete Task List")
    for t in task_list:
        print("_"*40)
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime('%d %b %Y')}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime('%d %b %Y')}\n"
        if t['completed'] == True:
            disp_str += f"Task Complete?:  YES\n"
        else:
            disp_str += f"Task Complete?:  NO\n"
        disp_str += f"Task Description:\n{t['description']}\n"
        print(disp_str)
    print("_"*40)



def view_mine():
    """ 
    Displays all tasks assigned to current user, 
        allowing tasks due date, assigned user and
            completion status to be changed. Can also return 
                to main menu with -1 
    """
    counter = 1
    user_tasks_numbered = []
    non_user_tasks = []
    for t in task_list:
        if t['username'] == curr_user:
            t['task number'] = counter
            counter += 1
            user_tasks_numbered.append(t)
        else:
            non_user_tasks.append(t)

    print("\n\t\tUser Assigned Tasks")
    for t in user_tasks_numbered:
        disp_str = "_"*40 + "\n"
        disp_str += f"Task Number {t['task number']}\n"
        disp_str += f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime('%d %b %Y')}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime('%d %b %Y')}\n"
        if t['completed'] == True:
            disp_str += f"Task Complete?:  YES\n"
        else:
            disp_str += f"Task Complete?:  NO\n"
        disp_str += f"Task Description: \n {t['description']}"
        print(disp_str)
    print("_"*40)

    chosen_task = []
    not_chosen = []
    users_tasks_range = len(user_tasks_numbered)
    while True:
        try:
            user_choice = int(input("Please enter a task number or enter -1 to return: "))
            break
        except ValueError:
            print("Invalid input")
       
    if user_choice == -1:
        print("Returning to menu")
        return
    
    elif user_choice > users_tasks_range:
        print("Invalid choice - returning to menu.")
        return
    
    else: 
        for t in user_tasks_numbered:
            if t['task number'] == int(user_choice):
                chosen_task.append(t)
                print("\nYou have chosen: ")
                disp_str = f"Task Number {t['task number']}\n"
                disp_str += f"Task: \t\t {t['title']}\n"
                disp_str += f"Assigned to: \t {t['username']}\n"
                disp_str += f"""Date Assigned: \t 
{t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"""
                disp_str += f"""Due Date: \t 
{t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"""
                if t['completed'] == True:
                    disp_str += f"Task Complete?:  YES\n"
                else:
                    disp_str += f"Task Complete?:  NO\n"
                disp_str += f"Task Description: \n{t['description']}\n"
                print(disp_str)
            else:
                not_chosen.append(t)

    edit_or_complete = input('''Please select one of the following options: 
    1 - Reassign the task to a different user or change the task's due date.
    2 - Mark a task as completed. 
Enter the option number: ''')

    while edit_or_complete.isnumeric() != True or int(edit_or_complete) > 2:
        edit_or_complete = input("Error - please enter either 1 or 2: ")

    if int(edit_or_complete) == 1:
        completed_check = chosen_task[0]['completed']
        if completed_check == True:
            print("""Error - this task has already been completed and cannot be
    edited.""")
            exit()
        
        date_only = chosen_task[0]['due_date']
        print(f"""\nThe current username assigned to Task Number {chosen_task[0]['task number']} is 
    {chosen_task[0]['username']}
The current due date for Task Number {chosen_task[0]['task number']} is 
    {date_only.strftime('%d %m %Y')}""")
        
        user_or_date = input("""Please enter 1 to change the username assigned, \
or enter 2 to change the due date of the task: """)
        
        while user_or_date.isnumeric() != True or int(user_or_date) > 2:
            user_or_date = input("Error - please enter either 1 or 2: ")

        if user_or_date == "1":
            print("\nThe current registered usernames are",(list(username_password.keys())))
            vm_new_user = input(f"""Please enter the username to assign Task Number \
{chosen_task[0]['task number']} to: """)
            while vm_new_user not in username_password.keys():
                vm_new_user = input("Not a valid username, please try again: ")
            if vm_new_user == chosen_task[0]['username']:
                vm_new_user = input("""Error - task already assigned to this user, please \
enter new username to assign: """)
            chosen_task[0]['username'] = vm_new_user
            print(f"""The username assigned to Task Number {chosen_task[0]['task number']}\
has been changed to {vm_new_user}.""")
            not_chosen.extend(chosen_task)
            task_list.clear()
            task_list.extend(not_chosen)
            task_list.extend(non_user_tasks)        
            tasks_to_write()    
        
        elif user_or_date == "2":
            while True:
                try:
                    new_due_date = input(f"""\nOriginal due date:\t{chosen_task[0]['due_date']}
Please enter the new due date in the format YYYY-MM-DD: """)
                    due_date_time = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                    break

                except ValueError:
                    print("Invalid datetime format. Please use the format specified.")

            chosen_task[0]['due_date'] = due_date_time
            print(f"""\nThe due date for Task Number {chosen_task[0]['task number']} \
has been updated to {due_date_time.strftime('%d %m %y')}.""")
            not_chosen.extend(chosen_task)
            task_list.clear()
            task_list.extend(not_chosen)
            task_list.extend(non_user_tasks)
            tasks_to_write()


    if edit_or_complete == "2":
        for t in chosen_task:
            completed_check = chosen_task[0]['completed']
            if completed_check == True:
                print("Error - task already completed.")
                continue
            else:
                chosen_task[0]['completed'] = True
                print(f"Task Number {chosen_task[0]['task number']} marked as complete.")
                for t in not_chosen:
                    del t['task number']
                not_chosen.extend(chosen_task) 
                task_list.clear()
                task_list.extend(not_chosen)
                task_list.extend(non_user_tasks)
                tasks_to_write()



def generate_reports():
    """
    Produces two text files
    Task overview - details on tasks as a whole
    User overview - task details broken down by user 
    """
    num_tasks = len(task_list)
    total_str = f"Total number of tasks:\t\t\t\t {num_tasks}"

    comp_count = 0
    incomp_count = 0
    for t in task_list:
        if t['completed'] == True:
            comp_count += 1
        else:
            incomp_count += 1
    comp_str = f"Total of completed tasks:\t\t\t {comp_count}"
    incomp_str = f"Total of incomplete tasks:\t\t\t {incomp_count}"

    incomp_over_count = 0
    for t in task_list:
        if t['completed'] == False and t['due_date'] < dt:
            incomp_over_count += 1
    incomp_over_str = f"Total overdue & incomplete tasks:\t {incomp_over_count}"

    incomp_percent = (incomp_count / num_tasks)*100
    incomp_per_str = f"% of incomplete tasks:  \
            {round(incomp_percent, 2)}%"

    overdue_per = (incomp_over_count/incomp_count)*100
    overdue_percent_str = f"% of overdue tasks:\t\t\
            {round(overdue_per, 2)}%"

    task_overview_str = (total_str + "\n" +
                         comp_str + "\n" +
                         incomp_str + "\n" +
                         incomp_over_str + "\n" +
                         incomp_per_str + "\n" +
                         overdue_percent_str + "\n"
                         )

    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write("\tTask Overview Report\n" + "_"*40 + "\n" 
                                 + task_overview_str + "_"*40)
        
    total_users = len(username_password.keys())
    total_users_str = f"Total number of users:\t{total_users}\n"

    total_tasks = len(task_list)
    total_tasks_str = f"Total number of tasks:\t{total_tasks}\n"

    users_list = []
    tasks_comp = []
    tasks_uncompleted = []
    tasks_overdue = []
    user_over_final_str = ""

    for user in username_password.keys():
        for t in task_list:
            if t['username'] == f"{user}":
                users_list.append(user)
            if t['username'] == f"{user}":
                if t['completed'] == True:
                    tasks_comp.append(user)
                if t['completed'] == False:
                    tasks_uncompleted.append(user)
                    if t['due_date'] < dt:
                        tasks_overdue.append(user)

        user_str = f"User name: \t\t\t\t{user}\n"
        task_str = f"No. of assigned tasks: \t{users_list.count(user)}\n"
        user_percent = (users_list.count(user)/total_tasks)*100
        per_str = f"% of tasks assigned: \t{round(user_percent, 2)}%\n"

        try:
            task_comp_per = (tasks_comp.count(user)/users_list.count(user)*100)
            tasks_comp_str = f"% tasks completed: \t\t{round(task_comp_per, 2)}%\n"
        except ZeroDivisionError as e:
            tasks_comp_str = f"% tasks completed: \t\tN/A\n" 

        try:
            tasks_incomp_per = (tasks_uncompleted.count(user)/users_list.count(user))*100
            tasks_incomp_str = f"% tasks incomplete: \t{round(tasks_incomp_per, 2)}%\n"
        except ZeroDivisionError as e:
            tasks_incomp_str = f"% tasks incomplete: \tN/A\n"

        try:
            tasks_over_per = tasks_overdue.count(user)/users_list.count(user)*100
            tasks_over_str = f"% overdue & incomplete: {round(tasks_over_per, 2)}%\n"
        except ZeroDivisionError as e:
            tasks_over_str = f"% overdue & incomplete: N/A\n"

        user_over_str = "_"*30 + "\n" + user_str + task_str 
        user_over_str += per_str + tasks_comp_str
        user_over_str += tasks_incomp_str + tasks_over_str
        user_over_final_str += user_over_str

    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write("User Overview Report\n" + "_"*40 + "\n"
                                 + total_users_str + total_tasks_str + user_over_final_str + "_"*40)
        print("""\nTask Overview report generated, please see task_overview.txt.
User Overview report generated, please see user_overview.txt.""")



#--------------------------------------

task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each task component (t_c)
    t_c = t_str.split(";")
    curr_t['username'] = t_c[0]
    curr_t['title'] = t_c[1]
    curr_t['description'] = t_c[2]
    curr_t['due_date'] = datetime.strptime(t_c[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(t_c[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if t_c[5] == "Yes" else False

    task_list.append(curr_t)

while True:
    print()
    print(f"\t\t***Hello {curr_user} - welcome to the Task Manager***")
    menu = input(f'''\nPlease select one of the following options: 
\tr - Register a user
\ta - Adding a task
\tva - View all tasks
\tvm - View my tasks
\tgr - generate reports
\tds - Display statistics
\te - Exit
: ''').lower()

    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()
          
    elif menu == 'vm':
        view_mine()             
    
    elif menu == 'gr':
        generate_reports()

    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        if not os.path.exists("tasks.txt"):
            with open("tasks.txt", "w") as task_file:
                pass
        with open("tasks.txt", 'r') as task_file:
            task_data = task_file.read().split("\n")
            task_data = [t for t in task_data if t != ""]
            task_list = []
            for t_str in task_data:
                curr_t = {}

                t_c = t_str.split(";")
                curr_t['username'] = t_c[0]
                curr_t['title'] = t_c[1]
                curr_t['description'] = t_c[2]
                curr_t['due_date'] = datetime.strptime(t_c[3], DATETIME_STRING_FORMAT)
                curr_t['assigned_date'] = datetime.strptime(t_c[4], DATETIME_STRING_FORMAT)
                curr_t['completed'] = True if t_c[5] == "Yes" else False

                task_list.append(curr_t)
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")    
    
    elif menu == 'ds' and curr_user != 'admin':
        print("Error - only the admin user may display statistics.")

    elif menu == 'e':
        print(f'Goodbye {curr_user}!\n' + "_"*60 + "\n")
        exit()

    else:
        print("You have made an invalid choice, please try again")

# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date
DATETIME_STRING_FORMAT = "%Y-%m-%d"

def reg_user():
    '''Add a new user to the user.txt file'''
    while True:
        # - Request input of a new username
        new_username = input("New Username: ")
        # - Checking if user exists.
        if new_username not in username_password.keys():
 
        # - Request input of a new password
            while True:
                new_password = input("New Password: ")

                # - Request input of password confirmation.
                confirm_password = input("Confirm Password: ")

                # - Check if the new password and confirmed password are the same.
                if new_password == confirm_password:
                # - If they are the same, add them to the user.txt file,
                    print("New user added")
                    username_password[new_username] = new_password
            
                    with open("user.txt", "w") as out_file:
                        user_data = []
                        for k in username_password:
                            user_data.append(f"{k};{username_password[k]}")
                        out_file.write("\n".join(user_data))
                        break

                # - Otherwise you present a relevant message.
                else:
                    print("\nPasswords do no match\n")
            break
        else:
            print("\nUser exists. Please choose different name.\n")    
    
def add_task():
    '''Allow a user to add a new task to task.txt file
        Prompt a user for the following: 
            - A username of the person whom the task is assigned to,
            - A title of a task,
            - A description of the task and 
            - the due date of the task.'''
    while True:
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            pass
        else:
            task_title = input("Title of Task: ")
            task_description = input("Description of Task: ")
            while True:
                try:
                    task_due_date = input("Due date of task (YYYY-MM-DD): ")
                    due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                    break

                except ValueError:
                    print("Invalid datetime format. Please use the format specified")
            break

    # Then get the current date.
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
    print("Task successfully added.")
    
def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling) 
    '''

    for t in task_list:
        disp_str = f"Task: \t\t\t {t['title']}\n"
        disp_str += f"Assigned to: \t\t {t['username']}\n"
        disp_str += f"Date Assigned: \t\t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t\t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \t {t['description']}\n"
        print(disp_str)
        
def generate_report():
    # Function to generating two reports
    # First calculating the necessary statistics
    num_users = len(username_password.keys())
    num_tasks = len(task_list)
    num_compl_tasks = 0
    overdue = 0
    for t in task_list:
        if t['completed'] == True:
            num_compl_tasks += 1
        elif datetime.date(t['due_date']) < date.today() and t['completed'] == False:
            overdue += 1
    percentage_incomplete = round((num_tasks - num_compl_tasks) / num_tasks * 100,2)
    percentage_overdue = round(overdue / num_tasks * 100,2)
    
    #The first report creates file with summary about tasks.
    with open("task_overview.txt", "w") as task_overview:
        task_report_str = f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n"
        task_report_str += f"The total number of generated tasks:                 {num_tasks}\n"
        task_report_str += f"The total number of completed tasks:                 {num_compl_tasks}\n"
        task_report_str += f"The total number of uncompleted tasks:               {num_tasks-num_compl_tasks}\n"
        task_report_str += f"The total number of uncompleted and overdue task:    {overdue}\n"
        task_report_str += f"The percentage of tasks that are incomplete:         {percentage_incomplete}\n"
        task_report_str += f"The percentage of tasks that are overdue:            {percentage_overdue}\n"
        task_report_str += f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n"
        
        #Saving report the the file.
        task_overview.write(task_report_str)
        print('Task report generated and saved to the file \"task_overview.txt\" succesfully.')
    
    #The second report creates file with summary of tasks assigned to each user with statistics.
    with open("user_overview.txt", "w") as user_overview:
        
        #Creating visual table.
        user_report_str = f"-------------------------------------------------------------------------------------\n"
        user_report_str += f"The total number of users:\t{num_users}\n"
        user_report_str += f"The total number of tasks:\t{num_tasks}\n"
        user_report_str += f"-------------------------------------------------------------------------------------\n"
        user_report_str += f"|                   |           |        Percentage of the tasks assigned           |\n"
        user_report_str += f"|        USER       |   Total   |---------------------------------------------------|\n"
        user_report_str += f"|                   |   Tasks   |   Total   | Completed | Not completed | Overdue   |\n"
        
        # Calculating the necessary statistics
        for user in username_password:
            user_task = 0
            user_completed_tasks = 0
            user_overdue = 0
            user_report_str +=f"|-------------------|-----------|-----------|-----------|---------------|-----------|\n"
            user_report_str += f"|{user}"
            user_report_str += f" "*(19-len(user))
            for task in task_list:
                if task['username'] == user:
                    user_task += 1
                    if task['completed'] == True:
                        user_completed_tasks += 1
                    elif datetime.date(task['due_date']) < date.today() and task['completed'] == False:
                        user_overdue += 1 
            
            if user_task > 0:
                user_percentage_of_total_tasks = round((user_task/num_tasks)*100,2)
                user_percentage_completed = round(user_completed_tasks/user_task*100,2)
                user_percentage_uncomleted = round((user_task-user_completed_tasks)/user_task*100,2)
                user_percentage_overdue = round(user_overdue/user_task*100,2)
            else:
                user_percentage_of_total_tasks = 0
                user_percentage_completed = 0
                user_percentage_uncomleted = 0
                user_percentage_overdue = 0 
            
            #Filling in the table with results.
            user_report_str +=f"|     {user_task}     |"    
            user_report_str += f" " * (10-len(str(user_percentage_of_total_tasks)))
            user_report_str += f"{user_percentage_of_total_tasks} |"
            
            user_report_str += f" " * (9-len(str(user_percentage_completed)))
            user_report_str +=f" {user_percentage_completed} |"
            
            user_report_str += f" " * (9-len(str(user_percentage_uncomleted)))
            user_report_str +=f" {user_percentage_uncomleted}     |"
            
            user_report_str += f" " * (9-len(str(user_percentage_overdue)))
            user_report_str +=f" {user_percentage_overdue} |\n"
        user_report_str += f"-------------------------------------------------------------------------------------\n"

        #Saving report to the file.
        user_overview.write(user_report_str)
        print('User report generated and saved to the file \"user_overview.txt\" succesfully.')        
     

def view_mine():
    '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling)
    '''
    #Displaying the tasks assigned to the logged user
    for t in task_list:
        if t['username'] == curr_user:
            print(f"Task number: \t\t {task_list.index(t)}")
            
            disp_str = f"Task: \t\t\t {t['title']}\n"
            disp_str += f"Assigned to: \t\t {t['username']}\n"
            disp_str += f"Date Assigned: \t\t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t\t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \t {t['description']}\n"
            disp_str += f"Task Completed: \t {'Yes' if t['completed'] else 'No'}\n"
            print(disp_str)
    
    #Asking user to choose option
    while True:
        try:
            sel_task = int(input("\nPlease enter number of the task you wish to edit or -1 to exit: "))
        
            #If user enters -1 returns to the menu.
            if sel_task == -1:
                break

            #Checking if chosen task number is correct
            elif sel_task > task_list.index(t) or task_list[sel_task]['username'] != curr_user:
                print('Wrong number. Please choose your task!')
        
            #Checking if task is completed
            elif task_list[sel_task]['username'] == curr_user and task_list[sel_task]['completed'] == True:
                print('You can\'t edit task that is completed.')
            else:
                if task_list[sel_task]['username'] == curr_user:
                    while True:
                        q1 = str.lower(input('Press [E] for edit or [C] to mark the task as completed : '))
                        if q1 == 'e':
                            while True:
                                new_username = input('Enter the username: ')
                                if new_username not in username_password.keys():
                                    print('User does not exist. Please enter a valid username.')
                                    pass
                                else:
                                    task_list[sel_task]['username'] = new_username
                                    break
                            task_list[sel_task]['title'] = input('Please enter the title of the task: ')
                            task_list[sel_task]['description'] = input('Please enter the description of the task: ')
                            while True:
                                try:
                                    new_due_date = input('Enter the new due date of the task (YYYY-MM-DD): ')
                                    new_due_date_time = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                                    task_list[sel_task]['due_date'] = new_due_date_time
                                    break
                                except ValueError:
                                    print('Invalid datetime format. Please use the format speciefied')
                            save_cahnges()
                            print("Task edited succesfully!")
                            break
                        elif q1 == 'c':
                            task_list[sel_task]['completed'] = True
                            save_cahnges()
                            print('Task marked as completed.')
                            break
                        else:
                            print('Wrong letter! Try again')
                break
        except ValueError:
            print('That\'s not a number. Please choos number!')

def display_stats():
    #Function to display statistics only for admin user.
    if curr_user == "admin":
        if not os.path.exists("tasks.txt"):
            generate_report()      
        with open("task_overview.txt", 'r') as to:
            report_data = to.read()
            print("\n TASKS STATISTICS\n******************\n")
            print(report_data)
        
        if not os.path.exists("user.txt"):
            generate_report()            
        with open("user_overview.txt", 'r') as uo:
            report_user = uo.read()
            print("\n USERS STATISTICS\n******************\n")
            print(report_user)
    else:
        print("This user can't see statistics")
        
def save_cahnges():
    #Additional function to save changes while editing or marking task completed
    with open("tasks.txt", "w") as edited_task_file:
        edited_task_list_to_write = []
        for t3 in task_list:
            edited_str_attrs = [
                t3['username'],
                t3['title'],
                t3['description'],
                t3['due_date'].strftime(DATETIME_STRING_FORMAT),
                t3['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t3['completed'] else "No"
            ]
            edited_task_list_to_write.append(";".join(edited_str_attrs))
        edited_task_file.write("\n".join(edited_task_list_to_write))

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;qwerty")

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


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()
            
    elif menu == 'gr':
        generate_report()

    elif menu == 'vm':
        view_mine()
    
    elif menu == 'ds':
        display_stats()
        
    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
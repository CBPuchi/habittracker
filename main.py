import sys
from datetime import datetime

import questionary
import analyze
import initialize
from period import Period
from habit import Habit

"""
This is the start of th habit tracker. It includes the menu and the navigation

It imports the library 'questionary' as the Command Line Interface (CLI) that guides the user through the program
as well as checks the user input.
It also imports the initialisation.py doc which launches the core functionalities of the program.
"""

#Start program with the introdcution
intro_message = "\n******************************\n" \
                "Welcome to Habit Tracker!\n" \
                "You can use this app to track your habits for a better coordinated life.\n" \
                "******************************\n"
print(intro_message)

test_data_message = ("\nStart with an empty DB\n"\
                     "Or start with testdata for the user Tick, Trick and Track\n"\
                    "The creation of the data may take some time - 2-3 min\n" \
                    "Afterwards you can use one of these users or create your own new user\n" \
                    "Or work with an existing DB\n")
print(test_data_message)
intro_testdata_question = questionary.select(
    "How do you want to start?", choices=[
        "Empty DB",
        "DB with Testdata",
        "Existing DB",
    ]).ask()
if intro_testdata_question == "Empty DB":
    initialize.launch_db()

elif intro_testdata_question == "DB with Testdata":
    initialize.launch_db()
    # insert example data
    initialize.insert_example_data_into_db()

#Ask the user to register or login
first_question = questionary.select(
    "\nIs this your first time here => register or have you been here before => login? ", choices=[
        "Register",
        "Login"
    ]).ask()

#login has been chosen, call the login function
#a valid return value of the login function is "exit", than the habit tracker is left
if first_question == "Login":
    user = initialize.login()
    if user == "Exit":
        sys.exit()
    else:
        print("Welcome back! " + user.name )

#Register has been chosen, call the register function
elif first_question == "Register":
    print("Your are new here. Please enter a name")
    user= initialize.register_user()
    user.choose_predefined_habits()

#the main menu for the user
def menu(user):
    """
    the user is asked, what he wants to do next
    He has got the choice between update the name of the user
    create, update, delete or complete a habit, her a submenu is started
    get a habit overview
    view statistics
    or exit the habit tracker
    """
    menu_question = questionary.select("\nWhat do you want to do next?",
                                       choices=["Update user",
                                                "Habits overview",
                                                "Create, update, delete or complete a habit",
                                                "View statistics",
                                                "Delete your account",
                                                "Exit programm"
                                               ]).ask()

    if menu_question == "Update user":
        """update y user name """
        print("\nLet's change the name of your user")
        print("\nYour current name is:" + user.name)
        new_name = questionary.text("\nWhat's your new name: ").ask()
        user.update(new_name)
        menu(user)

    elif menu_question == "Create, update, complete or delete a habit ":
        """choose habit acitivities"""
        habit_question = questionary.select("\nDo you want to: ",
                                            choices=[
                                                "Create a new habit",
                                                "Update an existing habit",
                                                "Mark a habit as completed",
                                                "Delete habit"
                                            ]).ask()
        if habit_question == "Create a new habit":
            """enter a name and period and the habit is created """
            habit_name = questionary.text("\nType in the name of the habit: ",
                                          validate=lambda text: True if len(text) > 0 and text.isalpha()
                                          else "Please enter a correct value. "
                                               "Your habit name should only contain upper and lowercase letters.").ask()
            chosen_period =questionary.select("\nDo you want to do the habit daily or weekly?",
                                           choices=["daily", "weekly"]).ask()
            period = Period[chosen_period].value
            new_habit = Habit(habit_name, period, user.userid)
            new_habit.save()

        elif habit_question == "Delete habit":
            """choose a habit by name and  change the name. This is deleted """
            habit_name = questionary.text("\nWhich habit do you want to delete - enter the name?").ask()
            habits = user.get_habits()
            del_habit = next((habit for habit in habits if habit.name == habit_name), None)
            if del_habit:
                del_habit.delete()
                print("\nThe habit: " + del_habit.name + " is deleted.")
            else:
                print("\nA habit with this name is unknown")

        elif habit_question == "Update an existing habit":
            """choose a habit by name and  change the name or period of it"""
            habit_name = questionary.text("\nWhich habit do you want to change - enter the name?").ask()
            habits = user.get_habits()
            if habits:
                change_habit = next((habit for habit in habits if habit.name == habit_name), None)
                if change_habit:
                    new_name = questionary.text("\nWhich should be the new name : ").ask()
                    chosen_period = questionary.select("\nShould the period be daily or weekly?",
                                                       choices=["daily", "weekly"]).ask()
                    period = Period[chosen_period].value
                    change_habit.update(new_name, period)
                else:
                    print("\nA habit with this name is unknown")
            else:
                print("\nThere are no habits to change")

        elif habit_question == "Mark a habit as completed":
            """mark a habit as completed"""
            habit_name = questionary.text("\nWhich habit do you want to complete - enter the name?").ask()
            complete_habit = user.get_habit(habit_name)
            if complete_habit:
                date_str = (questionary.text("\nEnter the completion date (YYYY-mm-dd)").ask())
                compl_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                exec_status= complete_habit.complete(compl_date)
                if exec_status !="ok":
                    print("\n" + exec_status)
                    print("\n retry")
            else:
                print("\nA habit with this name is unknown")
        else:
            """unexpected entry """
            print("\nHow could you enter " + habit_question + "?")

        menu(user)

    elif menu_question == "Habits overview":
        """all habits of the current user are listed
        in a second step the user is asked, if he wants to see the completion dates of one habit"""
        habits = user.get_habits()
        print("\nYour habits overview")
        for habit in habits:
            habit.print_readable()
        watch_completiondates = questionary.select("\nDo you want to see the completion dates of one habit?",
                                                choices=["yes", "no"]).ask()
        if watch_completiondates == "yes":
            habit_name = questionary.text("\nEnter name of habit to see its completion dates?").ask()
            l_habit = user.get_habit(habit_name)
            l_habit.print_completion_dates()

        menu(user)

    elif menu_question == "View statistics":
        """analyze your habit and activities"""
        analyze_question = questionary.select("Do you want to: ",
                                            choices=[
                                                "List one habit",
                                                "Your longest streak of all",
                                                "Your longest streak of habit",
                                                "Current completion status",
                                                "All of one period"
                                            ]).ask()
        if analyze_question == "List one habit":
            habit_name = questionary.text("\nWhich habit do you want to see").ask()
            l_habit = user.get_habit(habit_name)
            l_habit.print_complete_habit()

        elif analyze_question == "Your longest streak of all":
            """find the habit with the longeste streak"""
            analyze.longest_streak(user)

        elif analyze_question == "Your longest streak of habit":
            """check for a given habit-name the longest streak """
            habit_name = questionary.text("\nWhich habit do you want to see? (enter a name)").ask()
            l_habit = user.get_habit(habit_name)
            if l_habit:
                print("\nThe longest streak of the habit " + habit_name + " is : "
                + str(l_habit.longestStreak) +" with the Period: " + Period(l_habit.period).name + "\n" )
            else:
                print("A habit with this name doesn't exist: " + habit_name + "\n" )

        elif analyze_question == "Current completion status":
            """ check for all habits of one user, the current completion status"""
            analyze.current_completion_status(user)

        elif analyze_question == "All of one period":
            """list all habits with the same period"""
            analyze.all_of_one_period(user, )

        else:
            """unexpected entry """
            print("\nHow could you enter " + analyze_question + "?")

        menu(user)


    elif menu_question == "Delete your account":
        """delete the user with all of his habit and completiondates """
        habits = user.get_habits()
        for habit in habits:
            habit.delete()
        user.delete()
        print("\nYour user and his habits have been deleted.")
    else:
        sys.exit()

#call the main menu to continue
menu(user)
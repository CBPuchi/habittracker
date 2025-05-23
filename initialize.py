"""
This document organises the basic functionality of our database and creates it if it does not already exist.
Furthermore, this code deals with the creation of a user profile (registration)
"""

from datetime import date, timedelta
import habittrackerdb
import questionary
from user import User
from habit import Habit
from period import Period


""" Launch the database
#The database consist of three tables:
# 1. user for the user data
# 2. habit for the habits of each user data eg. name and period
# 3. completion for hte completiondates of each habit
"""
def launch_db():
    db=habittrackerdb.HabitTrackerDB()
    db.clean_db()


# This function is to register a new user to the app
def register_user():
    """
    The user can enter his name, only alphabetic are allowed
    If the name already exists in the  database, the user is asked for y new name
    The name ist saved in the database and an userid ist returned
    """
    db = habittrackerdb.HabitTrackerDB()
    name = questionary.text("What is your name?",
        validate=lambda text: True if len(text) > 0 and text.isalpha()
        else "Please enter a correct value. Your name should only contain upper and lowercase letters.").ask()
    user= db.read_user_by_name(name)
    if user is None:
        newuserid = db.save_user(name)
        user = User(name, newuserid)
        print("\nRegistration successful!\n")
        return user
    else:
        print("\nThis user already exists. Please choose a different name!\n")
        register_user()

# login for registered user
def login():
    """
    ask for the name and read the user
    if no user is found return None
    """
    db = habittrackerdb.HabitTrackerDB()
    entered_val = questionary.text("Enter your username(alphanumeric) or your userid(numeric): ").ask()
    entered_name_typ = type(entered_val)
    if entered_name_typ == int:
        user_values = db.read_user_by_id(entered_val)
    else:
        user_values= db.read_user_by_name(entered_val)
    if user_values:
        user = User(user_values[1], user_values[0])
        return user
    else:
        print("\nSomething went wrong. User " + entered_val +" is not found!\n")
        login_question = questionary.select(
                "\nYou want to retry or exit? ", choices=[
                    "Login",
                    "Exit"
                ]).ask()
        if login_question == "Login":
            login()
        else:
            print("\n exiting habit tracker")
            return "Exit"

#create testdata in DB
def insert_example_data_into_db():

    """ create three user"""
    user1 = User("Tick")  # Initialize User with name "Tick"
    user1.save()
    user2 = User("Trick")  # Initialize User with name "Trick"
    user2.save()
    user3 = User("Track")  # Initialize User with name "Track"
    user3.save()

    """add habits and completion dates for Tick"""
    nh1 = Habit("Playing soccer", Period.weekly.value, user1.userid)
    nh1.save()
    nh1.complete(date.today() - timedelta(days=27))
    nh1.complete(date.today() - timedelta(days=19))
    nh1.complete(date.today() - timedelta(days=14))
    nh1.complete(date.today() - timedelta(days=7))
    nh1.complete(date.today() - timedelta(days=1))

    nh2 = Habit("Reading", Period.daily.value, user1.userid)
    nh2.save()
    for x in range(30, 0, -1 ):
        nh2.complete(date.today() - timedelta(days= x))

    nh3 = Habit("Helping Donald", 1, user1.userid)
    nh3.save()
    nh3.complete(date.today() - timedelta(days=28))
    nh3.complete(date.today() - timedelta(days=27))
    nh3.complete(date.today() - timedelta(days=26))
    nh3.complete(date.today() - timedelta(days=25))
    nh3.complete(date.today() - timedelta(days=22))
    nh3.complete(date.today() - timedelta(days=21))
    nh3.complete(date.today() - timedelta(days=19))
    nh3.complete(date.today() - timedelta(days=18))
    nh3.complete(date.today() - timedelta(days=17))
    nh3.complete(date.today() - timedelta(days=16))
    nh3.complete(date.today() - timedelta(days=15))
    nh3.complete(date.today() - timedelta(days=14))
    nh3.complete(date.today() - timedelta(days=13))
    nh3.complete(date.today() - timedelta(days=10))
    nh3.complete(date.today() - timedelta(days=9))
    nh3.complete(date.today() - timedelta(days=8))
    nh3.complete(date.today() - timedelta(days=7))
    nh3.complete(date.today() - timedelta(days=5))
    nh3.complete(date.today() - timedelta(days=2))
    nh3.complete(date.today() - timedelta(days=1))
    nh3.complete(date.today())

    nh4 = Habit("Scout meeting", Period.weekly.value, user1.userid)
    nh4.save()
    nh4.complete(date.today() - timedelta(days=29))
    nh4.complete(date.today() - timedelta(days=22))
    nh4.complete(date.today() - timedelta(days=15))
    nh4.complete(date.today() - timedelta(days=8))
    nh4.complete(date.today() - timedelta(days=1))


    nh5 = Habit("Visiting Dagobert", Period.weekly.value, user1.userid)
    nh5.save()
    nh5.complete(date.today() - timedelta(days=30))
    nh5.complete(date.today() - timedelta(days=23))
    nh5.complete(date.today() - timedelta(days=16))
    nh5.complete(date.today() - timedelta(days=9))
    nh5.complete(date.today() - timedelta(days=2))

    """ add habits and completion dates for Trick"""
    nh1 = Habit("Playing soccer", Period.weekly.value, user2.userid)
    nh1.save()
    nh1.complete(date.today() - timedelta(days=28))
    nh1.complete(date.today() - timedelta(days=23))
    nh1.complete(date.today() - timedelta(days=18))
    nh1.complete(date.today() - timedelta(days=12))
    nh1.complete(date.today() - timedelta(days=4))

    nh2 = Habit("Reading", Period.daily.value, user2.userid)
    nh2.save()
    nh2.complete(date.today() - timedelta(days=29))
    nh2.complete(date.today() - timedelta(days=28))
    nh2.complete(date.today() - timedelta(days=27))
    nh2.complete(date.today() - timedelta(days=26))
    nh2.complete(date.today() - timedelta(days=23))
    nh2.complete(date.today() - timedelta(days=22))
    nh2.complete(date.today() - timedelta(days=20))
    nh2.complete(date.today() - timedelta(days=19))
    nh2.complete(date.today() - timedelta(days=18))
    nh2.complete(date.today() - timedelta(days=17))
    nh2.complete(date.today() - timedelta(days=16))
    nh2.complete(date.today() - timedelta(days=15))
    nh2.complete(date.today() - timedelta(days=14))
    nh2.complete(date.today() - timedelta(days=11))
    nh2.complete(date.today() - timedelta(days=10))
    nh2.complete(date.today() - timedelta(days=9))
    nh2.complete(date.today() - timedelta(days=8))
    nh2.complete(date.today() - timedelta(days=6))
    nh2.complete(date.today() - timedelta(days=4))
    nh2.complete(date.today() - timedelta(days=2))
    nh2.complete(date.today() - timedelta(days=1))

    nh3 = Habit("Helping Donald", Period.daily.value, user2.userid)
    nh3.save()
    for x in range(30,0,1):
        nh3.complete(date.today() - timedelta(days=x))

    nh4 = Habit("Scout meeting", Period.weekly.value, user2.userid)
    nh4.save()
    nh4.complete(date.today() - timedelta(days=29))
    nh4.complete(date.today() - timedelta(days=22))
    nh4.complete(date.today() - timedelta(days=15))
    nh4.complete(date.today() - timedelta(days=8))
    nh4.complete(date.today() - timedelta(days=1))

    nh5 = Habit("Visiting Dagobert", Period.weekly.value, user2.userid)
    nh5.save()
    nh5.complete(date.today() - timedelta(days=30))
    nh5.complete(date.today() - timedelta(days=23))
    nh5.complete(date.today() - timedelta(days=16))
    nh5.complete(date.today() - timedelta(days=9))
    nh5.complete(date.today() - timedelta(days=2))

    """ add habits and completion dates for Track"""
    nh1 = Habit("Playing soccer", Period.weekly.value, user3.userid)
    nh1.save()
    nh1.complete(date.today() - timedelta(days=29))
    nh1.complete(date.today() - timedelta(days=22))
    nh1.complete(date.today() - timedelta(days=15))
    nh1.complete(date.today() - timedelta(days=8))
    nh1.complete(date.today() - timedelta(days=1))

    nh2 = Habit("Reading", Period.daily.value, user3.userid)
    nh2.save()
    for x in range(30, 0,-1):
        nh2.complete(date.today() - timedelta(days=x))

    nh3 = Habit("Helping Donald", Period.daily.value, user3.userid)
    nh3.save()
    for x in range(31, 2, -1 ):
        nh3.complete(date.today() - timedelta(days=x))

    nh4 = Habit("Scout meeting", Period.weekly.value, user3.userid)
    nh4.save()
    nh4.complete(date.today() - timedelta(days=29))
    nh4.complete(date.today() - timedelta(days=22))
    nh4.complete(date.today() - timedelta(days=15))
    nh4.complete(date.today() - timedelta(days=8))
    nh4.complete(date.today() - timedelta(days=1))

    nh5 = Habit("Visiting Dagobert", Period.weekly.value, user3.userid)
    nh5.save()
    nh5.complete(date.today() - timedelta(days=30))
    nh5.complete(date.today() - timedelta(days=23))
    nh5.complete(date.today() - timedelta(days=16))
    nh5.complete(date.today() - timedelta(days=9))
    nh5.complete(date.today() - timedelta(days=2))

import questionary
import habittrackerdb
from habit import Habit

""" Definition of class User
The name and userid of the user are persisted
"""
class User:

    #init a user and set DB
    def __init__(self, name: str, userid=None):
        self.name = name
        self.userid = userid
        self.db = habittrackerdb.HabitTrackerDB()

    #print values of user
    def __str__(self):
        return f'name:{self.name}; ID:{self.userid}'

    def update(self, pName:str):
        """The name of a user can be changed"""
        self.name = pName
        self.db.update_user(pName, self.userid)

    def save(self):
        """ save the user"""
        id = self.db.save_user(self.name)
        self.userid = id

    def delete(self):
        """ delete the user"""
        self.db.delete_user(self.userid)

    def get_habits(self):
        """read all habits of the user"""
        habits = self.db.read_list_of_habits(self.userid)
        return habits

    def get_habit(self,name):
        """read one habit of user by name"""
        habit = self.db.read_one_habit_name(self.userid, name)
        return habit

    def choose_predefined_habits(self):
        """if a user has no habits, he is new user must choose the first habit of a predefined list"""
        habits = self.db.read_list_of_habits(self.userid)
        """if no habits exist, the user has to choose one habit out of the predefined habits"""
        if (len(habits) == 0):
            print("Welcome " + self.name + " - since you are new , you can choose your first habit:")
            first_habit = questionary.confirm("Running (weekly)").ask()
            second_habit = questionary.confirm("Singing (daily)").ask()
            third_habit = questionary.confirm("Swimming (weekly)").ask()
            fourth_habit = questionary.confirm("Tea time (daily)").ask()
            fifth_habit = questionary.confirm("Yoga (daily)").ask()

        if first_habit:
            newhabit1 = Habit('Running', 7, self.userid)
            newhabit1.save()

        else:
            pass

        if second_habit:
            newhabit2 = Habit('Singing', 1, self.userid)
            newhabit2.save()
        else:
            pass

        if third_habit:
            newhabit3 = Habit('Swimming', 7, self.userid)
            newhabit3.save()
        else:
            pass

        if fourth_habit:
            newhabit4 = Habit('Tea time', 1, self.userid)
            newhabit4.save()
        else:
            pass

        if fifth_habit:
            newhabit5 = Habit('Yoga', 1, self.userid)
            newhabit5.save()

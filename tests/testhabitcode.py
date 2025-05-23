from datetime import timedelta, date
from tokenize import endpats

import habittrackerdb
from user import User
from habit import Habit, Period

class TestHabitcode:

    def setup_method(self):
        """Setup before each test method."""
        self.db = habittrackerdb.HabitTrackerDB()
        user = self.db.read_user_by_name("Tick")

    def test_readcompletiondates(self):
        compl_dates = self.db.read_list_of_completions(1)
        for compl_date in compl_dates:
            print(compl_date)

    def test_complete_habit_found(self):
        user = User("Susi", 1)
        complete_habit = user.get_habit("yoga")
        if complete_habit:
            print("Found")
            print(complete_habit)
        else:
            print("Not found")

    def test_complete_habit(self):
        user = User("Tim", 1)
        complete_habit = user.get_habit("Swimming")
        complete_habit.complete(date(2025, 4, 10))

    def teardown_method(self):
        pass
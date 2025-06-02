import pytest
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import habittrackerdb
import analyze
import initialize
import period
from user import User
from period import Period

class TestAnalyze:

    def setup_method(self):
        """Setup before each test method."""
        self.db = habittrackerdb.HabitTrackerDB()


    def test_prepare_DB(self):
        """initialize DB for test with user Pauline"""
        self.db.clean_db()
        initialize.insert_example_data_into_db()
        pass

    def test_longest_streak(self):
        userValues = self.db.read_user_by_name("Tick")
        user = User(userValues[1], userValues[0])
        analyze.longest_streak(user)

    def test_current_completion_status(self):
        userValues = self.db.read_user_by_name("Tick")
        user = User(userValues[1], userValues[0])
        analyze.current_completion_status(user)

    def test_all_of_one_period(self):
        userValues = self.db.read_user_by_name("Tick")
        user = User(userValues[1], userValues[0])
        analyze.all_of_one_period(user, Period.daily.value)
        analyze.all_of_one_period(user, Period.weekly.value)
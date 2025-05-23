import freezegun
import pytest
from datetime import timedelta, date, datetime
import habittrackerdb
from user import User
from habit import Habit, Period


class TestHabit:
    def setup_method(self):
        """Setup before each test method."""
        self.db = habittrackerdb.HabitTrackerDB()
        user = self.db.read_user_by_name("Pauline")


    def test_prepare_DB(self):
        """initialize DB for test with user Pauline"""
        self.db.clean_db()
        self.db._initialize_db()
        user = User('Pauline')
        user.save()

    def test_create_habits(self):
        """read user Pauline and create habits"""
        userValues = self.db.read_user_by_name("Pauline")
        """create three habits for Pauline and save them"""
        habit1 = Habit('running', Period.weekly.value, userValues[0])
        habit1.save()
        assert habit1.habitid == 1

        habit2 = Habit('singing', Period.weekly.value, userValues[0])
        habit2.save()
        assert habit2.habitid == 2

        habit3 = Habit('coffee break', Period.daily.value, userValues[0])
        habit3.save()
        assert habit3.habitid == 3

    def test_read_habits(self):
        """read user Pauline and her habits"""
        userValues = self.db.read_user_by_name("Pauline")
        user1 = User(userValues[1], userValues[0])
        """read all habit of user Pauline"""
        list_of_habits =user1.get_habits()
        assert len(list_of_habits) == 3
        assert list_of_habits[0].habitid == 1
        assert list_of_habits[0].name == 'running'
        assert list_of_habits[1].habitid == 2
        assert list_of_habits[1].name == 'singing'
        assert list_of_habits[2].habitid == 3
        assert list_of_habits[2].name == 'coffee break'

    def test_update_habit(self):
        """read user Pauline and update habits"""
        userValues = self.db.read_user_by_name("Pauline")
        user1 = User(userValues[1], userValues[0])
        """read habit 1 of user"""
        habit = self.db.read_one_habit_name(user1.userid, "running")
        assert habit.name == "running"
        assert habit.period == Period.weekly.value
        """change habit to tea time every week"""
        habit.update("tea time", Period.weekly.value)
        assert habit.name == "tea time"
        assert habit.period == Period.weekly.value
        """change the period of tea time to every day"""
        habit.update("tea time", Period.daily.value)
        assert habit.period == Period.daily.value

    def test_delete_habit(self):
        """read user Pauline and delete habits"""
        userValues = self.db.read_user_by_name("Pauline")
        user1 = User(userValues[1], userValues[0])
        """read habit 3 of user Pauline"""
        habit = self.db.read_one_habit_id(user1.userid, 3)
        habit.delete()
        habit = self.db.read_one_habit_id(user1.userid, 3)
        assert habit is None

    def test_complete_habits(self):
        """read user Pauline and complete habits"""
        userValues = self.db.read_user_by_name("Pauline")
        user1 = User(userValues[1], userValues[0])
        """read habit no 1 of user Pauline"""
        habit = self.db.read_one_habit_id(user1.userid, 1)
        """add 5 completion dates in a row for habit no 1"""
        habit.complete(date(2025, 3, 2))
        habit.complete(date(2025, 3, 3))
        habit.complete(date(2025, 3, 4))
        habit.complete(date(2025, 3, 5))
        habit.complete(date(2025, 3, 6))
        assert len(habit.getCompletionDates()) == 5
        assert (habit.getCompletionDates()[0] == datetime.strptime('2025-03-02', '%Y-%m-%d').date())
        """check for current and longest streak"""
        assert habit.longestStreak == 5
        assert habit.currentStreak == 5

    def test_complete_twostreaks(self):
        """read user Pauline and check streaks"""
        userValues = self.db.read_user_by_name("Pauline")
        user1 = User(userValues[1], userValues[0])
        """read habit no 1 of user Pauline"""
        habit = self.db.read_one_habit_id(user1.userid, 1)
        list_of_compldates = habit.getCompletionDates()
        assert len(list_of_compldates) == 5
        assert (list_of_compldates[0] ==datetime.strptime('2025-03-02', '%Y-%m-%d').date())
        assert (list_of_compldates[1] == datetime.strptime('2025-03-03', '%Y-%m-%d').date())

        """delete all completionDate of habit no 1"""
        self.db.delete_completion(habit)
        list_of_compldates = habit.getCompletionDates()
        assert len(list_of_compldates) == 0

        """create new completionDates with gap to test current and longest streak"""
        habit.complete(date(2025, 3, 2))
        habit.complete(date(2025, 3, 3))
        habit.complete(date(2025, 3, 4))
        habit.complete(date(2025, 3, 5))
        habit.currentStreak = 4
        habit.longestStreak = 4
        print(habit)
        habit.complete(date(2025, 3, 7))
        habit.complete(date(2025, 3, 8))
        assert habit.currentStreak == 2
        assert habit.longestStreak == 4
        print(habit)
        """try to add completion date < latest completion date"""
        assert(habit.complete(date(2025, 3, 6)) == 'DateAlreadyCompleted: 2025-03-06')

    @freezegun.freeze_time("2025-03-11")
    def test_check_completionStatus(self):
        """read user Pauline and check the completion status of her habits"""
        userValues = self.db.read_user_by_name("Pauline")
        user1 = User(userValues[1], userValues[0])
        """read habit no 1 of user Pauline"""
        habit = self.db.read_one_habit_id(user1.userid, 1)

        """delete all completionDate of habit no 1"""
        self.db.delete_completion(habit)

        """create new completionDates to check if current streak is ongoing"""
        habit.complete(date(2025, 3, 2))
        habit.complete(date(2025, 3, 3))
        habit.complete(date(2025, 3, 4))
        habit.complete(date(2025, 3, 6))
        assert(habit.checkCompletionStatus()) == 'streak -  tea time -  has been broken. Never mind restart it!'
        habit.complete(date(2025, 3, 7))
        habit.complete(date(2025, 3, 8))
        habit.complete(date(2025, 3, 9))
        habit.complete(date(2025, 3, 10))
        assert(habit.checkCompletionStatus()) =='Friendly reminder: streak - tea time - needs to be done'
        habit.complete(date.today())
        assert(habit.checkCompletionStatus()) == 'streak - tea time - is completed today'

    def test_delete_habit_with_completion(self):
        """read user Pauline and delete all habits with completion dates"""
        userValues = self.db.read_user_by_name("Pauline")
        user1 = User(userValues[1], userValues[0])
        """read habit no 1 of user Pauline"""
        habit = self.db.read_one_habit_id(user1.userid, 2)
        assert (habit.name) == 'singing'
        habit.complete(date.today() - timedelta(days=1))
        habit.complete(date.today())
        assert(len(habit.getCompletionDates())) == 2
        """delete completiondates of habit no 2"""
        self.db.delete_completion(habit)
        assert (self.db.read_list_of_completions(habit.habitid)) == []
        """delete habit no 2"""
        habit.delete()
        assert (self.db.read_one_habit_id(user1.userid, 2)) == None

    def teardown_method(self):
        self.habit = None

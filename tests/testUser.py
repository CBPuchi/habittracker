import pytest
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import habittrackerdb
from user import User


class TestUser:

    def setup_method(self):
        """Setup before each test method."""
        self.db = habittrackerdb.HabitTrackerDB()

    def test_save_user(self):
        #start with empty database
        self.db.clean_db()
        self.db._initialize_db()

        #create two user and save
        self.user1 = User("Peter")  # Initialize User with name "Peter
        self.user2 = User("Pauline")  # Initialize User with name "Pauline"
        self.user1.save()
        assert self.user1.userid == 1
        self.user2.save()
        assert self.user2.userid == 2

    def test_read_user_by_id(self):
        # read two user with their ID
        userValues = self.db.read_user_by_id(1)
        assert userValues[0] == 1
        assert userValues[1] == "Peter"
        user1 = User(userValues[1], userValues[0])
        assert user1.userid == 1
        assert user1.name == "Peter"

        userValues = self.db.read_user_by_id(2)
        assert userValues[0] == 2
        assert userValues[1] == "Pauline"
        user2 = User(userValues[1], userValues[0])
        assert user2.userid == 2
        assert user2.name == "Pauline"

        userValues = self.db.read_user_by_id(3)
        assert userValues == None


    def test_read_user_by_name(self):
        # read two user with their name
        userValues = self.db.read_user_by_name("Peter")
        assert userValues[0] == 1
        assert userValues[1] == "Peter"
        user1 = User(userValues[1], userValues[0])
        assert user1.userid == 1
        assert user1.name == "Peter"

        userValues = self.db.read_user_by_name("Pauline")
        assert userValues[0] == 2
        assert userValues[1] == "Pauline"
        user2 = User(userValues[1], userValues[0])
        assert user2.userid == 2
        assert user2.name == "Pauline"

        userValues = self.db.read_user_by_name("Paula")
        assert userValues == None

        #save two user with the same name
        self.user3 = User("Paul")
        self.user3.save()
        self.user4 = User("Paul")
        self.user4.save()
        #read by name and return number of found users
        userValues = self.db.read_user_by_name("Paul")
        assert userValues > 1


    def test_update(self):
        #Test updating the name.
        userValues = self.db.read_user_by_name("Pauline")
        user1 = User(userValues[1], userValues[0])
        assert user1.userid == 2
        assert user1.name == "Pauline"
        user1.update("Paula")
        #read again Pauline, not found
        userValues = self.db.read_user_by_name("Pauline")
        assert userValues == None

        # read Paula and found with new name
        userValues = self.db.read_user_by_name("Paula")
        assert userValues[0] == 2
        assert userValues[1] == "Paula"

    def test_delete(self):
        userValues = self.db.read_user_by_id(1)
        if userValues:
            user1= User(userValues[1], userValues[0])
            user1.delete()
        userValues = self.db.read_user_by_id(1)
        assert userValues == None

    def teardown_method(self):
        self.user = None

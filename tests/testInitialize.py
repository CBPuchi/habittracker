import pytest

import habittrackerdb
import initialize
import user
from user import User
from datetime import date

class TestInitialize:

    def setup_method(self):
        """Setup before each test method."""
        self.db = habittrackerdb.HabitTrackerDB()

    def test_register_user(self):
        # start with empty database
        self.db.clean_db()
        self.db._initialize_db()
        user = self.db.read_user_by_name("Tom")
        if user is None:
            newuserid = self.db.save_user("Tom")
            user = User("Tom", newuserid)
        assert user.userid == 1
        assert user.name == "Tom"

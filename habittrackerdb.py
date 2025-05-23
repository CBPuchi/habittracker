import sqlite3
import os

from datetime import datetime
from habit import Habit


class HabitTrackerDB:
    """define the path of the database"""
    DB_PATH = os.path.join(os.path.dirname(__file__), 'habittracker.db')

    def __init__(self):
           self._initialize_db()


    """
    The database consists of three tables:
    user --> for all user data
    habit --> for all habits across all users
    completion --> for the completionsdate of all habits
    The tables are created, if they not exist yet
    """
    def _initialize_db(self):
        conn = sqlite3.connect(self.DB_PATH)
        curs = conn.cursor()

        curs.execute("""
             create table if not exists user(
             userid integer primary key autoincrement,
             username text not null);
            """)

        curs.execute("""
            create table if not exists habit(
             habitid integer primary key autoincrement,
             name text not null,
             period integer not null,
             creationdate timestamp not null,
             currentstreak integer not null,
             longeststreak integer not null,
             userid integer not null,
            foreign key (userid) references user(userid));
            """)

        curs.execute("""
             create table if not exists completion(
                completiondate date not null,
                habitid integer not null,
                PRIMARY KEY(completiondate, habitid),
                FOREIGN key (habitid) references habit(habitid));
            """)
        conn.commit()
        conn.close()

    """
    clean the database and drop all three tables
    users --> for all user data
    habits --> for all habits across all users
    progress --> for all progress data across users
    """
    def clean_db(self):
        conn = sqlite3.connect(self.DB_PATH)
        curs = conn.cursor()
        curs.execute("""
               drop table if exists completion;
               """)

        curs.execute("""
                drop table if exists habit;
                """)

        curs.execute("""
                    drop table if exists user;
                   """)
        conn.commit()
        conn.close()

    """save a user with the given name and return the new userid"""
    def save_user(self, name: str):
        conn = sqlite3.connect(self.DB_PATH)
        curs = conn.cursor()
        curs.execute('''INSERT INTO user(username) VALUES (?)''', (name,))
        userid  = curs.lastrowid
        conn.commit()
        conn.close()
        return userid

    """find a user with the userid and return the userid and name"""
    def read_user_by_id(self, puserid):
        conn = sqlite3.connect(self.DB_PATH)
        curs = conn.cursor()
        curs.execute('''select userid, username from user where userid= ?''', (puserid,))
        uservalues = curs.fetchone()
        conn.commit()
        conn.close()
        # if a user ist found, return a dictionary with data
        # else return none
        if uservalues:
            return uservalues
        else:
            return None

    """find a user with his name and return the userid and name or an error"""
    def read_user_by_name(self, pname):
        conn = sqlite3.connect(self.DB_PATH)
        curs = conn.cursor()
        curs.execute('''select userid, username from user where username= ?''', (pname,))
        list_of_users = curs.fetchall()
        conn.commit()
        conn.close()
        """if more than one user ist found, return number of found user
        if one use is found return the userid and name of this user
        or return none, if nothing is found
        """
        if len(list_of_users) > 1:
            return len(list_of_users)
        elif len(list_of_users) == 1:
            uservalues  = list_of_users[0]
            return uservalues
        else:
            return None

    """update the name of a user, he is identified with his userid"""
    def update_user(self, name: str, id: int):
        conn = sqlite3.connect(self.DB_PATH)
        curs = conn.cursor()
        curs.execute('''update user set username= ? where userid= ?''', (name,id,))
        conn.commit()
        conn.close()

    """delete a user from DB with his userid"""
    def delete_user(self, id: int):
        conn = sqlite3.connect(self.DB_PATH)
        curs = conn.cursor()
        curs.execute('''delete from user where userid= ?''', (id,))
        conn.commit()
        conn.close()

    """save habit """
    def save_habit(self, habit):
        conn = sqlite3.connect(self.DB_PATH)
        curs = conn.cursor()
        if habit.habitid is None:
            curs.execute('''insert into habit( name, period, creationdate, currentstreak, longeststreak, userid) values (?,?,?,?,?,?)''',
                             (habit.name, habit.period, habit.creationDate,habit.currentStreak, habit.longestStreak, habit.user))
            lhabitid = curs.lastrowid
        else:
            lhabitid = habit.habitid
            curs.execute('''update habit set name =?, period =?, currentstreak =?, longeststreak=? where habitid =?'''
                         ,(habit.name, habit.period, habit.currentStreak, habit.longestStreak, habit.habitid))
        conn.commit()
        conn.close()
        return lhabitid

    """read list of habits of a user """
    def read_list_of_habits(self, userid):
        conn = sqlite3.connect(self.DB_PATH)
        curs = conn.cursor()
        curs.execute('''select habitid, name, period, creationdate, currentstreak, longeststreak from habit where userid = ?''',
                     (userid,))
        list_of_habits = curs.fetchall()
        conn.commit()
        conn.close()
        habits = []
        for row in list_of_habits:
            habit = Habit(row[1], row[2], userid, row[0])
            habit.creationDate = row[3]
            habit.currentStreak = row[4]
            habit.longestStreak = row[5]
            habits.append(habit)
        return habits

    """read one habit of a user with habitid"""
    def read_one_habit_id(self, userid, habitid):
        conn = sqlite3.connect(self.DB_PATH)
        curs = conn.cursor()
        curs.execute('''select habitid, name, period, creationdate, currentstreak, longeststreak from habit where userid = ? and habitid = ?''',
                     (userid, habitid))
        habit_row = curs.fetchone()
        conn.commit()
        conn.close()

        if habit_row:
            habit = Habit(habit_row[1], habit_row[2], userid, habit_row[0])
            habit.creationDate = habit_row[3]
            habit.currentStreak = habit_row[4]
            habit.longestStreak = habit_row[5]
            return habit
        else:
            return None

    """read one habit of a user with habit-name"""
    def read_one_habit_name(self, userid, habit_name):
        conn = sqlite3.connect(self.DB_PATH)
        curs = conn.cursor()
        curs.execute(
            '''select habitid, name, period, creationdate, currentstreak, longeststreak from habit where userid = ? and name = ?''',
            (userid, habit_name))
        habit_row = curs.fetchone()
        conn.commit()
        conn.close()

        if habit_row:
            habit = Habit(habit_row[1], habit_row[2], userid, habit_row[0])
            habit.creationDate = habit_row[3]
            habit.currentStreak = habit_row[4]
            habit.longestStreak = habit_row[5]
            return habit
        else:
            return None

    """update habit of a user"""
    def update_habit(self, habit):
        conn = sqlite3.connect(self.DB_PATH)
        curs = conn.cursor()
        curs.execute('''update habit set name=?, period=? where habitid = ?''',
                     (habit.name, habit.period, habit.habitid,))
        conn.commit()
        conn.close()

    """save completion of one habit"""
    def save_completiondate(self, habit, pdate  ):
        conn = sqlite3.connect(self.DB_PATH)
        curs = conn.cursor()
        curs.execute('''insert into completion(completiondate, habitid) values (?,?)''',
                     (pdate, habit.habitid))
        conn.commit()
        conn.close()


    """read list of completions of one habit"""
    def read_list_of_completions(self, habitid):
        conn = sqlite3.connect(self.DB_PATH)
        curs = conn.cursor()
        curs.execute('''select completiondate from completion where habitid = ? ''', (habitid,))
        list_of_completions = curs.fetchall()
        conn.commit()
        conn.close()
        completionDates = [datetime.strptime(row[0], "%Y-%m-%d").date() for row in list_of_completions]

        return completionDates

    """delete completion dates of one habit"""
    def delete_completion(self, habit):
        conn = sqlite3.connect(self.DB_PATH)
        curs = conn.cursor()
        curs.execute('''delete from completion where habitid =?''', (habit.habitid,))
        conn.commit()
        conn.close()

    """delete a habit by its habitid"""
    def delete_habit(self, habit):
        conn = sqlite3.connect(self.DB_PATH)
        curs = conn.cursor()
        curs.execute('''delete from habit where habitid=?''', (habit.habitid,))
        conn.commit()
        conn.close()
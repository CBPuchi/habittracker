# My Habit tracker App

## Table of contents
1. [General Info](#General-Info)
2. [Installation](#Installation)
3. [Usage](#Usage)
4. [Test](#Test)
5. [Contributing](#Contributing)


## General Info
This app help you to track your activities and complete and check them periodically.
At the beginning you are asked to register with a name. If this is done, you can choose out of a list of five predefined habits 
or enter any habit you want.
Habits can be checked daily or weekly.
Once you have done your habits a while you can check the current status of completion of your habits 
and for each habit the length of the current streak and your longest streak of a habit.

This app is build with Python as a backend app for a habit tracker.


## Installation

The app is developed for windows.

**Requirements:**<br>
* Python 3.13	 <br>
download here:  https://www.python.org/downloads/

**Requested packages:**<br>
* questionary 2.1.0<br>
download here: https://github.com/tmbo/questionary
install via: pip install questionary  	

**for the tests:**<br>
* pytest install via pip install -U pytest  <br>
download here: https://docs.pytest.org/en/6.2.x/#<br>
* freezegun install via "pip install freezgun"<br>
download here https://pypi.org/project/freezegun/

```shell
pip install -r requirements.txt
````

## Usage
Start the habit tracker with the command 
python main.py
and follow instructions on screen. First you are asked with which data you want to start.
Afterwards you are asked to log in and hten you can enter and complete your habits.

#### 0. Initialize Database
You can choose out of three options
1. Start with an empty database und enter your habits in the follwoing process. 
 This option drops an exitsing database and creates a new one.
2. Start with testdata. In this case a new database is created and the testdata of the
 user Tick, Trick and Track is  created. Each of them has the five habits: playing soccer, reading,
 helping Donald, scout meeting and visiting Dagobert. More details see in chaper test. The initialization
 of the data may take up to 3 minutes.
3. Continue with an existing database. This is the choice, if you have entered habits 
and want to continue with further habit or completing habits.
 ---
#### 1. Login
If it's the first time of using the habit tracker you are asked to register.
For the registration you have to enter a name. Only letters are allowed. If the chosen name alreads exist,
you are asked to enter a different name. A successful registration is quitted with "Registration successful!"
Since your are new, you can choose your first habits out of a list. The list includes: Running (weekly), 
Singing (daily), Swimming (weekly), Tea time (daily) and Yoga (daily).

To login in you have to enter your username. If you know your userid, you can also login with the userid.
If no user could be found with the entered data, you are asked to login again or you can exit the habit tracker.
---
#### 2. Update user
First point in the main menu is, that you can change your user name.
The current name is shown und you can enter a new name.
---
#### 3. Habit overwiew
With the habit overview all of your habits are listed with the period, the longest streak and current streak.
And your are asked, if you want to see the ompletion date of any habit.
---
#### 4.Create, update, delete or complete a habit

##### 4.1. Create a new habit 
You are able to create your own habits.
To do so, you are prompted for a habit name and its period (daily/weekly).
For the habit name only letters are allowed.

##### 4.2. Update a new habit 
You are able to change the name ond the period. You are asked for both attributes.

##### 4.3.Mark a habit as completed
To track your progress, you need to mark your habits as completed when you finished them. 
To mark your progress, just type in the name of your habit and afterwards enter the date of completion.
The date must have the format YYYY-mm-dd.
If a younger date exist, the new date is not excepted.
With entering a new date the current streak and longest streak of the habit are calculated.
          
##### 4.4. Delete a habit
To delete a habit, type in the name of the habit you want to delete. 
You will be prompted, if a habit with the entered name doesn't exist.

---
#### 5. View statistic

##### 5.1.List one habit
Shows you a list of all your habits with period, current streak and longest streak. 
          
##### 5.2. Longest streak of all habits
Shows you for both type of period the habit with the longest streak of all habits. 
          
##### 5.3. Longest streak of one habit
Shows you the longest streak of a selected habit

##### 5.4. Current completion status
Shows you for each habit the current status. The status can be completed, needs to be done 
or has been broken. Never mind restart it!

##### 5.3. All of on period
Shows you a list of all habits with the same period for both period types. 

---
#### 5. Delete your account
With this function all of your habits and your user are deleted.
 
---
## Test
Start the test with.
python -m pytest
There are four tests you can start

### testInitialize
The testdb habittracker.db is cleaned and created.
Afterwards it's tried to read the user Tom. If nothing is found, the user Tom is created and saved and the userid
is checked.

### testUser
This test starts with an empty DB
this test creates two user, Peter and Pauline, and saves them to the database. They are read by name and userid.
The name of Pauline is changed to Paula saved and read
And finally Peter is deleted.

### testHabit
This test starts with an empty DB
The user Pauline ist created and the habits running - weekly, singing - weekly and coffee break - daily are added.
- The three habits are read.
- The habit running is read and thename is changed to tea time with period: daily.
- The habit coffee break of Pauline ist deleted.
- The habit tea time is been completed on 5 days ina row and the current streak and longest streak are checked to 5.
- The habit tea time of Pauline is read and the completion dates are deleted 
to add new completion dates with a streak of 4 and 2 days. So the after the first four completion dates 
the current streak=4 and the longest streak=4. When the two further completion dates have been added the
current streak=2 and the longest streak=4.
- To test the completion status tge current date is frozen to @freezegun.freeze_time("2025-03-11")
The completion dates of tea time are deleted and date from 2.3. - 6.3.2025  have been added. The test of the completion 
status returns ...has been broken. Never mind restart it!
Then the completion dates 7.3. - 10.3.2025 have been added. The test of the completion status returns: needs to be done
Finally the 11.3.2025 has been added and the compltion status returns: is completed today
- To test to delete a habit and its  completion dates the habit singing is read and the completion dates 
and finally the habit is deleted. 


### testAnalyze
This test cleans the database and initializes it with the testdata of Tick, Trick and Track. 
Then for the User Tick the functions longest_streak, current_completion_status and all_of_one_periodare called.

Tick, Trick adn Track have all the habits with the period: 
playing soccer - weekly
reading - daily
helping Donald - daily
scout meeting - weekly
visiting Dagobert - weekly
The completion dates differ for the three user.
For Tick 
the longest streak is: 
the completion status is: 
	playing soccer: completed
	reading: 
	helping Donald: needs to be done
	scout meeting: completed
	visiting Dagobert: completed
all of one period returns: 
daily:
	reading
	helping Donald
weekly:
	playing soccer
	scout meeting
	visiting Dagobert


## Contributing 
This is my first Python project. Your comments, suggestions, and contributions are welcome. 
Please feel free to contribute pull requests or create issues for bugs and feature requests.

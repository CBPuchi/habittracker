# My Habit tracker App

## Table of contents
1. [General Info](#General-Info)
2. [Installation](#Installation)
3. [Usage](#Usage)
4. [Test](#Test)
5. [Contributing](#Contributing)


## General Info
This app help you to track your activities and complete and check them periodically.
At the beginning you are asked to register with a name. If this is done, you can choose out of a list of five predefined habit or enter any habit you want.
Habits can be checked daily or weekly.
Once you have done your habits a while you can check 
the current status of completion of your habits 
and for each habit the length of the current streak 
and your longest streak of a habit.

This app is build with Python as a backend app for a habit tracker.


## Installation

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
start
```usage
python main.py
```
and follow instructions on screen. These offer
#### 0. Initialize Database
* Possibility to create a database with test data 
* You are prompted to enter your first and last name, your preferred username and password. 
* If the username is already taken, you are prompted for a new one. 
* If everything is filled out correctly, your profile is created and you can login to the program. 
---
#### 1. Login
* Enter your username and password to login. 
* If you are a new user and haven't saved any habits yet, you are prompted to choose your habits from a predefined list. 
* You can either choose to select or skip a habit with Y/N. 

---
#### 2. Edit User Profile
* You can edit your first and last name as well as your password. 

---
#### 3. Create, Change or Mark a Habit as completed
#####  3.1. Create a new habit 
* You are able to create your own habits.
* To do so, you are prompted for a habit name, its category (Health, Fun, or Mindfulnes) and its periodicity (daily/weekly). 
          
##### 3.2. Delete a habit
* To delete a habit, type in the name of the habit you want to delete. 
          
##### 3.3. Change an existing habit
* To change an existing habit, type in the name of the habit you want to change. 
* You can change a habit's category and periodicity. You cannot change a habits name. 
          
##### 3.4. Mark a habit as completed
* To track your progress, you need to mark your habits as completed when you finished them. 
* To mark your progress, just type in the name of your habit. 
* You can mark a habit as completed any time. 
* If you save the progress multiple times per day it is only counted as a one-day-streak. 

---
#### 4. Activity Overview
##### 4.1. All habits
* Shows you a list of all your saved habits. 
          
##### 4.2. All weekly habits
* Shows you a list of all your weekly habits. 
          
##### 4.3. All daily habits
* Shows you a list of all your daily habits. 

---
#### 5. View Stats
##### 5.1. Your current streak overview
* Shows you a list of all your habits and their respective current streaks. 
* Displays all weekly and all daily habits. 
          
##### 5.2. Your current streak per habit
* To see your current streak of a specific habit, you are prompted to type in the name of the habit you want to check. 
          
##### 5.3. Your longest streak per habit
* You can also find out what your best / longest streak for a specific habit is. 
* Just type in the name of the habit to find out. 
          
##### 5.4. Your longest streak overview (by periodicity) 
* Tells you what your longest daily and longest weekly streak are among all your habits. 
## Test
``` shell 
pytest .
```

## Contributing 
This is my first Python project. Your comments, suggestions, and contributions are welcome. 
Please feel free to contribute pull requests or create issues for bugs and feature requests.

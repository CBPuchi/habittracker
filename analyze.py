import questionary
from period import Period

def longest_streak(user):
    """find the habit with the longest streak for period = weekly and for daily
    within all habits of the given user.  """
    longest_weekly_streak = 0
    longest_weekly_name = ""
    longest_daily_streak = 0
    longest_daily_name = ""
    habits = user.get_habits()
    if habits:
        for habit in habits:
            if habit.period == Period.weekly.value:
                if habit.longestStreak > longest_weekly_streak:
                    longest_weekly_streak = habit.longestStreak
                    longest_weekly_name = habit.name

            else:
                if habit.longestStreak > longest_daily_streak:
                    longest_daily_streak = habit.longestStreak
                    longest_daily_name = habit.name
        print("\nWeekly habit with longest streak: " + longest_weekly_name + " with streak of: "
              + str(longest_weekly_streak) + " weeks")
        print(
            "\nDaily habit with longest streak: " + longest_daily_name + " with streak of: "
            + str(longest_daily_streak) + " days")
    else:
        print("\nThere are no habits to analyze")

def current_completion_status(user):
    """print the current completion status of all habits of the given user
    """
    habits = user.get_habits()
    list_weekly_habits = []
    list_daily_habits = []
    if habits:
        for habit in habits:
            if habit.getCompletionDates():
                if habit.period == Period.weekly.value:
                    list_weekly_habits.append({"name": habit.name, "status": habit.checkCompletionStatus()})
                else:
                    list_daily_habits.append({"name": habit.name, "status": habit.checkCompletionStatus()})
        print("\nStatus of daily habits: ")
        if len(list_daily_habits) > 0:
            for daily_habit in list_daily_habits:
                print(daily_habit["name"] + ": " + daily_habit["status"])
        else:
            print("The daily habits have no completion dates")

        print("\nStatus of weekly habits: ")
        if len(list_weekly_habits) > 0:
            for weekly_habit in list_weekly_habits:
                print(weekly_habit["name"] + ": " + weekly_habit["status"])
        else:
            print("The weekly habits have no completion dates")
    else:
        print("There are no habits to analyze")

def all_of_one_period(user):
    """list all the habits of the given user and the chosen period type"""
    period_type = questionary.select("\nOf which period-type your habits you want to see", choices=[
        "daily",
        "weekly"
    ]).ask()
    period_val = Period[period_type].value
    habits = user.get_habits()
    for habit in habits:
        if habit.period == period_val:
            print("\n" + habit.name + " Period: " + Period(
                habit.period).name + "  creationdate: " + habit.creationDate +
                  " current streak: " + str(habit.currentStreak) + " longest streak: " + str(habit.longestStreak))

def all_of_one_period(user, period_val):
    """list all the habits of the given user and period"""
    habits = user.get_habits()
    for habit in habits:
        if habit.period == period_val:
            print("\n" + habit.name + " Period: " + Period(
                habit.period).name + "  creationdate: " + habit.creationDate +
                  " current streak: " + str(habit.currentStreak) + " longest streak: " + str(habit.longestStreak))
from datetime import timedelta, date
from period import Period
import habittrackerdb

#Definition of class Habit
class Habit:
    """
    With the parameters:name, period, userid and habitid a new habit is created
    The creationDate is set to the current timestamp
    currentStreak and longestStreak get a default value = 0
    The completionDates is an empty array
    """
    def __init__(self, name: str,
                 period: int,
                 userid:int,
                 habitid=None):
        self.habitid = habitid
        self.name = name
        self.period = period
        self.creationDate = date.today()
        self.currentStreak = 0
        self.longestStreak = 0
        self.user = userid
        self.completionDates = []
        self.db = habittrackerdb.HabitTrackerDB()

    #save the habit of the user
    def save(self):
        id = self.db.save_habit(self)
        if self.habitid is None:
            self.habitid = id

    #update the name and period of the habit
    def update(self, name:str,
               period:int):
        self.name = name
        self.period = period
        self.db.update_habit(self)

    #delete the habit
    def delete(self):
        self.db.delete_completion(self)
        self.db.delete_habit(self)

    #save the completiondate of the habit
    def save_completiondate(self, pdate):
        self.db.save_completiondate(self, pdate)

    #Complete a habit for a date
    def complete(self, complDate: date):
        """
        It is not allowed to add older completiondates than the youngest date in the list
        To check this the list of completiondates is sorted reverse
        and the new date is checked against the first date in the list
        """
        execStatus = 'ok'
        self.getCompletionDates().sort(reverse=True)
        if self.completionDates:
            if complDate > self.completionDates[0]:
                self.completionDates.append(complDate)
                self.save_completiondate(complDate)
                self.calculateStreaks()
            else:
                execStatus = "DateAlreadyCompleted: " + str(complDate)
        else:
            """
            the habit is initially started
            """
            self.completionDates.append(complDate)
            self.save_completiondate(complDate)
            self.currentStreak = 1
            self.longestStreak = 1
        self.save()
        return execStatus

    # check the completion status of a habit
    def checkCompletionStatus(self):
        """
        The completion status can be 'completed', 'needs to be done' oder 'has been broken'
        :return: a string with the completion status
        """
        self.completionDates = self.getCompletionDates()
        self.completionDates.sort(reverse=True)
        if  date.today() == self.completionDates[0]:
            return f'streak - {self.name} - is completed today'
        elif date.today() - self.completionDates[0]  <= timedelta(self.period):
            return f'Friendly reminder: streak - {self.name} - needs to be done'
        else:
            return f'streak -  {self.name} -  has been broken. Never mind restart it!'

    #calculate the current streak
    def calculateStreaks(self):
        """
        if only one completionDate exists => current streak = 1 and longest streak = 1
        is there are at least 2 dates
        check if the difference between the two latest is <= period
        if yes, than the current streak is ongoing and one added
        in case the difference ist bigger than period, than the streak is stopped.
        check the length of this current against the longest streak
        if no date exists the current streak = 0
        """
        if len(self.completionDates) == 1:
            self.currentStreak = 1
            self.longestStreak = 1
        elif len(self.completionDates) > 1:
            self.completionDates.sort(reverse=True)
            if self.completionDates[0] - self.completionDates[1] <= timedelta(self.period):
                self.currentStreak += 1
                self.longestStreak = max(self.currentStreak, self.longestStreak)
            else:
                self.currentStreak = 1
        else:
            self.currentStreak = 0


    def __str__(self):
        return (f'name:{self.name}; ID:{self.habitid}; period:{self.period}; current streak:{self.currentStreak}; '
                f'longest streak:{self.longestStreak}; created:{self.creationDate}; user:{self.user}')

    #get all completionDates of one habit
    def getCompletionDates(self):
        list_of_completion_dates = self.db.read_list_of_completions(self.habitid)
        self.completionDates = list_of_completion_dates
        return self.completionDates

    #print habit details readable
    def print_readable(self):
        print(self.name + " Period: " + Period(self.period).name + "  creationdate: " + self.creationDate +
        " current streak: " + str(self.currentStreak) + " longest streak: " + str(self.longestStreak))

    #print one complete habit including the completion dates
    def print_complete_habit(self):
        self.print_readable()
        self.print_completion_dates()

    #print completion dates of one habit
    def print_completion_dates(self):
        compl_dates = self.getCompletionDates()
        if compl_dates:
            print("Completion dates:")
            for compl_date in compl_dates:
                print(compl_date)
        else:
            print("No completion dates are available")

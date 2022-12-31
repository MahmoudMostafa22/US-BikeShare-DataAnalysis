from asyncio.windows_events import NULL
from pickle import TRUE
from statistics import mean, mode
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
Months_list = ["january","february","march","april","may","june","all"]
Days_list = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Enter Which city you look to analyze? ").lower()
        if city not in ("new york city","chicago","washington"):
            print("Sorry, {} is not in our dataset \nPlease, Enter a valid city within our data: ".format(city))
            continue
        else:
            break
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Enter which month you want to filter by or enter 'all' to apply no month filter: ").lower()
        if month not in Months_list :
            print("Sorry,{} is not a vaild month \nPlease enter a suitable Month: ".format(month))
            continue
        else:
            break
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Enter which day you want to filter by or enter 'all' to apply no day filter: ").lower()
        if day not in Days_list:
            print("Sorry, {} is not a valid day \nPlease try to enter a valid day of the week:  ".format(day))
            continue
        else:
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    #loading data
    df = pd.read_csv("{}".format(CITY_DATA[city]))


    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek


    if month != "all" :
        month = Months_list.index(month)+1 
        df= df[df["month"]==month]

    if day != "all" :
        day = Days_list.index(day)+1 
        df= df[df["day_of_week"] == day]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_Month = df['month'].mode()[0]
    print("The Most Common Month Is : {}".format(common_Month))

    # display the most common day of week
    common_Day = df["day_of_week"].mode()[0]
    print("The Most Common Day Is : {}".format(common_Day))

    # display the most common start hour
    df["hour"] = df["Start Time"].dt.hour
    common_Hour = df["hour"].mode()[0]
    print("The Most Common Hour of the Day Is : {}".format(common_Hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    Start_station =df["Start Station"].value_counts().idxmax()
    print("Most common station used as a starting station is: ",Start_station)
    

    # display most commonly used end station
    End_station = df["End Station"].value_counts().idxmax()
    print("Most common station used as a ending station is: ",End_station)

    # display most frequent combination of start station and end station trip
    Common_station = df[['Start Station','End Station']].mode().loc[0]
    print("Most common stations used as a starting | ending station is: \n{} ".format(Common_station))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    # time is in seconds
    Total_time = sum(df["Trip Duration"])
    # convert time from seconds to days
    print("Total Travel Time: {} Day(s)".format(Total_time/(60*60*24)))


    # display mean travel time
    Mean_Time = df["Trip Duration"]
    print("Average Travel Time: {} Min".format(mean(Mean_Time)/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    # i put it in the if statement down below
 

    # Display earliest, most recent, and most common year of birth
    if city != "washington":
        gender = df['Gender'].value_counts()
        birth_year = df["Birth Year"]
        # print(birth_year)
        earliest = birth_year.value_counts().min()
        recent = birth_year.value_counts().max()
        common = birth_year.value_counts().idxmax()
        print("\nUsers Gender are: \n{}".format(gender))
        print("The Earliest Birth Year is: {}".format(earliest))
        print("The most recent Birth Year is: {}".format(recent))
        print("The most common Birth Year is: {}".format(int(common)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def show_data(df):
    i = 0
    x=df.count(1)
    flag =True
    while flag:
        while True:
            check = input("Do you want to see some data? type('Yes'or'No'): ").title()
            if check not in ["Yes","No"]:
                print("Sorry, {} is not valid: ".format(check))
                continue
            elif check == "Yes" :
                if (i+5 <= len(df)):
                    print("\n",df.iloc[i:i+5])
                    i=i+5
                else:
                    print(df.iloc[i:])
                    print("\nThere is no extra data to print\n")
                    flag = False
                    break
            else:
                flag = False
                break
    print('-'*40)    


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        show_data(df)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    city = str(input('\nPlease select the city you want to explore: ')).lower()
    while city not in CITY_DATA:
        print('\nThe city your select is not in the list')
        city = str(input('\nPlease select the city you want to explore: ')).lower()
    # get user input for month (all, january, february, ... , june)
    print('\nThe data contain monthly information from Januray to June \nEnter all if you want to see all of them')
    monlist = ['all','january','february','march','april','may','june']
    month = str(input('\nPlease select the month you want to explore: ')).lower()
    while month not in monlist:
        print('\nThe month your select is unaviliable')
        month = str(input('\nPlease reselect the month you want to explore: ')).lower()
        
    # get user input for day of week (all, monday, tuesday, ... sunday)
    daylist = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    day = str(input('\nPlease select a specific day in a week you want to explore \nEnter all to see all: ')).lower()
    while day not in daylist:
        print('\nThe day your select is unaviliable')
        day = str(input('\nPlease reselect the day you want to explore: ')).lower()
    
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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('\nThe most frequent month is {}'.format(popular_month))
    
    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('\nThe most frequent day is {}'.format(popular_day_of_week))
    
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]
    print('\nThe most frequent hour is {}'.format(popular_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].value_counts().iloc[[0]]
    print('\nThe most frequent Start Station is {}'.format(popular_start))
    
    # display most commonly used end station
    popular_end = df['End Station'].value_counts().iloc[[0]]
    print('\nThe most frequent End Station is {}'.format(popular_end))

    # display most frequent combination of start station and end station trip
    conbined = df['Start Station']+ df['End Station']
    popular_conbined = conbined.value_counts().iloc[[0]]
    print('\nThe most frequent conbined Station is {}'.format(popular_conbined))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print('\nThe total travel time is {}'.format(total_travel))

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print('\nThe average travel time is {}'.format(mean_travel))
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print('\nThe user type is following\n', user_type)
    # Display counts of gender
    # discount the gender
    if 'Gender' in df.columns:
        df['Gender']=df['Gender'].dropna(axis=0,inplace = True)
        gender_type = df['Gender'].value_counts()
        print('\nThe gender type is following\n', gender_type)
    else:
        print('No avaible info can be provided for gender')
    if 'Birth Year' in df.columns:   
        # Display earliest, most recent, and most common year of birth
        df['Birth Year']=df['Birth Year'].dropna(axis=0,inplace = True)
        earliest_birth = df['Birth Year'].min()
        recent_birth = df['Birth Year'].max()
        common_birth = df['Birth Year'].mode()
        print('earliest, most recent, and most common year of birth are {} {} {}'.format(earliest_birth,recent_birth,common_birth))
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    else:
        print('No avaible info can be provided for birth year')

def user_input(df):
    """ask user whether they want to see raw data"""
    i = 0
    while seerawdata == 'yes':
        print('\n five lines of raw data is presented as follow\n', df.iloc[i:i+5])
        i = i + 5
        seerawdata = input('\nWould you see first five lines of raw data? Enter yes or no.\n').lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        seerawdata = input('\nWould you see first five lines of raw data? Enter yes or no.\n').lower()
        user_input(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

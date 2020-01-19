import time
import pandas as pd
import numpy as np
import random

chicago = r'C:\Users\Tobias\Documents\Udacity\3_Python\Project\chicago.csv'
new_york = r'C:\Users\Tobias\Documents\Udacity\3_Python\Project\new_york_city.csv'
washington = r'C:\Users\Tobias\Documents\Udacity\3_Python\Project\washington.csv'

CITY_DATA = { 'chicago': chicago,
              'new york city': new_york,
              'washington': washington }


# GLOBAL VARIABLES, LISTS, ETC
cities = list(CITY_DATA)+list(['random'])
months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
modes = ['random','standard']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')

    # Additional feature "mode" for analysis of data: choose random or individual
    mode = input('Do you want random or individually chosen output? Type \'random\' or \'standard\': ').lower()

    if mode == 'random':
        rcity = random.choice(list(CITY_DATA))
        rmonth = random.choice(months)
        rday = random.choice(days)
        print('Random data is analyzed for city \'{}\', month \'{}\', week day \'{}\'.'\
              .format(rcity.title(),rmonth.title(),rday.title())\
             )
        print('-'*40)
        return rcity, rmonth, rday

    # Asking user for selective output for city, month, week day
    elif mode == 'standard':

        # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city = input('Please name a city you want to analyze bike share data for: \n\
        \t Choose from: ({})'.format(list(CITY_DATA))).lower()
        # While loop to handle invalid inputs for city
        while city not in cities:
            print('No data available for this city. Please choose from this list: {}'.format(list(CITY_DATA)))
            city = input('Please name a city you want to analyze data for: ').lower()

        # TO DO: get user input for month (all, january, february, ... , june)
        month = input('Enter a month you want to analyze bike share data for: ').lower()
        # While loop to handle invalid inputs for month
        while month not in months:
            print('No data available for this month. Please choose from this selection: {}'.format(months))
            month = input('Enter a month you want to analyze bike share data for: ').lower()

        # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        day = input('Enter a week day you want to analyze bike share data for: ').lower()
        # While loop to handle invalid inputs for week day
        while day not in days:
            print('No data available for this day. Please choose from this selection: {}'.format(days))
            day = input('Enter a week day you want to analyze bike share data for: ').lower()
        print('-'*40)
        return city, month, day

    else:
        print('Unexpected input. Please try again.')
        main()


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day

    +++ STEPS +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    1. Open csv file and create a temporary data frame for selected city.
    2. Verify, if a filter for month is applied or not.
    3. Verify, if a filter for week day is applied or not.
    4. Create respective data frame for city, month and week day.
    5. Return data frame for other functions to work with.
   """

    file = pd.read_csv(CITY_DATA[city])
    df_temp = pd.DataFrame(file)
    df_temp['Start Time'] = pd.to_datetime(df_temp['Start Time'])

    if month != 'all':

        if day != 'all':
            temp = df_temp[df_temp['Start Time'].dt.month == months.index(month)]
            df = temp[temp['Start Time'].dt.weekday == days.index(day)-1]
        else:
            df = df_temp[df_temp['Start Time'].dt.month == months.index(month)]
    else:

        if day != 'all':
            df = df_temp[df_temp['Start Time'].dt.weekday == days.index(day)-1]
        else:
            df = df_temp

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    mc_month = df['Start Time'].dt.month.mode()[0]
    print('\t The most popular month is {}.'.format(months[mc_month].title()))

    # TO DO: display the most common day of week
    mc_dow = df['Start Time'].dt.weekday_name.mode()[0]
    print('\t The most popular week day is {}.'.format(mc_dow))

    # TO DO: display the most common start hour
    mc_hour = df['Start Time'].dt.hour.mode()[0]
    print('\t The most popular hour for rentals is {} o\'clock.'.format(mc_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    mc_start_sta = df['Start Station'].mode()[0]
    print('\t The most commonly used start station is {}.'.format(mc_start_sta.title()))

    # TO DO: display most commonly used end station
    mc_end_sta = df['End Station'].mode()[0]
    print('\t The most commonly used end station is {}.'.format(mc_end_sta.title()))

    # TO DO: display most frequent combination of start station and end station trip
    """
    1. Create temporary data frame to group by and count combinations of start / end station.
    2. Create a second temporary data frame to filter first temporary df to find highest hit rate .
    3. Extract values for start/end station and hit rate.
    4. Display result.
    """
    # 1.
    temp_df = pd.DataFrame(df.groupby(['Start Station','End Station'])['User Type'].count())
    # 2.
    temp_df2 = temp_df[temp_df['User Type'] == temp_df['User Type'].max()]
    # 3.
    start = temp_df2.index[0][0]
    end = temp_df2.index[0][1]
    count = temp_df2['User Type'][0]
    # 4.
    print('\t With {} hits the most frequent start / end combination is:\n\
    \t\t {} / {}'.format(count,start.title(),end.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    trip_duration = df['Trip Duration'].sum()/3600
    print('\t The total trip duration is {} hours.'.format(round(trip_duration,2)))

    # TO DO: display mean travel time
    m_trip_duration = df['Trip Duration'].mean()/60
    print('\t The mean trip duration is {} minutes.'.format(round(m_trip_duration,2)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    # TO DO: Display counts of user types
    for user in df['User Type'].unique():
        ct_user_type = df[df['User Type']==user]['Start Time'].count()
        print('\t {} {} rented a bike.'.format(ct_user_type, user))
    print()

    # TO DO: Display counts of gender
    """
    1. Check if data for 'Gender' is available for city chosen.
    2. If yes, find number of users per gender and print respective results.
    3. If no, print a statement that no data is available.
    """
    if 'Gender' in df.columns:
        for gender in df['Gender'].unique():
            ct_gender = df[df['Gender']==gender]['Start Time'].count()
            print('\t The number of {} users is {}.'.format(gender, ct_gender))
    else:
        print('\t No data on users\' gender is available.')
    print()

    # TO DO: Display earliest, most recent, and most common year of birth
    """
    1. Check if data for 'Birth Year' is available for city chosen.
    2. Extract earliest, most recent and most common birth year.
    3. Print respective result for selection of city, month and week day.
    """
    if 'Birth Year' in df.columns:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        mc_year = int(df['Birth Year'].mode()[0])

        print('\t The oldest user to was born in {}.\n\
         The youngest user was born in {}.\n\
         The birth year {} in comparison shows the highest number of users.'.format(earliest, recent, mc_year))
    else:
        print('\t No data on users\' birth year available.')
    print()

    #++++++++++++
    #EXTRA - Correlation between Birth Year and Trip Duration
    #++++++++++++
    """
    1. Check if data for 'Birth Year' is available for city chosen.
    2. Check if correlation value is greater or equal to or below 0.75.
    3. Print result to show whether correlation between birth year and trip duration is existent or not.
    """
    if 'Birth Year' in df.columns:
        age_duration_correlation = df.corr()['Trip Duration']['Birth Year']
        if age_duration_correlation >= 0.75:
            print('\t There is a {}% correlation between birth year and trip duration.'.format(age_duration_correlation))
        else:
            print('\t There is no significant correlation between birth year and trip duration.')
    else:
        print('\t Data on user\'s age is not available, therefore no correlation can be calculated.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):

    show = input('Do you want to skip through the raw data selected 5 rows at a time? (yes/no) ').lower()
    i=0
    while True:
        extract = df.iloc[0+i:5+i]
        i += 5
        print(extract)
        show = input('Do you want to skip through the raw data selected 5 rows at a time? (yes/no) ').lower()

        if show != 'yes':
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break



if __name__ == "__main__":
	main()

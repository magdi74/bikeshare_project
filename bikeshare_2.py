import time
import pandas as pd
from tabulate import tabulate

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

cities = ['chicago', 'new york city', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['thursday', 'friday', 'saturday', 'sunday', 'monday', 'tuesday', 'wednesday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "none" to apply no month filter
        (str) day - name of the day of week to filter by, or "none" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    global city
    choice = ['none', 'month', 'day', 'both']

    while True:
        print('Choose a name of a city: Chicago, New York City or Washington')
        city = input().lower()
        if city in cities:
            break

    while True:
        print('Choose a way to filter the data: Month, Day, Both or None')
        x = input().lower()
        if x in choice:
            if x == choice[0]:
                month = 'none'
                day = 'none'
                break
            # Month or Both choice
            if x == choice[1] or x == choice[3]:
                while True:
                    print('Please type a full month name\nJanuary, February, March, April, May or June')
                    month = input().lower()
                    if month in months:
                        break

                # Both choice
                if x == choice[3]:
                    x = choice[2]
                else:
                    day = 'none'
                    break
            # Day choice
            if x == choice[2]:
                while True:
                    print(
                        'Please type a full days name\nFriday, Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday')
                    day = input().lower()
                    if day in days:
                        break
                month = 'none'
                break

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "none" to apply no month filter
        (str) day - name of the day of week to filter by, or "none" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'none':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'none':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = months[df['month'].mode()[0] - 1].capitalize()

    # display the most common day of week
    df['weekday'] = df['Start Time'].dt.day_name()
    popular_weekday = df['weekday'].mode()[0]

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]

    print('The most popular month:', popular_month)
    print('The most popular weekday:', popular_weekday)
    print('The most popular start hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().idxmax()
    count_start_station = df['Start Station'].value_counts(ascending=False)[0]

    # display most commonly used end station
    popular_end_station = df['End Station'].value_counts().idxmax()
    count_end_station = df['End Station'].value_counts(ascending=False)[0]

    # display most frequent combination of start station and end station trip
    freq_trip = (df['Start Station'] + '--' + df['End Station']).mode().loc[0]
    count_freq_trip = df[['Start Station', 'End Station']].value_counts(ascending=False)[0]

    print(tabulate([[popular_start_station, popular_end_station], [count_start_station, count_end_station]],
                   headers=['Most used start station with count', 'Most used end station with count']))

    print('\nThe most frequent combination of start and end station trip with count {}\n{} \t to \t {}'
          .format(count_freq_trip, freq_trip.split('--')[0], freq_trip.split('--')[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()

    # display minimum travel time
    min_travel = df['Trip Duration'].min()

    # display minimum travel time
    max_travel = df['Trip Duration'].max()

    print("Total travel time:", total_travel)
    print("Mean travel time:", mean_travel)
    print('Max travel time:', max_travel)
    print('Min travel time', min_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()

    if city == cities[0] or city == cities[1]:
        # Display counts of gender
        gender = df['Gender'].value_counts()
        print('{} \n\n{}'.format(user_type, gender))

        # Display earliest, most recent, and most common year of birth
        earliest_year = int(df['Birth Year'].min())
        recent_year = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])

        print('\nThe earliest year', earliest_year)
        print('The most recent year', recent_year)
        print('The most common year', common_year)

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-' * 40)
    else:
        print(user_type)
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-' * 40)


def raw_data(df):
    """Displays some of the Raw data."""

    print(df.head())
    new = 0

    while True:
        view_data = input('\nWould you like to see the next five rows? Enter yes or no.\n')
        if view_data.lower() != 'yes':
            return
        new += 5
        print(df.iloc[new:new + 5])


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        while True:
            user_input = input('\nWould you like to see first five raw data? Enter yes or no.\n')
            if user_input.lower() == 'yes' or user_input.lower() == 'no':
                if user_input.lower() != 'yes':
                    break
                raw_data(df)
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

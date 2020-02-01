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
    city, month, day, filter_by = '', '', '', ''
    months = ['all', 'january', 'february', 'march', 'april',
              'may', 'june']
    days_of_week = ['all', 'monday', 'tuesday', 'wednesday',
                    'thursday', 'friday', 'saturday', 'sunday']
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while(True):
        if not (city in CITY_DATA):    
            city = input('Would you like to see data for Chicago, New York, or Washington?\n').lower()
            if city == 'new york':
                city = 'new york city'
    # get user input for month (all, january, february, ... , june)
        if (filter_by != 'month') or (filter_by != 'day') or (filter_by != 'none'):    
            filter_by = input('Would you like to filter the data by month, day, or none?\n(typos will be counted as none)\n').lower()
        if filter_by == 'month':
            if month not in months:
                month = input('Which month - January, February, March, April, May, or June\n').lower()
                day = 'all'
                
        elif filter_by == 'day':    
    # get user input for day of week (all, monday, tuesday, ... sunday)
            if day not in days_of_week:
                day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday\n').lower()
                month = 'all'
        else:
            month = 'all'
            day = 'all'
        if (city in CITY_DATA and month in months and day in days_of_week):
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
    # taken from the practice problem #3 before project submission
    # for info on 'datetime' I used
    # https://stackoverflow.com/questions/25146121/extracting-just-month-and-year-separately-from-pandas-datetime-column
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        
        df = df[df['Month']== month]
    if day != 'all':
        df = df[df['Day of Week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month

    print('There were {} uses in month {} of the year.'.format( df['Month'].value_counts().max(), df['Month'].value_counts().idxmax()))
    # display the most common day of week
    print('There were {} uses on {}.'.format(df['Day of Week'].value_counts().max(),  df['Day of Week'].value_counts().idxmax()))

    # display the most common start hour
    common_start = df['Start Time'].dt.hour.mode()[0]
    if common_start > 12:
        common_start -= 12
        print('The most common Start Time is {} P.M.'.format(common_start))
    else:
        print('The most common Start Time is {} A.M.'.format(common_start))
        

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most popular start station is {} with {} started trips.'.format(df['Start Station'].value_counts().idxmax(), df['Start Station'].value_counts().max()))

    # display most commonly used end station
    print('The most popular end station is {} with {} ended trips.'.format(df['End Station'].value_counts().idxmax(), df['End Station'].value_counts().max()))

    # display most frequent combination of start station and end station trip
    # found use of 'groupby' method from 
    # https://stackoverflow.com/questions/27018622/pandas-groupby-sort-descending-order/36316186
    most_trips = df.groupby(['Start Station','End Station'])['End Station'].agg(['count'])
    most_trips = most_trips.sort_values(('count'), ascending=False)[0:3][0:1]
    most_trips_start = most_trips.index[0][0]
    most_trips_end = most_trips.index[0][1]
    print('From {} to {} has {} trips'.format(most_trips_start, most_trips_end, int(most_trips['count'])))
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    hours = total_travel_time // 360
    minutes = (total_travel_time % 360) // 60
    seconds = ((total_travel_time % 360) % 60) 
    print('Total Trip duration is {} hours {} minutes and {} seconds'.format( hours, minutes, seconds))
    # display mean travel time
    mean = df['Trip Duration'].mean()
    mean_min = mean // 60
    mean_sec = mean % 60
    print('Trip Duration mean: {} minutes and {} seconds'.format(mean_min, mean_sec))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df.groupby(['User Type'])['User Type'].agg(['count'])
    # found use of method 'iterrows' from
    # https://stackoverflow.com/questions/40004871/pandas-get-the-value-of-the-index-for-a-row
    for i, row in user_type_count.iterrows():
        print('There are {} {} users.'.format(row[0],i))
        
    print()
    
    # Display counts of gender
    # found of 'in df.columns' from
    # https://stackoverflow.com/questions/24870306/how-to-check-if-a-column-exists-in-pandas/39371897
    if 'Gender' in df.columns:    
        gender_count = df.groupby(['Gender'])['Gender'].agg(['count'])
        for i, row in gender_count.iterrows():
            print('There are {} {}\'s.'.format(row[0], i))
            
        print()
    else:
        print('No gender data')
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        df = df.sort_values('Start Time')
        by = df['Birth Year']
        by = by.dropna()
        earliest_year = by.tail(1)
        
        print('The earliest birth year is {}'.format(int(earliest_year)))
        
        recent_year = by.head(1)
        
        print('The most recent year of birth is {}'.format(int(recent_year)))
        
        mode_year = by.mode()
        
        print('The most common birth year is {}'.format(int(mode_year)))
        
    else:
        print('No Birth Year data')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    view_count = 0
    # set option found
    #https://stackoverflow.com/questions/11707586/how-do-i-expand-the-output-display-to-see-more-columns-of-a-pandas-dataframe
    pd.set_option('display.width',1000)
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    while True:
        print('Would you like to view 5 lines of raw data?\n')
        view_raw_data = input('Yes or No\n')
        if view_raw_data.lower() == 'yes':
            print(df[view_count:view_count+5])
            view_count += 5
        elif view_raw_data.lower() == 'no':
            break
        else:
            print('Incorrect choice')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

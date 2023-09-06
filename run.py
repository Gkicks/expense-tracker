import gspread
from google.oauth2.service_account import Credentials
import re
from datetime import datetime, timedelta
from colorama import Fore, Style
import pwinput
import os
import time
from time import sleep
import sys
import bcrypt
import pandas as pd
import numpy as np
from transaction import Transaction

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# global variables
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('expense-tracker')
# A list of all the existing users usernames
CURRENT_USERNAMES = SHEET.worksheet('users').col_values(1)
# A list of all the existing users passwords
CURRENT_PASSWORDS = SHEET.worksheet('users').col_values(2)
# A list to put the users username and password in for use in other functions
USERNAME_PASSWORD = ['gail', 'password']

# beginning title - reads EXPENSE TRANCKERS over two lines
print(Fore.BLUE + '                     __     __   __       __   __')
print(Fore.MAGENTA + '                    |__ \\/ |__| |__ |\\ | |__  |__')
print(Fore.RED + '                    |__ /\\ |    |__ | \\|  __| |__\n')
print(Fore.BLUE + '                    ___  __   __   __     __  __')
print(Fore.MAGENTA + '                     |  |__| |__| |   |/ |__ |__|')
print(Fore.RED + '                     |  |  \\ |  | |__ |\\ |__ |  \\ ')
print(Style.RESET_ALL)


def print_slow(str):
    """
    To slow how quickly text is printed to the screen
    """
    for character in str:
        sys.stdout.write(character)
        # to prevent the characters spacing out
        sys.stdout.flush()
        # the length of time between each charater showing
        time.sleep(0.05)

    return


def sleep_clear_screen(num):
    """
    clears the user's display screen after a second's delay
    """
    # length of pause, before screen clearing, in seconds
    sleep(num)
    # clears the screen
    os.system('clear')

    return


# functions relating to username and password
def new_or_existing_user():
    """
    Asks the user if they are a new or existing user
    """
    print('\nAre you a new or existing user?\n')
    print('N - new user')
    print('E - existing user\n')
    while True:
        new_or_existing_choice = input('Enter N or E: ').upper()
        if validate_new_user_option(new_or_existing_choice):
            sleep_clear_screen(1)
            break

    return new_or_existing_choice


def validate_new_user_option(letter):
    """
    Ensures the user only inputs one of the two options available.
    These are whether they are a new (N) or existing (E) user
    """
    new_existing_options = ['N', 'E']
    try:
        if letter not in new_existing_options:
            raise ValueError
    except ValueError:
        print(Fore.RED + 'You did not enter a correct value')
        print(Style.RESET_ALL)
        return False

    return True


def choose_username():
    """
    Asks the user to choose a new username
    """
    print('\nPlease choose a username\n')
    print_slow('Username should be at least two characters long\n')
    print_slow('Username must only be one word\n')
    while True:
        username = input('\nEnter username: ')
        # converts username to lowercase for storage
        username_lower = username.lower()
        if validate_new_username(username_lower):
            print_slow(Fore.BLUE + f'\nThank you. Your username is {username}')
            sleep_clear_screen(1)
            print(Style.RESET_ALL)
            USERNAME_PASSWORD[0] = username_lower
            break

    return username


def validate_new_username(username):
    """
    Validates the users chosen username.
    Checks username is at least two characters long
    Checks username isn't already in use
    Checks there are no spaces in the username
    """
    try:
        if len(username) < 2:
            print(Fore.RED + 'Username must contain at least two charaters')
            raise ValueError
        if username in CURRENT_USERNAMES:
            print(Fore.RED + 'That username already exists')
            raise ValueError
        if " " in username:
            print(Fore.RED + 'Username must only be one word')
            raise ValueError
    except ValueError:
        print('Please choose another username')
        print(Style.RESET_ALL)
        return False

    return True


def encrypt_pw(password):
    """
    Encrypts and encodes the entered password
    Returns the password as decoded
    """
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # Returns the password decoded so it can be store in Google Sheets
    return hashed_pw.decode()


def choose_password():
    """
    Asks the user to choose a password
    Adds a new worksheet to Google Sheets, named the user's username
    """
    print('Please choose a password\n')
    print_slow('Passwords must be at least six characters long,\n')
    print_slow('contain at least one uppercase letter,\n')
    print_slow('one lowercase letter,\n')
    print_slow('one number and one special character\n\n')

    while True:
        new_password = input('Enter password here: ')
        # encrypts and decodes the password
        enc_pw = encrypt_pw(new_password)
        if validate_new_password(new_password):
            print(Fore.GREEN + 'Thank you. That password is valid\n')
            sleep_clear_screen(1)
            print_slow(Fore.BLUE + f'\nHi {USERNAME_PASSWORD[0]}!\n')
            print(Style.RESET_ALL)
            # saves password to list so it can be appended
            USERNAME_PASSWORD[1] = enc_pw
            # gets the worksheet where usernames and passwords stored
            user_worksheet = SHEET.worksheet('users')
            # appends the username and password to bottom of worksheet
            user_worksheet.append_row(USERNAME_PASSWORD)
            # adds a new worksheet to record the users transactions
            username_lower = USERNAME_PASSWORD[0].lower()
            add_new_user_worksheet(username_lower)
            break

    return new_password


def validate_new_password(password):
    """
    Validates the chosen password.
    Password must be at least six characters long.
    Password must contain one uppercase and one lowercase letter,
    one number and one special character
    """
    try:
        if len(password) < 6:
            print(Fore.RED + f'Password entered was {len(password)} long')
            print('Password must be at least six characters long')
            raise ValueError
        if not re.search('[A-Z]', password):
            print(Fore.RED + 'Password must contain one uppercase letter')
            raise ValueError
        if not re.search('[a-z]', password):
            print(Fore.RED + 'Password must contain one lowercase letter')
            raise ValueError
        if not re.search('[!"#£$%&\'()*+,-./:;<=>?@[\\]^_`{~}]', password):
            print(Fore.RED + 'Password must contain one special character')
            raise ValueError
        if not re.search('[0-9]', password):
            print(Fore.RED + 'Your password must include at least one number')
            raise ValueError
    except ValueError:
        print('Please try again')
        print(Style.RESET_ALL)
        return False

    return True


def add_new_user_worksheet(username):
    """
    Adds new worksheet to the expense-tracker Google sheet
    Calls the worksheet the users username
    """
    SHEET.add_worksheet(username, rows="1", cols="4")
    headings = ['Date', 'Category', 'Description', 'Amount']
    SHEET.worksheet(username).append_row(headings)

    return


def get_existing_username():
    """
    Asks existing users to enter their existing username
    """
    while True:
        username = input('\nPlease enter your username: \n')
        # converts username to lowercase as how is stored
        username_lower = username.lower()
        if validate_existing_username(username_lower):
            # changes the list entry to the chosen username
            USERNAME_PASSWORD[0] = username
            break

    return username


def validate_existing_username(username):
    """
    Checks that the username inputted exists
    """
    try:
        # checks the username is in the list of stored usernames
        if username not in CURRENT_USERNAMES:
            print(Fore.RED + 'username does not exist')
            raise ValueError
    except ValueError:
        print('Please try again')
        print(Style.RESET_ALL)
        return False

    return True


def get_existing_password():
    """
    Asks existing users to enter their existing password
    """
    while True:
        # ask user to enter their password
        # the password character displayed as * for security
        password = pwinput.pwinput(prompt='\nPlease enter your password: ')
        # ask user to confirm their password
        # the password character displayed as * for security
        pw_confirm = pwinput.pwinput(prompt='Please confirm your password: ')
        if validate_existing_password(password, pw_confirm):
            print(Fore.BLUE + f'\nWelcome back {USERNAME_PASSWORD[0]}!\n')
            print(Style.RESET_ALL)
            sleep_clear_screen(1)
            break

    return


def validate_existing_password(password, pw_confirm):
    """
    Checks the two passwords entered match
    Checks the password inputted matches the password stored
    """
    # creates a merged dictionary of stored usernames and passwords
    username_password_dic = dict(zip(CURRENT_USERNAMES, CURRENT_PASSWORDS))
    username = USERNAME_PASSWORD[0]
    # converts username to lowercase as that's how it's stored
    username_lower = username.lower()
    # gets the password value from the username
    users_password = username_password_dic[username_lower]
    try:
        if password != pw_confirm:
            print('\nThose passwords do not match')
            raise ValueError
        # checks the stored password against the entered password
        if not bcrypt.checkpw(password.encode(), users_password.encode()):
            print(Fore.RED + 'Your username and password do not match')
            raise ValueError
    except ValueError:
        print('Please try again')
        print(Style.RESET_ALL)
        return False

    return True


# main menu function
def main_menu():
    """
    Main menu of options for the user to choose from
    1 - will take the user to entering a transaction, starting with the date
    2 - will give the user the option to analyse their transactions
    3 - will give the user the option to view their transacitons,
            from a date range
    4 - will terminate the programme
    """
    print('Please pick an option:\n')
    print('1 - Enter Transaction')
    print('2 - Analyse Spending')
    print('3 - View Transactions')
    print('4 - Quit\n')
    while True:
        option = input('Please pick an option between 1 and 4: ')
        if option_validation(option):
            if option == '1':
                sleep_clear_screen(1)
                get_transaction()
            elif option == '2':
                sleep_clear_screen(1)
                date_range = get_date_range()
                start_date = date_range[0]
                end_date = date_range[1]
                analyse_spending(start_date, end_date)
            elif option == '3':
                sleep_clear_screen(1)
                date_range = get_date_range()
                start_date = date_range[0]
                end_date = date_range[1]
                show_transactions(start_date, end_date)
            else:
                print(Fore.MAGENTA + '\nThank you for using this tracker')
                print(f'Goodbye {USERNAME_PASSWORD[0]}\n')
                break
            break
    return option


def option_validation(option):
    """
    Validates the option input
    """
    if option == "":
        print(Fore.RED + '\nYou did not enter a number!\n')
        print(Style.RESET_ALL)
    else:
        num_options = ['1', '2', '3', '4']
        try:
            if option not in num_options:
                raise ValueError
        except ValueError:
            print(Fore.RED + 'Not a valid number. Please try again.\n')
            print(Style.RESET_ALL)
            return False
        return True
    return


# Entering transaction functions
def get_date():
    """
    Asks user to input a date
    """
    print('\nPlease enter the date of the transaction\n')
    print_slow('This should be in the format DD/MM/YYYY\n')
    while True:
        transaction_date = input('\n> ')
        if validate_date(transaction_date):
            sleep_clear_screen(1)
            break

    return transaction_date


def validate_date(date):
    """
    Validates that the date inputted is in the format DD/MM/YYYY
    Checks the date added is not in the future
    """
    try:
        if len(date) != 10:
            print(Fore.RED + '\ndate is not in the correct format')
            print('The date should be in the format DD/MM/YYYY')
            raise ValueError
        # gets today's date
        today = datetime.now()
        # determines the format the date should be entered in
        date_str = datetime.strptime(date, '%d/%m/%Y')
        if date_str > today:
            print(Fore.RED + 'The date cannot be in the future')
            raise ValueError
        # splits the date at the / character
        date_split = date.split('/')
        day = date_split[0]
        month = date_split[1]
        year = date_split[2]
        # checks if the number of characters in day and month is two
        # checks the year has four characters
        if len(day) != 2 or len(month) != 2 or len(year) != 4:
            print(Fore.RED + '\ndate is not in the correct format')
            print('The date should be in the format DD/MM/YYYY')
            raise ValueError
        if int(year) < 2000:
            print(Fore.RED + 'Date cannot be before 01/01/2000')
            raise ValueError
    except ValueError:
        print(Fore.RED + 'Please enter a valid date')
        print(Style.RESET_ALL)
        return False

    return True


def get_spend_category():
    """
    Asks user to pick a spend category from given options
    """
    while True:
        print('\nPlease enter the transaction category\n')
        print('1 - Household Bills')
        print('2 - Transportation')
        print('3 - Food')
        print('4 - Savings')
        print('5 - Personal Spending')
        print('6 - Other')
        spend_category = input('\nEnter a number betweeen 1 and 6: ')
        if validate_spend_category(spend_category):
            sleep_clear_screen(1)
            if spend_category == '1':
                spend_cat_name = 'Household Bills'
            elif spend_category == '2':
                spend_cat_name = 'Transportation'
            elif spend_category == '3':
                spend_cat_name = 'Food'
            elif spend_category == '4':
                spend_cat_name = 'Savings'
            elif spend_category == '5':
                spend_cat_name = 'Personal Spending'
            elif spend_category == '6':
                spend_cat_name = 'Other'
            break

    return spend_cat_name


def validate_spend_category(number):
    """
    Validates that the option chosen is one of the available options
    """
    avail_options = ['1', '2', '3', '4', '5', '6']
    try:
        if number not in avail_options:
            raise ValueError
    except ValueError:
        print(Fore.RED + 'incorrect option chosen')
        print(Fore.RED + 'Please enter a number between 1 and 6')
        print(Style.RESET_ALL)
        return False

    return True


def get_description():
    """
    Asks the user to input a description of spend
    """
    print('\nEnter a description of the spend\n')
    print_slow('For example, "rent" or "lunch"\n\n')
    while True:
        spend_desc = input('> ')
        if validate_desc(spend_desc):
            sleep_clear_screen(1)
            break

    return spend_desc


def validate_desc(spend_desc):
    try:
        if spend_desc == "":
            print(Fore.RED + 'Decription is required')
            raise ValueError
    except ValueError:
        print(Style.RESET_ALL)
        return False

    return True


def get_amount():
    """
    Asks the user to input the spend amount
    """
    print('\nPlease enter the amount spent.\n')
    print_slow('This should be a valid amount\n')
    print_slow('For example, £10 or £5.67\n\n')
    while True:
        spend_amount = input('£ ')
        if validate_amount(spend_amount):
            print(Fore.MAGENTA + '\nAdding transaction...\n')
            print_slow(Fore.BLUE + f'Thank you {USERNAME_PASSWORD[0]}.\n')
            print_slow('Your transaction has been added')
            print(Style.RESET_ALL)
            sleep_clear_screen(1)
            break

    return spend_amount


def validate_amount(number):
    """
    Validates that the amount entered is a valid amount
    and that the amount is greater than 0
    """
    try:
        if not re.fullmatch(r'^\-?[0-9]+(?:\.[0-9]{2})?$', number):
            print(Fore.RED + 'That is not a valid amount')
            raise ValueError
        number = float(number)
        if number <= 0:
            print(Fore.RED + 'The amount must be greater than £0')
            raise ValueError
    except ValueError:
        print('Please try again')
        print(Style.RESET_ALL)
        return False
    return True


def get_transaction():
    # functions to get the class values
    date = get_date()
    category = get_spend_category()
    desc = get_description()
    amount = get_amount()
    # returned data as a class
    new_transaction_cl = Transaction(date=date, category=category,
                                     description=desc, amount=amount)
    # convert the class to a list
    new_transaction = list(vars(new_transaction_cl).values())
    add_transaction(new_transaction)
    next_choice()

    return new_transaction


def add_transaction(transaction):
    """
    Adds the transation to the sheet of the current user
    """
    # covert username to lowercase as as is stored
    username_lower = USERNAME_PASSWORD[0].lower()
    # add transaction to bottom of user's worksheet
    SHEET.worksheet(username_lower).append_row(transaction)

    return


# function is get further choice from user
def next_choice():
    """
    Allows the user to choose if they would like to perform another action
    """
    print('\nWhat would you like to do next?\n')
    print('1 - Enter another transaction')
    print('2 - Return to the main menu')
    print('3 - Quit')
    while True:
        next_choice_action = input('\n> ').upper()
        if validate_next_choice(next_choice_action):
            if next_choice_action == '1':
                sleep_clear_screen(1)
                get_transaction()
                break
            elif next_choice_action == '2':
                sleep_clear_screen(1)
                main_menu()
                break
            elif next_choice_action == "3":
                print(Fore.MAGENTA + '\nThank you for using this tracker')
                print(f'Goodbye {USERNAME_PASSWORD[0]}\n')
                break
    return


def validate_next_choice(num):
    """
    Ensures the user only inputs one of the three options available.
    """
    next_choice_options = ['1', '2', '3']
    try:
        if num not in next_choice_options:
            raise ValueError
    except ValueError:
        print(Fore.RED + 'You did not enter a correct value')
        print('Please enter a number between 1 and 3')
        print(Style.RESET_ALL)
        return False

    return True


def get_date_range():
    """
    Asks user to input a date range
    Validates the individual dates
    Pulls function to validate date range
    """
    print('\nPlease enter the start and end dates')
    print('of the transactions you want to view\n')
    print_slow('These should be in the format DD/MM/YYYY\n')
    print_slow('Dates should be no more than 90 days apart\n\n')
    while True:
        start_date = input('Start Date: ')
        if validate_date(start_date):
            while True:
                end_date = input('\nEnd Date: ')
                if validate_date(end_date):
                    while True:
                        if validate_date_range(start_date, end_date):
                            sleep_clear_screen(1)
                        break
                break
        break

    return start_date, end_date


def validate_date_range(date1, date2):
    """
    Converts both dates to strings
    calculates the number of day between the dates
    Checks the start date is before of equal to the end date
    Checks the dates are 90 or less days apart
    """
    # converts dates to strings
    date_str_1 = datetime.strptime(date1, '%d/%m/%Y')
    date_str_2 = datetime.strptime(date2, '%d/%m/%Y')
    # calculates the difference between the two dates, in days
    difference = abs((date_str_1 - date_str_2).days)
    try:
        # Checks the start date is not after the end date
        if date_str_2 < date_str_1:
            print(Fore.RED + 'End date cannot be before the start date')
            raise ValueError
        # Checks the dates are not more than 90 days apart
        if difference > 90:
            print(Fore.RED + '\nDates cannot be more than 90 days apart')
            raise ValueError
    except ValueError:
        print('Please enter new dates')
        print(Style.RESET_ALL)
        return False

    return True


def get_pds_df():
    username_lower = USERNAME_PASSWORD[0].lower()
    # gets the users worksheet
    ws = SHEET.worksheet(username_lower)
    # put the worksheet into a pandas dataframe
    df = pd.DataFrame(ws.get_all_records())

    return df


def show_transactions(date1, date2):
    """
    Puts the users Google worksheet into a pandas dataframe.
    Sorts this by date ascending
    filters the lines between the two dates chosen
    """
    df = get_pds_df()
    # converts date string to date so can be sorted
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    # sorts the dataframe by dates ascending
    df.sort_values(by='Date', ascending=True, inplace=True)
    # converts dates from string to date
    start_date = datetime.strptime(date1, '%d/%m/%Y')
    end_date = datetime.strptime(date2, '%d/%m/%Y')
    # filters rows between the start and end date
    filter_dates = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    # checks if there is data to display
    if filter_dates.empty:
        print(Fore.RED + 'There is no data to show')
        print(Style.RESET_ALL)
    else:
        # prints filter_dates
        print('These are your transactions between {date1} and {date2}\n')
        print(Fore.YELLOW + filter_dates.to_string(index=False))
        print(Style.RESET_ALL)
    next_choice()

    return


def analyse_spending(date1, date2):
    df = get_pds_df()
    df['Amount'] = pd.to_numeric(df['Amount'])
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    df.sort_values(by='Date', ascending=True, inplace=True)
    start_date = datetime.strptime(date1, '%d/%m/%Y')
    end_date = datetime.strptime(date2, '%d/%m/%Y')
    filter_dates = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    if filter_dates.empty:
        print(Fore.RED + '\nThere is no data to show')
        print(Style.RESET_ALL)
        next_choice()
    else:
        print('Would you like to see the sum or average of your spending?')
        print('1 - Sum')
        print('2 - Average')
    while True:
        validate_analyse_choice = input('> ')
        if validate_choice(validate_analyse_choice):
            if validate_analyse_choice == '1':
                pivot = pd.pivot_table(data=filter_dates, index=['Category'],
                                       values=['Amount'], aggfunc=np.sum)
                print('These are the sums of your transactions between:')
                print(f'{date1} and {date2}\n')
                print(pivot)
                break
            else:
                pivot = pd.pivot_table(data=filter_dates, index=['Category'],
                                       values=['Amount'], aggfunc=np.mean)
                pivot_round = pivot.round(2)
                print('These are the averages of your transactions between:')
                print(f'{date1} and {date2}\n')
                print(pivot_round)
                break
    next_choice()


def validate_choice(num):
    choices = ['1', '2']
    try:
        if num not in choices:
            raise ValueError
    except ValueError:
        print(Fore.RED + '\nNot a valid option')
        print(Style.RESET_ALL)
        return False

    return True


# main function
def main():
    """
    The main function that runs the rest of functions
    """
    new_or_existing_choice = new_or_existing_user()
    if new_or_existing_choice == 'N':
        choose_username()
        choose_password()
    elif new_or_existing_choice == 'E':
        get_existing_username()
        get_existing_password()
    main_menu()


# true if the program is run as a file
if __name__ == "__main__":
    pass
    main()

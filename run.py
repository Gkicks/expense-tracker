import gspread
from google.oauth2.service_account import Credentials
import regex
from datetime import datetime
# from dateutil.parser import parse

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('expense-tracker')
current_usernames = SHEET.worksheet('users').col_values(1)
current_passwords = SHEET.worksheet('users').col_values(2)
new_user = ['username', 'password']

print('Welcome to the Python expense tracker!\n')


def new_or_existing_user():
    """
    Asks the user if they are a new or existing user
    """
    print('Are you a new or existing user?')
    print('N - new user')
    print('E - existing user')
    while True:
        new_or_existing_choice = input('Enter N or E: \n').upper()
        if validate_new_user_option(new_or_existing_choice):
            break
    return new_or_existing_choice


def validate_new_user_option(new_or_existing_choice):
    """
    Ensures the user only inputs one of the two options available.
    These are whether they are a new (N) or existing (E) user
    """
    new_existing_options = ['N', 'E']
    try:
        if new_or_existing_choice not in new_existing_options:
            raise ValueError
    except ValueError:
        print('You did not enter a correct value')
        return False
    return True


def choose_username():
    """
    Asks the user to choose a new username
    """
    print('\nPlease choose a username')
    print('Username should be at least two characters in length')
    print('Username must only contain letters or numbers')
    while True:
        new_username = input('Enter username: \n')
        if validate_new_username(new_username):
            print(f'\nThank you. Your username is {new_username}')
            new_user[0] = new_username
            choose_password()
            break

    return new_username


def validate_new_username(new_username):
    """
    Validates the users chosen username.
    Checks username is at least two characters long
    Checks username isn't already in use
    """
    try:
        if len(new_username) < 2:
            print('Your username must contain at least two characters')    
            raise ValueError
        if new_username in current_usernames:
            print('That username already exists')
            raise ValueError
    except ValueError:
        print('Please choose another username')
        return False
    return True


def choose_password():
    """
    Asks the user to choose a password
    """
    print('\nPlease choose a password')
    print('Passwords must be at least 6 characters long')
    print('and contain at least one uppercase letter,')
    print('one lowercase letter,')
    print('one number')
    print('and one special character')
    print('special characters accepted are £, $, %, ^ or &')

    while True:
        new_password = input('Enter password here: \n')

        if validate_new_password(new_password):
            print('Thank you. That password is valid')
            new_user[1] = new_password
            print(new_user)
            user_worksheet = SHEET.worksheet('users')
            user_worksheet.append_row(new_user)
            add_new_user_worksheet(new_user[0])
            break


def validate_new_password(new_password):
    """
    Validates the chosen password.
    Password must be at least six characters long.
    Password must contain one uppercase and one lowercase letter,
    one number and one special character
    """
    try:    
        if len(new_password) < 6:
            print(f'That password is only {len(new_password)} characters long')
            print('Your password must be at least 6 characters long')
            raise ValueError
        if not any(x.isupper() for x in new_password):
            print('Your password must contain at least one uppercase letter')
            raise ValueError
        if not any(x.islower() for x in new_password):
            print('Your password must contain at least one lowercase letter')
            raise ValueError
        special_characters = ['£', '$', '%', '^', '&']
        if not any(x in special_characters for x in new_password):
            print('Your password must contain either £, $, %, ^ or &')
            raise ValueError
        if not any(x.isdigit() for x in new_password):
            print('Your password must include at least one number')
            raise ValueError
    except ValueError:
        print('Please try again')
        return False
    return True


def add_new_user_worksheet(user):
    SHEET.add_worksheet(user, rows="1", cols="7")
    SHEET.worksheet(user).append_row(['Date', 'Household Bills', 'Transportation', 'Food', 'Savings', 'Personal Spending', 'Other'])


def get_existing_username_password():
    """
    Asks existing users to enter their username and password
    """
    while True:
        username = input('\nPlease enter your username: \n')
        password = input('Please enter your password: \n')
        if validate_existing_username_password(username, password):
            print(f'\nWelcome back {username}!\n')
            break

    return username, password


def validate_existing_username_password(username, password):
    """
    Checks that the username inputted exists.
    Checks the password inputted matches the password stored
    """
    try: 
        if username == 'username':
            print('username is not a valid option')
            raise ValueError
        if username not in current_usernames:
            print(f'You entered {username}. That username does not exist')
            raise ValueError
        # bug - had this at the start of the function.
        # was causing a keyerror 
        username_password = dict(zip(current_usernames, current_passwords))
        users_password = username_password[username]
        if password != users_password:        
            print('Your username and password do not match')
            raise ValueError
    except ValueError: 
        print('Please try again')
        return False
    return True

  
def choose_option():
    """
    gets the action option the user has chosen to do
    """
    print('What would you like to do today?')
    print('1 - Enter Transaction')
    print('2 - Analyse Spending\n')
    while True:
        option = input('Please pick an option, either 1 or 2: \n')
        if option_validation(option):
            if option == '1':
                print('option 1 chosen')
                get_transaction()
            elif option == '2':
                print('option 2 chosen')
                # spending = analyse_transaction()
            else:
                print('Error! Please restart program')        
            break
    return option
    

def option_validation(option):
    """
    Validates the option input
    """
    if option == "":
        print('\nYou did not enter a number!\n')
    else:
        num_options = ['1', '2']
        try:
            if option not in num_options:
                raise ValueError
        except ValueError:
            print('Not a valid number. Please try again.\n')
            return False
        return True
    return option


def get_transaction():
    print('\nPlease enter the date of the transaction')
    print('This should be in the format DD/MM/YY')
    while True:
        transaction_date = input('> \n')
        if validate_date(transaction_date):     
            print('\nPlease enter the transaction category')
            print('1 - Household Bills')
            print('2 - Transportation')
            print('3 - Food')
            print('4 - Savings')
            print('5 - Personal Spending')
            print('6 - Other')
            while True:
                spend_category = input('Enter a number betweeen 1 and 6: \n')
            
                if validate_spend_category(spend_category):
                    print('\nPlease enter the amount spent.')
                    print('This should be in the format £xx.xx')
                    while True:
                        spend_amount = input('£ \n')

                        if validate_amount(spend_amount):
                            print('Adding transaction...')
                            return False
                            break


def validate_date(date):
    try:
        date_str = datetime.strptime(date, '%d/%m/%y')
        return True
        print(date)
    except ValueError:
        print('Invalid date')
        return False

def validate_spend_category(number):
    avail_options = ['1', '2', '3', '4', '5', '6']
    try:
        if number not in avail_options:
            raise ValueError
    except ValueError:
        print('incorrect option chosen')
        print('Please enter a number between 1 and 6')
        return False
    return True

def validate_amount(float):
    try:
        if len(float.rsplit('.')[-1]) != 2:
            raise ValueError
    except ValueError:
        print('This is not a correct amount')
        print('Please try again')
        return False
    return True


def main():
    new_or_existing_choice = new_or_existing_user()
    if new_or_existing_choice == 'N':
        new_username = choose_username()
        print(f'\nHi {new_username}! What would you like to do today?\n')
        option = choose_option()
    elif new_or_existing_choice == 'E':
        get_existing_username_password()
        # password = enter_password()
        option = choose_option()
        # action = option_action()
    else:
        print('Error! Please restart program')


main()
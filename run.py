import gspread
from google.oauth2.service_account import Credentials
import regex
from datetime import datetime
from colorama import init, Fore, Back, Style

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
username_password = ['username', 'password']


print(Fore.BLUE + ' __     __   __       __   __')
print(Fore.MAGENTA + '|__ \/ |__| |__ |\ | |__  |__')
print(Fore.RED + '|__ /\ |    |__ | \|  __| |__\n')
print(Fore.BLUE + ' ___  __   __   __     __  __')
print(Fore.MAGENTA + '  |  |__| |__| |   |/ |__ |__|')
print(Fore.RED + '  |  |  \ |  | |__ |\ |__ |  \ ')
print(Style.RESET_ALL)


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
        print(Fore.RED + 'You did not enter a correct value')
        print(Style.RESET_ALL)
        return False
    return True


def choose_username():
    """
    Asks the user to choose a new username
    """
    print('\nPlease choose a username\n')
    print('Username should be at least two characters in length')
    print('Username must only contain letters or numbers\n')
    while True:
        username = input('Enter username: ')
        if validate_new_username(username):
            print(Fore.BLUE + f'\nThank you. Your username is {username}')
            print(Style.RESET_ALL)
            username_password[0] = username
            choose_password()
            break

    return username


def validate_new_username(username):
    """
    Validates the users chosen username.
    Checks username is at least two characters long
    Checks username isn't already in use
    """
    try:
        if len(username) < 2:
            print(Fore.RED + 'Username must contain at least two characters')    
            print(Style.RESET_ALL)
            raise ValueError
        if username in current_usernames:
            print(Fore.RED + 'That username already exists')
            print(Style.RESET_ALL)
            raise ValueError
    except ValueError:
        print('Please choose another username')
        return False
    return True


def choose_password():
    """
    Asks the user to choose a password
    """
    print('\nPlease choose a password\n')
    print('Passwords must be at least 6 characters long')
    print('and contain at least one uppercase letter,')
    print('one lowercase letter,')
    print('one number')
    print('and one special character')
    print('special characters accepted are £, $, %, ^ or &\n')

    while True:
        new_password = input('Enter password here: \n')

        if validate_new_password(new_password):
            print(Fore.GREEN + 'Thank you. That password is valid')
            print(Style.RESET_ALL)
            username_password[1] = new_password
            user_worksheet = SHEET.worksheet('users')
            user_worksheet.append_row(username_password)
            add_new_user_worksheet(username_password[0])
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
            print(Fore.RED + 'Password must be at least 6 characters long')
            raise ValueError
        if not any(x.isupper() for x in new_password):
            print(Fore.RED + 'Password must contain 1 uppercase letter')
            raise ValueError
        if not any(x.islower() for x in new_password):
            print(Fore.RED + 'Password must contain 1 lowercase letter')
            raise ValueError
        special_characters = ['£', '$', '%', '^', '&']
        if not any(x in special_characters for x in new_password):
            print(Fore.RED + 'Password must contain either £, $, %, ^ or &')
            raise ValueError
        if not any(x.isdigit() for x in new_password):
            print(Fore.RED + 'Your password must include at least 1 number')
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
    SHEET.add_worksheet(username, rows="1", cols="7")
    SHEET.worksheet(username).append_row(['Date', 'Catergory', 'Amount'])


def get_existing_username_password():
    """
    Asks existing users to enter their username and password
    """
    while True:
        username = input('\nPlease enter your username: \n')
        password = input('\nPlease enter your password: \n')
        if validate_existing_username_password(username, password):
            username_password[0] = username
            print(username_password)
            print(Fore.BLUE + f'\nWelcome back {username}!\n')
            print(Style.RESET_ALL)
            break

    return username, password


def validate_existing_username_password(username, password):
    """
    Checks that the username inputted exists.
    Checks the password inputted matches the password stored
    """
    try: 
        if username == 'username':
            print(Fore.RED + 'username is not a valid option')
            raise ValueError
        if username not in current_usernames:
            print(Fore.RED + f"You entered {username}. Username doesn't exist")
            raise ValueError
        username_password_dic = dict(zip(current_usernames, current_passwords))
        users_password = username_password_dic[username]
        if password != users_password:        
            print(Fore.RED + 'Your username and password do not match')
            raise ValueError
    except ValueError: 
        print('Please try again')
        print(Style.RESET_ALL)
        return False
    return True

  
def choose_option():
    """
    gets the action option the user has chosen to do
    """
    print('What would you like to do today?\n')
    print('1 - Enter Transaction')
    print('2 - Analyse Spending\n')
    while True:
        option = input('Please pick an option, either 1 or 2: ')
        if option_validation(option):
            if option == '1':
                print('option 1 chosen')
                # get_transaction()
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
        print(Fore.RED + '\nYou did not enter a number!\n')
        print(Style.RESET_ALL)
    else:
        num_options = ['1', '2']
        try:
            if option not in num_options:
                raise ValueError
        except ValueError:
            print(Fore.RED + 'Not a valid number. Please try again.\n')
            print(Style.RESET_ALL)
            return False
        return True
    return option


def get_transaction():
    """
    Asks the user to enter the transaction date,
    the transaction category
    and the transaction amount
    """
    print('\nPlease enter the date of the transaction')
    print('This should be in the format DD/MM/YYYY')
    transaction = [] 
    while True:
        transaction_date = input('> ')
        if validate_date(transaction_date):
            transaction.append(transaction_date)     
            print('\nPlease enter the transaction category\n')
            print('1 - Household Bills')
            print('2 - Transportation')
            print('3 - Food')
            print('4 - Savings')
            print('5 - Personal Spending')
            print('6 - Other')
            while True:
                spend_category = input('\nEnter a number betweeen 1 and 6: ')
                if validate_spend_category(spend_category):
                    transaction.append(spend_category)     
                    print('\nPlease enter the amount spent.')
                    print('This should be in the format £xx.xx')
                    while True:
                        spend_amount = input('£ ')
                        if validate_amount(spend_amount):
                            transaction.append(spend_amount)
                            print('Adding transaction...')
                            add_transaction(transaction)
                            return False
                            break


def validate_date(date):
    """
    Validates that the date inputted is in the format DD/MM/YYYY
    """
    try:
        today = datetime.now()
        date_str = datetime.strptime(date, '%d/%m/%Y')
        if date_str > today:
            print(Fore.RED + 'The date cannot be in the future')
            raise ValueError
    except ValueError:
        print(Fore.RED + 'That is not a valid date. Please enter valid date')
        print(Style.RESET_ALL)
        return False
    return True


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


def validate_amount(float):
    """
    Validates that the amount entered is a float to two decimal places
    """
    try:
        if len(float.rsplit('.')[-1]) != 2:
            raise ValueError
    except ValueError:
        print(Fore.RED + 'This is not a correct amount')
        print('Please try again')
        print(Style.RESET_ALL)
        return False
    return True


def add_transaction(transaction):
    SHEET.worksheet(username_password[0]).append_row(transaction)


def main():
    """
    The main function that runs the rest of the functions
    """
    new_or_existing_choice = new_or_existing_user()
    if new_or_existing_choice == 'N':
        username = choose_username()
        print(Fore.BLUE + f'\nHi {username}!\n')
    elif new_or_existing_choice == 'E':
        get_existing_username_password()

    option = choose_option()
    if option == '1':
        get_transaction()  
    elif option == '2':
        print('TBC')


main()
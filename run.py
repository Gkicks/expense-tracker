import gspread
from google.oauth2.service_account import Credentials
import re
from datetime import datetime
from colorama import Fore, Style
import pwinput

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
USERNAME_PASSWORD = ['username', 'password']
# A list to hold the transaction details
TRANSACTION = []

# beginning title - reads EXPENSE TRANCKERS over two lines
print(Fore.BLUE + '                     __     __   __       __   __')
print(Fore.MAGENTA + '                    |__ \\/ |__| |__ |\\ | |__  |__')
print(Fore.RED + '                    |__ /\\ |    |__ | \\|  __| |__\n')
print(Fore.BLUE + '                    ___  __   __   __     __  __')
print(Fore.MAGENTA + '                     |  |__| |__| |   |/ |__ |__|')
print(Fore.RED + '                     |  |  \\ |  | |__ |\\ |__ |  \\ ')
print(Style.RESET_ALL)


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
    print('Username should be at least two characters in length\n')
    while True:
        username = input('Enter username: ').lower()
        if validate_new_username(username):
            print(Fore.BLUE + f'\nThank you. Your username is {username}')
            print(Style.RESET_ALL)
            USERNAME_PASSWORD[0] = username
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
            print(Fore.RED + 'Username must contain at least two charaters')
            print(Style.RESET_ALL)
            raise ValueError
        if username in CURRENT_USERNAMES:
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
    print('Please choose a password\n')
    print('Passwords must be at least 6 characters long,')
    print('contain at least one uppercase letter, one lowercase letter,')
    print('one number and one special character')

    while True:
        new_password = input('Enter password here: ')

        if validate_new_password(new_password):
            print(Fore.GREEN + 'Thank you. That password is valid')
            print(Style.RESET_ALL)
            USERNAME_PASSWORD[1] = new_password
            user_worksheet = SHEET.worksheet('users')
            user_worksheet.append_row(USERNAME_PASSWORD)
            add_new_user_worksheet(USERNAME_PASSWORD[0])
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
            print(Fore.RED + f'Password entered was {len(new_password)} long')
            print('Password must be at least 6 characters long')
            raise ValueError
        if not re.search('[A-Z]', new_password):
            print(Fore.RED + 'Password must contain 1 uppercase letter')
            raise ValueError
        if not re.search('[a-z]', new_password):
            print(Fore.RED + 'Password must contain 1 lowercase letter')
            raise ValueError
        if not re.search('[!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]', new_password):
            print(Fore.RED + 'Password must contain 1 special character')
            raise ValueError
        if not re.search('[0-9]', new_password):
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
    headings = ['Date', 'Catergory', 'Description', 'Amount']
    SHEET.worksheet(username).append_row(headings)


def get_existing_username():
    """
    Asks existing users to enter their existing username
    """
    while True:
        username = input('\nPlease enter your username: \n')
        if validate_existing_username(username):
            USERNAME_PASSWORD[0] = username
            break

    return username


def validate_existing_username(username):
    """
    Checks that the username inputted exists
    """
    try:
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
        password = pwinput.pwinput(prompt='\nPlease enter your password: ')
        pw_confirm = pwinput.pwinput(prompt='Please re-enter your password: ')
        if validate_existing_password(password, pw_confirm):
            print(Fore.BLUE + f'\nWelcome back {USERNAME_PASSWORD[0]}!\n')
            print(Style.RESET_ALL)
            break

    return


def validate_existing_password(password, pw_confirm):
    """
    Checks the password inputted matches the password stored
    """
    username_password_dic = dict(zip(CURRENT_USERNAMES, CURRENT_PASSWORDS))
    users_password = username_password_dic[USERNAME_PASSWORD[0]]
    try:
        if password != pw_confirm:
            print('\nThose passwords do not match')
            raise ValueError
        if password != users_password:
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
    print('\nPlease pick an option:\n')
    print('1 - Enter Transaction')
    print('2 - Analyse Spending')
    print('3 - View Transactions')
    print('4 - Quit\n')
    while True:
        option = input('Please pick an optionbetween 1 and 4: ')
        if option_validation(option):
            if option == '1':
                get_date()
            elif option == '2':
                pass
                # spending = analyse_transaction()
            elif option == '3':
                pass
            elif option == '4':
                print(Fore.MAGENTA + '\nThank you for using this tracker')
                print(f'Goodbye {USERNAME_PASSWORD[0]}\n')
                break
            else:
                print('Error! Please restart program')
            break
    return


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
    print('\nPlease enter the date of the transaction')
    print('This should be in the format DD/MM/YYYY')
    while True:
        transaction_date = input('\n> ')
        if validate_date(transaction_date):
            TRANSACTION.append(transaction_date)
            get_spend_category()
            break

    return


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
            TRANSACTION.append(spend_category)
            get_description()
            break

    return


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
    print('\nEnter a description of the spend')
    print('For example, "rent" or "lunch"')
    while True:
        spend_desc = input('> ')
        if validate_desc(spend_desc):
            TRANSACTION.append(spend_desc)
            get_amount()
            break

    return


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
    print('\nPlease enter the amount spent.')
    print('This should be a valid transaction cost')
    print('For example, £10 or £5.67')
    while True:
        spend_amount = input('£ ')
        if validate_amount(spend_amount):
            TRANSACTION.append(spend_amount)
            print(Fore.MAGENTA + '\nAdding transaction...')
            print(Style.RESET_ALL)
            next_choice()
            break

    return


def validate_amount(float_number):
    """
    Validates that the amount entered is a valid cash amount
    and that the amount is greater than 0
    """
    try:
        if not re.fullmatch(r'^\-?[0-9]+(?:\.[0-9]{2})?$', float_number):
            print(Fore.RED + 'The amount must be a valid cost amount')
            raise ValueError
        float_number = float(float_number)
        if float_number <= 0:
            print(Fore.RED + 'The amount must be greater than £0')
            raise ValueError
    except ValueError:
        print('Please try again')
        print(Style.RESET_ALL)
        return False
    return True


def add_transaction(transaction):
    """
    Adds the transation to the sheet of the current user
    """
    SHEET.worksheet(USERNAME_PASSWORD[0]).append_row(transaction)


# function is get further choice from user
def next_choice():
    """
    Allows the user to choose if they would like to perform another action
    """
    print(f'Thank you {USERNAME_PASSWORD[0]}. Your transaction has been added')
    print('What would you like to do next?\n')
    print('1 - Enter another transaction')
    print('2 - Return to the main menu')
    print('3 - Quit')
    while True:
        next_choice_action = input('\n> ').upper()
        if validate_next_choice(next_choice_action):
            if next_choice_action == '1':
                get_date()
                break
            elif next_choice_action == '2':
                main_menu()
                break
            elif next_choice_action == "3": 
                print(Fore.MAGENTA + '\nThank you for using this tracker')
                print(f'Goodbye {USERNAME_PASSWORD[0]}\n')
                break
    return


def validate_next_choice(letter):
    """
    Ensures the user only inputs one of the three options available.
    """
    next_choice_options = ['1', '2', '3']
    try:
        if letter not in next_choice_options:
            raise ValueError
    except ValueError:
        print(Fore.RED + 'You did not enter a correct value')
        print('Please enter a number between 1 and 3')
        print(Style.RESET_ALL)
        return False
    return True


# main function
def main():
    """
    The main function that runs the rest of the functions
    """
    new_or_existing_choice = new_or_existing_user()
    if new_or_existing_choice == 'N':
        username = choose_username()
        print(Fore.BLUE + f'Hi {username}!')
        print(Style.RESET_ALL)
    elif new_or_existing_choice == 'E':
        get_existing_username()
        get_existing_password()
    main_menu()


if __name__ == "__main__":
    main()

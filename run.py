import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('expense-tracker')

print('Welcome to the Python expense tracker!\n')


def get_username():
    """
    get the users name
    """
    while True:
        username = input('Please enter your name: ')

        if username_validation(username):
            break
    return username


def username_validation(username):
    """
    Raises NameError if username does not only contain letters
    """
    if username == "":
        print("\nYou didn't enter a name. Please try again\n")
    else:
        try:
            if username.isalpha() is not True:
                raise NameError('Your name should only contain letters')
        except NameError as e:
            print(f'{e}. {username} is not a valid name. Please try again\n')
            return False
        return True


def choose_option():
    print(f'\nHi {username}! What would you like to do today?\n')
    print('1-enter income')
    print('2-enter transactions')
    print('3-analyse transactions\n')
    while True:
        option = input('Please pick an option between 1 and 3: ')
        if option_validation(option):
            break
    return option


def option_validation(option):
    if option == "":
        print('\nYou did not enter a number!\n')
    else:
        num_options = ['1', '2', '3']
        try:
            if option not in num_options:
                raise NameError
        except NameError:
            print('Not a valid number. Please try again.\n')
            return False
        return True
    return option


username = get_username()
option = choose_option()

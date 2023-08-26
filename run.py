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


def new_or_existing_user():
    """
    Asks the user if they are a new or existing user
    """
    print('Are you a new or existing user?')
    print('N - new user')
    print('E - existing user')
    while True:
        new_or_existing_choice = input('Enter N or E: ').upper()
        # validate_new_user_option(new_or_existing_choice)
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
    if new_or_existing_choice == 'N':
        print('Please choose a username')
        print('Username should be at least two characters in length')
        print('Username must only contain letters or numbers')

        while True:
            new_username = input('Enter username: ')
        
            if validate_new_username(new_username):
                print(f'Thank you. Your username is {new_username}')
                choose_password()
                break

    return new_username


def validate_new_username(new_username):
    try:
        if len(new_username) < 2:
            raise ValueError
    except ValueError:
        print('Your username must contain at least two characters')
        return False
    return True
    
    
    # def get_username():
#     """
#     get the user's name
#     """
#     while True:
#         username = input('Please enter your name: ')

#         if username_validation(username):
#             break
#     return username


# def username_validation(username):
#     """
#     Raises NameError if username does not contain only letters
#     """
#     if username == "":
#         print("\nYou didn't enter a name. Please try again\n")
#     else:
#         try:
#             if username.isalpha() is not True:
#                 raise NameError('Your name should only contain letters')
#         except NameError as e:
#             print(f'{e}. {username} is not a valid name. Please try again\n')
#             return False
#         return True


def choose_option():
    """
    gets the action option the user has chosen to do
    """
    print(f'\nHi {username}! What would you like to do today?\n')
    print('1-enter income')
    print('2-enter transactions')
    print('3-analyse spending\n')
    while True:
        option = input('Please pick an option between 1 and 3: ')
        if option_validation(option):
            break
    return option


def option_validation(option):
    """
    Validates the option input
    """
    if option == "":
        print('\nYou did not enter a number!\n')
    else:
        num_options = ['1', '2', '3']
        try:
            if option not in num_options:
                raise ValueError
        except ValueError:
            print('Not a valid number. Please try again.\n')
            return False
        return True
    return option


# def add_income():
    

new_or_existing_choice = new_or_existing_user()
new_username = choose_username()
# username = get_username()
option = choose_option()

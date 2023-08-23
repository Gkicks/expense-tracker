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
    username = input('please enter your name: ')
    username_validation(username)

def username_validation(username):
    """
    Raises NameError if username does not only contain letters
    """
    if username == "":
        print("You didn't enter a name. Please try again")
    else: 
        try:
            if username.isalpha() != True:
                raise NameError('Your name should only contain letters')
        except NameError as e:
            print(f'{e}. {username} is not a valid name. Please try again')

get_username()



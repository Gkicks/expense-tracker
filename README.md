# Expense Tracker

The expense tracker is a useful tool for the user to track, view and analyse their spending.

![landing-page](assets/images/landing-page.png)

# Contents

- [Expense Tracker](#expense-tracker)
- [Contents](#contents)
- [User Experience (UX)](#user-experience-ux)
  - [Initial Discussion](#initial-discussion)
    - [Key Information for the Site](#key-information-for-the-site)
  - [User Stories](#user-stories)
    - [Client Goals](#client-goals)
    - [Visitor Goals](#visitor-goals)
- [Design](#design)
  - [Colour Scheme](#colour-scheme)
  - [Flowcharts](#flowcharts)
- [Features](#features)
  - [Existing Features](#existing-features)
    - [Landing Page](#landing-page)
    - [New User](#new-user)
    - [Existing User](#existing-user)
    - [Main Menu](#main-menu)
    - [Enter Transaction](#enter-transaction)
    - [Next Choice](#next-choice)
    - [Analyse Spending](#analyse-transaction)
    - [View Transactions](#view-transactions)
  - [Future Implementations](#future-implementations)
- [Technologies Used](#technologies-used)
  - [Languages Used](#languages-used)
  - [Frameworks, libraries and programs used](#frameworks-libraries-and-programs-used)
- [Deployment](#deployment)
- [Testing](#testing)
  - [PEP8 Vlaidator](#pep8-validator)
  - [Testing User Stories](#testing-user-stories)
    - [Client Goals](#client-goals-1)
    - [Visitor Goals](#visitor-goals-1)
  - [Full Testing](#full-testing)
    - [Landing Page](#landing-page-2)
    - [New User](#new-user-2)
    - [Existing User](#existing-user-2)
    - [Main Menu](#main-menu-2)
    - [Enter Transaction](#enter-transaction-2)
    - [Next Choice](#next-choice-2)
    - [Analyse Spending](#analyse-transaction-2)
    - [View Transactions](#view-transactions-2)
  - [Bugs](#bugs)
    - [Resolved Bugs](#resolved-bugs)
    - [Unresolved Bugs](#unresolved-bugs)
- [Credits](#credits)
  - [Code Used](#code-used)
  - [Content](#content)
  - [Media](#media)
  - [Other](#other)
  - [Acknowledgements](#acknowledgements)

[Back to top](#expense-tracker)

# User Experience (UX)

## Initial Discussion

The expense tracker is a tool for the user to keep track of their spending. 
The application is designed to be simple and intuitive, allowing the user to add transactions, analyse their spending and view their transactions

### Key Information for the Site

- New user to set up a new account
- Exisiting user to access their account
- Functions to;
    - Add transactions
    - Analyse spending
    - View transactions

## User Stories

### Client Goals

- A simple application that users will want to use
- An application that meets the user’s needs
- The user to feel their security is taken seriously

### Visitor Goals

#### New User Goals

- To be able to set up a new account
- To understand how to use the application
- To be able to choose their own username

#### Existing User Goals

- For personal data to be stored securely
- To access an exisiting account
- To be able to add transactions, by category and with a description
- To be able to view the sum and mean values of their transactions, by category, for a selected date range
- An option to view their transactions for a selected date range
- A pleasant user experience

[Back to top](#expense-tracker)

# Design

## Colour Scheme

I used the colorama library to style the font by colour. I chose to only change the font colour as I believe this makes the application look cleaner and more professional.
I chose the following colours for different commands:
    
- Red: to display error messages

![red-message](assets/images/red-message.png)

- Blue: welcoming messages for the user

![blue-message](assets/images/blue-message.png)

- Green: for valid inputs

![green-message](assets/images/green-message.png)

- Yellow: to display pandas dataframes

![yellow-message](assets/images/yellow-message.png)

- Magenta: to display the message when the transaction is being added and the user selects to quit 

![magenta-message](assets/images/magenta-message.png)

## Flowcharts

- The flowcharts were created using Miro

### User Experience

![user-experience-flowchart](assets/images/user-experience-flowchart.png)

### Python Validation

![user-experience-flowchart](assets/images/validation-flowchart.png)
import os

def main_menu():
    os.system('clear')
    print('******  ******  *****    **   **  **  **   **   ****   **   ')
    print('  **    **      **  **   *** ***  **  ***  **  **  **  **   ')
    print('  **    *****   *****    ** * **  **  ** * **  ******  **   ')
    print('  **    **      **  **   **   **  **  **  ***  **  **  **   ')
    print('  **    ******  **   **  **   **  **  **   **  **  **  *****')
    print('------------------------------------------------------------')
    print('   1. LOG IN   |    2. CREATE ACCOUNT     |     3. EXIT     ')
    print('------------------------------------------------------------')
    print('      ******  *****    ****   ******   *****  *****         ')
    print('        **    **  **  **  **  **   **  **     **  **        ')
    print('        **    *****   ******  **   **  ****   *****         ')
    print('        **    ** **   **  **  **   **  **     **  **        ')
    print('        **    **  **  **  **  ******   *****  ***  **       ')
    choice = input("\nWhat would you like to do? ")
    return choice

def us_exist(username):
    print('{} already exists. Please try again!'.format(username))
    input()

def create_account():
    os.system('clear')
    print('******  ******  *****    **   **  **  **   **   ****   **   ')
    print('  **    **      **  **   *** ***  **  ***  **  **  **  **   ')
    print('  **    *****   *****    ** * **  **  ** * **  ******  **   ')
    print('  **    **      **  **   **   **  **  **  ***  **  **  **   ')
    print('  **    ******  **   **  **   **  **  **   **  **  **  *****')
    print('------------------------------------------------------------')
    print('                       CREATE ACCOUNT                       ')
    print('------------------------------------------------------------')
    print('      ******  *****    ****   ******   *****  *****         ')
    print('        **    **  **  **  **  **   **  **     **  **        ')
    print('        **    *****   ******  **   **  ****   *****         ')
    print('        **    ** **   **  **  **   **  **     **  **        ')
    print('        **    **  **  **  **  ******   *****  ***  **       ')

def verify_login():
    os.system('clear')
    print('******  ******  *****    **   **  **  **   **   ****   **   ')
    print('  **    **      **  **   *** ***  **  ***  **  **  **  **   ')
    print('  **    *****   *****    ** * **  **  ** * **  ******  **   ')
    print('  **    **      **  **   **   **  **  **  ***  **  **  **   ')
    print('  **    ******  **   **  **   **  **  **   **  **  **  *****')
    print('------------------------------------------------------------')
    print('             ENTER CORRECT USERNAME & PASSWORD              ')
    print('------------------------------------------------------------')
    print('      ******  *****    ****   ******   *****  *****         ')
    print('        **    **  **  **  **  **   **  **     **  **        ')
    print('        **    *****   ******  **   **  ****   *****         ')
    print('        **    ** **   **  **  **   **  **     **  **        ')
    print('        **    **  **  **  **  ******   *****  ***  **       ')

def login_menu():
    os.system('clear')
    print('******  ******  *****    **   **  **  **   **   ****   **   ')
    print('  **    **      **  **   *** ***  **  ***  **  **  **  **   ')
    print('  **    *****   *****    ** * **  **  ** * **  ******  **   ')
    print('  **    **      **  **   **   **  **  **  ***  **  **  **   ')
    print('  **    ******  **   **  **   **  **  **   **  **  **  *****')
    print('------------------------------------------------------------')
    print('                         WELCOME!                           ')
    print('------------------------------------------------------------')
    print('      ******  *****    ****   ******   *****  *****         ')
    print('        **    **  **  **  **  **   **  **     **  **        ')
    print('        **    *****   ******  **   **  ****   *****         ')
    print('        **    ** **   **  **  **   **  **     **  **        ')
    print('        **    **  **  **  **  ******   *****  ***  **       ')
    print('------------------------------------------------------------')
    print('   1. BALANCE     |     2. DEPOSIT    |    3. VIEW SHARES   ')                           
    print('------------------------------------------------------------')
    print('   4. BUY/SELL    |     5. HISTORY    |    6. ACCOUNT INFO  ')
    print('------------------------------------------------------------')
    print('   7. SEND MONEY  |     8. TRADE      |    9. LOGOUT        ')
    print('------------------------------------------------------------')

def buy_menu():
    os.system('clear')
    print('******  ******  *****    **   **  **  **   **   ****   **   ')
    print('  **    **      **  **   *** ***  **  ***  **  **  **  **   ')
    print('  **    *****   *****    ** * **  **  ** * **  ******  **   ')
    print('  **    **      **  **   **   **  **  **  ***  **  **  **   ')
    print('  **    ******  **   **  **   **  **  **   **  **  **  *****')
    print('------------------------------------------------------------')
    print(' 1. LOOKUP PRICE  |   2. BUY   |   3. SELL   |   4. RETURN  ')
    print('------------------------------------------------------------')
    print('      ******  *****    ****   ******   *****  *****         ')
    print('        **    **  **  **  **  **   **  **     **  **        ')
    print('        **    *****   ******  **   **  ****   *****         ')
    print('        **    ** **   **  **  **   **  **     **  **        ')
    print('        **    **  **  **  **  ******   *****  ***  **       ')

def change_info():
    os.system('clear')
    print('******  ******  *****    **   **  **  **   **   ****   **   ')
    print('  **    **      **  **   *** ***  **  ***  **  **  **  **   ')
    print('  **    *****   *****    ** * **  **  ** * **  ******  **   ')
    print('  **    **      **  **   **   **  **  **  ***  **  **  **   ')
    print('  **    ******  **   **  **   **  **  **   **  **  **  *****')
    print('------------------------------------------------------------')
    print('                   CHANGE ACCOUNT INFO                      ')
    print('------------------------------------------------------------')
    print('      ******  *****    ****   ******   *****  *****         ')
    print('        **    **  **  **  **  **   **  **     **  **        ')
    print('        **    *****   ******  **   **  ****   *****         ')
    print('        **    ** **   **  **  **   **  **     **  **        ')
    print('        **    **  **  **  **  ******   *****  ***  **       ')
    print('------------------------------------------------------------')
    print('  1. USERNAME  |  2. PASSWORD   |  3. EMAIL   |  4. RETURN  ')                           
    print('------------------------------------------------------------')
def pass_dont_match():
    print('Passwords do not match. Try Again!')
    input()

def added(word):
    print("{} created.".format(word))
    input()

def not_added(word):
    print("{} not created. Try again!".format(word))
    input()

def incorrect_login():
    print('Username/Password not recognized.')

def bad_input():
    print('Bad Input. Try Again.')

def deposit_success(amount):
    print('You have deposited {} to your account.'.format(amount))
    input()

def buy_success(symbol,shares,price):
    symbol = symbol.upper()
    print('{} shares of {} have been added to your account for ${}.'.format(shares,symbol,round(price,2)))
    input()

def sell_success(symbol,shares,price):
    symbol = symbol.upper()
    print('{} shares of {} have been sold from your account for ${}.'.format(shares,symbol,round(price,2)))
    input()

def success_un(new_un):
    print('You have changed your Username to {}.'.format(new_un))

def success_new_em(em):
    print('You have changed you Email to {}.'.format(em))

def success_new_pw():
    print('You have change your password.')

def un_dont_match():
    print("Usernames don't match!")

def good_bye():
    print('Goodbye!')
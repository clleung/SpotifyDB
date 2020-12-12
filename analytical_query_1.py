#-----------------------------------------------------------------
# Working with psycopg2
#-----------------------------------------------------------------

import psycopg2
import sys
from prettytable import PrettyTable


def heading(str):
    print('-'*60)
    print("** %s:" % (str,))
    print('-'*60, '\n')    

SHOW_CMD = True
def print_cmd(cmd):
    if SHOW_CMD:
        print(cmd.decode('utf-8'))

def print_rows(rows):
    for row in rows:
        print(row)


#------------------------------------------------------------
# show_menu
#------------------------------------------------------------

def show_menu():
    menu = '''

--------------------------------------------------
1. List users 
2. Show user 
3. New user 
---
4. Show friends 
5. Add friend 
---
6. Make an Ad
7. Post message

Choose (1-7, 0 to quit): '''

    try:
        choice = int(input( menu ))
    except ValueError:
        print("\n\n* Invalid choice. Choose again.")
        show_menu()
    else:
        if choice == 0:
            print('Done.')
            cur.close()
            conn.close()
        elif choice in range(1,1+7):
            print()
            actions[choice]()
            show_menu()
        else:
            print("\n\n* Invalid choice (%s). Choose again." % choice)
            show_menu()
    finally:
        if cur != None:
            cur.close() 
        if conn != None:
            conn.close() 
    
#------------------------------------------------------------
# list_users
#------------------------------------------------------------

def list_users_menu():
    heading('List Users:')
    list_users()

def list_users():
    tmpl = '''
        SELECT *
          FROM Users as u
         ORDER BY username
    '''
    cur.execute(tmpl)
    rows = cur.fetchall()
    table = PrettyTable(['uid','username', 'email', 'country', 'fname', 'lname', 'join_date'])
    for row in rows:
        table.add_row(row)
    print(table)


#-----------------------------------------------------------------
# show_user
#-----------------------------------------------------------------

def show_user_menu():
    heading("Show User(s):")
    name = input('User name: ')
    show_user(name)
    
def show_user(name):
    tmpl = '''
        SELECT *
          FROM Users as u
         -- ILIKE is a case insensitive LIKE
         WHERE (username = %s );
    '''
    cmd = cur.mogrify(tmpl, ('%'+name+'%', '%'+name+'%'))
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    print_rows(rows)
    print()
    for row in rows:
        username, email, country, fname, lname, join_date, friend_username = row
        print("%s. %s, %s, %s, %s, %s (%s)" % (username, email, country, fname, lname, join_date, friend_username))


def show_user_by_id(id):
    pass

#-----------------------------------------------------------------
# new_user
#-----------------------------------------------------------------

def new_user_menu():
    heading("new_user")
    username = input('Username: ')
    email = input('Email: ')
    country = input('Country: ')
    fname = input('First name: ')
    lname = input('Last name: ')
    join_date = input('Date Joined: ')
    
    new_user(username=username, email=email, country=country, first_name=fname, last_name=lname, join_date=join_date)

def new_user(username, email, country, first_name, last_name, join_date):
    tmpl = '''
        INSERT INTO Users (username, email, country, fname, lname, join_date) VALUES (%s, %s, %s, %s, %s, %s)
    '''
    cmd = cur.mogrify(tmpl, (username, email, country, first_name, last_name, join_date))
    print_cmd(cmd)
    cur.execute(cmd)
    list_users()
    
#-----------------------------------------------------------------
# show_friends
#-----------------------------------------------------------------

def show_friends_menu():
    heading("Show friends")    
    uid = input("User id: ")
    show_friends(uid)

def show_friends(uid):
    tmpl = '''
        SELECT s.username, s.fname, s.lname
          FROM Friends as f
          JOIN Users as s
            ON s.uid = f.uid2
         WHERE f.uid1 = %s
    '''
    cmd = cur.mogrify(tmpl, (uid, ))
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    print_rows(rows)
    print()

#-----------------------------------------------------------------
# add_friend
#-----------------------------------------------------------------

def add_friend_menu():
    print("add_friend")
    userID = input("User ID: ")
    friend_userID = input("Friend's User ID: ")
    simultaneous_play = input("Play Music Together? (True/False): ")
    add_friend(userID, friend_userID, simultaneous_play)

def add_friend(userID, friend_userID, simultaneous_play):
    tmpl = '''
        INSERT INTO Friends (uid1, uid2, simultaneous_play) VALUES (%s, %s, %s)
    '''
    cmd = cur.mogrify(tmpl, (userID, friend_userID, simultaneous_play))
    print_cmd(cmd)
    cur.execute(cmd)
    cmd = cur.mogrify(tmpl, (friend_userID, userID, simultaneous_play))
    print_cmd(cmd)
    cur.execute(cmd)
    show_friends(userID)
    show_friends(friend_userID)
    
#-----------------------------------------------------------------
# show messages
#-----------------------------------------------------------------

def show_messages_menu():
    heading("show_messages")
    uid = input("User id: ")
    show_messages(uid)

def show_messages(uid):
    tmpl = '''
        SELECT m.message
          FROM Messages as m
          JOIN Users as u
            ON m.posted_by = u.uid
         WHERE %s = m.posted_to
    '''
    cmd = cur.mogrify(tmpl, (uid, ))
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    print_rows(rows)
    print()

#-----------------------------------------------------------------
# create ad
#-----------------------------------------------------------------
    
def make_ad_menu():
     heading("make_ad")
     duration = input("Ad Duration: ")
     frequency = input("Ad Frequency: ")
     ad_message = input("Ad Message: ")
     cost = input("Ad Cost: ")
     sponsorID = input("Sponsor ID: ")
     make_ad(duration, frequency, ad_message, cost, sponsorID)

def make_ad(duration, frequency, ad_message, cost, sponsorID):
    tmpl = '''INSERT INTO Ads (duration, frequency, information, cost, sponsor_id) VALUES (%s, %s, %s, %s, %s)'''
    cmd = cur.mogrify(tmpl, (duration, frequency, ad_message, cost, sponsorID))
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    print_rows(rows)
    print()
    
#-----------------------------------------------------------------
# post message
#-----------------------------------------------------------------

def post_message_menu():
    heading("post_message")
    posted_by = input('Posted by: ')
    posted_to = input("Posted to: ")
    message = input('Message: ')
    post_message(posted_by=posted_by, posted_to=posted_to, message=message)

def post_message(posted_by, posted_to, message):
    tmpl = '''
        INSERT INTO Messages (posted_by, posted_to, message) VALUES (%s, %s, %s)
    '''
    cmd = cur.mogrify(tmpl, (posted_by, posted_to, message))
    print_cmd(cmd)
    cur.execute(cmd)
    show_messages(posted_by)
    
# We leverage the fact that in Python functions are first class
# objects and build a dictionary of functions numerically indexed 

actions = { 1:list_users_menu,    2:show_user_menu,   3:new_user_menu,
            4:show_friends_menu,  5:add_friend_menu,
            6:make_ad_menu, 7:post_message_menu }


if __name__ == '__main__':
    try:
        # default database and user
        db, user = 'spotifydb', 'isdb'
        # you may have to adjust the user 
        # python a4-socnet-sraja.py a4_socnet postgres
        if len(sys.argv) >= 2:
            db = sys.argv[1]
        if len(sys.argv) >= 3:
            user = sys.argv[2]
        # by assigning to conn and cur here they become
        # global variables.  Hence they are not passed
        # into the various SQL interface functions
        conn = psycopg2.connect(database=db, user=user)
        conn.autocommit = True
        cur = conn.cursor()
        show_menu()
    except psycopg2.Error as e:
        print("Unable to open connection: %s" % (e,))

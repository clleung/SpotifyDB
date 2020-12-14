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
    This is Simple Query 3

    User Story 6: 
        As a listener, I want to find my friends on Spotify, so that I can 
        listen to music with them

--------------------------------------------------
1. List users 
2. New user 
---
3. Show friends 
4. Add friend 
5. List all Friends

Choose (1-5, 0 to quit): '''

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
        elif choice in range(1,1+5):
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
         ORDER BY uid DESC
    '''
    cur.execute(tmpl)
    rows = cur.fetchall()
    table = PrettyTable(['uid', 'username', 'email', 'country', 'fname', 'lname', 'join_date'])
    for row in rows:
        table.add_row(row)
    print(table)
  
#-----------------------------------------------------------------
# show_friends
#-----------------------------------------------------------------

def show_friends_menu():
    heading("Show friends")    
    uid = 1
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
    table = PrettyTable(['username', 'fname', 'lname'])
    for row in rows:
        table.add_row(row)
    print(table)

def list_friends_menu():
    heading('Shows who is friends with who')
    list_friends()

def list_friends():
    tmpl = '''
        SELECT *
          FROM Friends
         ORDER BY uid1 DESC
    '''
    cur.execute(tmpl)
    rows = cur.fetchall()
    table = PrettyTable(['uid1', 'uid2', 'simultaneous_play'])
    for row in rows:
        table.add_row(row)
    print(table)

#-----------------------------------------------------------------
# add_friend
#-----------------------------------------------------------------

def add_friend_menu():
    print('''Adds a friend''')
    userID = "1"
    friend_userID = "4"
    simultaneous_play = "True"
    
    print('User ID: ' + userID)
    print('Friend ID: ' + friend_userID)
    print('Play Music Together?: ' + simultaneous_play)

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


# We leverage the fact that in Python functions are first class
# objects and build a dictionary of functions numerically indexed 

actions = { 1:list_users_menu,  2:new_user_menu,
            3:show_friends_menu, 4:add_friend_menu, 5:list_friends_menu}


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

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
---
2. Stream Song
3. List all Streams
4. Count the Plays a User has Played a Song

Choose (1-4, 0 to quit): '''

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
        elif choice in range(1,1+4):
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
# play song
#----------------------------------------------------------------- 

def play_song_menu():
    heading("play a song")
    uid = "12"
    song_id = "4"
    date = "2020-12-04"
    time = "01:15:12"
    play_song(uid, song_id, date, time)

def play_song(uid, song_id, date, time):
    tmpl = '''INSERT INTO Stream (uid, song_id, date, time) VALUES (%s, %s, %s, %s)'''
    cmd = cur.mogrify(tmpl, (uid, song_id, date, time))
    print_cmd(cmd)
    cur.execute(cmd)
    list_streams()

def list_streams_menu():
    heading("Shows all streams")
    list_streams()

def list_streams():
    tmpl = '''
        SELECT *
          FROM Stream
         ORDER BY stream_id DESC
    '''
    cur.execute(tmpl)
    rows = cur.fetchall()
    table = PrettyTable(['stream_id', 'uid', 'song_id', 'date', 'time'])
    for row in rows:
        table.add_row(row)
    print(table)

#-----------------------------------------------------------------
# count plays
#----------------------------------------------------------------- 

def count_plays_menu():
    heading('''User Story 7 (Analytical):
                As a listener, I want to find out how many times I've listened
                to a song so that I can see what I'm doing with my time''')
    uid = "1"
    song_id = "5"
    count_plays(uid, song_id)

def count_plays(uid, song_id):
    tmpl = '''SELECT count(song_id)
                FROM Stream
               WHERE (uid = %s) and (song_id = %s)'''
    cmd = cur.mogrify(tmpl, (uid, song_id))
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    table = PrettyTable(['song_id'])
    for row in rows:
        table.add_row(row)
    print(table)


# We leverage the fact that in Python functions are first class
# objects and build a dictionary of functions numerically indexed 

actions = { 1:list_users_menu,  2:play_song_menu, 
            3:list_streams_menu, 4:count_plays_menu }


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

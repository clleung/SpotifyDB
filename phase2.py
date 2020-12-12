#-----------------------------------------------------------------
# Working with psycopg2
#-----------------------------------------------------------------

import psycopg2
import sys
from prettytable import from_csv
with open("Users.csv") as fp:
    mytable = from_csv(fp)

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
3. New user 
---
3. Show friends 
4. Add friend 
---
5. Make an Ad
6. Show Ad
---
7. Stream Song
8. Count the Plays a User has Played a Song
---
9. Make External Ad
10. Make Artist Ad

Choose (1-11, 0 to quit): '''

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
        elif choice in range(1,1+10):
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
    print_rows(rows)
    print()
    for row in rows:
        username, email, country, fname, lname, join_date, friend_username = row
        print("%s. %s, %s, %s, %s, %s (%s)" % (username, email, country, fname, lname, join_date, friend_username))

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
# show ad
#----------------------------------------------------------------- 

def show_ad_menu():
    heading("show_ad")
    ad_id = input("Ad ID: ")
    show_ad(ad_id)

def show_ad(ad_id):
    tmpl = '''
        SELECT *
          FROM Ads
    '''
    cmd = cur.mogrify(tmpl, (ad_id))
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    print_rows(rows)
    print()

#-----------------------------------------------------------------
# play song
#----------------------------------------------------------------- 

def play_song_menu():
    heading("play a song")
    uid = input("User ID: ")
    song_id = input("Song ID: ")
    date = input("Date: ")
    time = input("Time: ")
    play_song(uid, song_id, date, time)

def play_song(uid, song_id, date, time):
    tmpl = '''INSERT INTO Stream (uid, song_id, date, time) VALUES (%s, %s, %s, %s)'''
    cmd = cur.mogrify(tmpl, (uid, song_id, date, time))
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    print_rows(rows)
    print()


#-----------------------------------------------------------------
# count plays
#----------------------------------------------------------------- 

def count_plays_menu():
    heading("count number of plays a song has")
    uid = input("User ID: ")
    song_id = input("Song ID: ")
    count_plays(uid, song_id)

def count_plays(uid, song_id):
    tmpl = '''SELECT count(song_id)
                FROM Stream
               WHERE (uid = %s) and (song_id = %s)'''
    cmd = cur.mogrify(tmpl, (uid, song_id))
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    print_rows(rows)
    print()

#-----------------------------------------------------------------
# make external ad
#----------------------------------------------------------------- 

def make_external_ad_menu():
    heading("make_external_ad")
    adID = input("Ad ID: ")
    clientName = input("Client Name: ")
    make_external_ad(adID, clientName)

def make_external_ad(adID, clientName):
    tmpl = '''INSERT INTO External_Ads (ad_id, client_name) VALUES (%s, %s)'''
    cmd = cur.mogrify(tmpl, (adID, clientName))
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    print_rows(rows)
    print()

#-----------------------------------------------------------------
# make artist ad
#----------------------------------------------------------------- 

def make_artist_ad_menu():
    heading("make_artist_ad")
    adID = input("Ad ID: ")
    artistID = input("Artist ID: ")
    eventDate = input("Event Date: ")
    make_external_ad(adID, artistID, eventDate)

def make_external_ad(adID, artistID, eventDate):
    tmpl = '''INSERT INTO Artist_Ads (adID, artistID, eventDate) VALUES (%s, %s, %s)'''
    cmd = cur.mogrify(tmpl, (adID, artistID, eventDate))
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    print_rows(rows)
    print()

# We leverage the fact that in Python functions are first class
# objects and build a dictionary of functions numerically indexed 

actions = { 1:list_users_menu,  2:new_user_menu,
            3:show_friends_menu,  4:add_friend_menu,
            5:make_ad_menu, 6:show_ad_menu, 7:play_song_menu,
            8:count_plays_menu, 9:make_external_ad_menu, 10:make_artist_ad_menu }


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

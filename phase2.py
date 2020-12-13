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
2. New user 
---
3. Show friends 
4. Add friend 
5. List all Friends
---
6. Make an Ad
7. Show Ad
8. List all Ads
---
9. Stream Song
10. List all Streams
11. Count the Plays a User has Played a Song
---
12. Make External Ad
13. List External Ads
14. Make Artist Ad
15. List Artist Ads

Choose (1-15, 0 to quit): '''

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
        elif choice in range(1,1+15):
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

def list_ads_menu():
    heading("Shows all ads made")
    list_ads()

def list_ads():
    tmpl = '''
        SELECT *
          FROM Ads
         ORDER BY ad_id DESC
    '''
    cur.execute(tmpl)
    rows = cur.fetchall()
    table = PrettyTable(['ad_id', 'duration', 'frequency', 'information', 'cost', 'sponsor_id'])
    for row in rows:
        table.add_row(row)
    print(table)


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

def list_external_ads_menu():
    heading("Shows all external ads made")
    list_external_ads()

def list_external_ads():
    tmpl = '''
        SELECT *
          FROM External_Ads
         ORDER BY ad_id DESC
    '''
    cur.execute(tmpl)
    rows = cur.fetchall()
    table = PrettyTable(['ad_id', 'client_name'])
    for row in rows:
        table.add_row(row)
    print(table)

#-----------------------------------------------------------------
# make artist ad
#----------------------------------------------------------------- 

def make_artist_ad_menu():
    heading("make_artist_ad")
    adID = input("Ad ID: ")
    artistID = input("Artist ID: ")
    eventDate = input("Event Date: ")
    make_artist_ad(adID, artistID, eventDate)

def make_artist_ad(adID, artistID, eventDate):
    tmpl = '''INSERT INTO Artist_Ads (adID, artistID, eventDate) VALUES (%s, %s, %s)'''
    cmd = cur.mogrify(tmpl, (adID, artistID, eventDate))
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    print_rows(rows)
    print()

def list_artist_ads_menu():
    heading("Shows all artists ads made")
    list_artist_ads()

def list_artist_ads():
    tmpl = '''
        SELECT *
          FROM Artist_Ads
         ORDER BY ad_id DESC
    '''
    cur.execute(tmpl)
    rows = cur.fetchall()
    table = PrettyTable(['ad_id', 'artist_id', 'event_date'])
    for row in rows:
        table.add_row(row)
    print(table)

# We leverage the fact that in Python functions are first class
# objects and build a dictionary of functions numerically indexed 

actions = { 1:list_users_menu,  2:new_user_menu,
            3:show_friends_menu, 4:add_friend_menu, 5:list_friends_menu,
            6:make_ad_menu, 7:show_ad_menu, 8:list_ads_menu, 
            9:play_song_menu, 10:list_streams_menu, 11:count_plays_menu, 
            12:make_external_ad_menu, 13:list_external_ads_menu, 
            14:make_artist_ad_menu, 15:list_artist_ads_menu }


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

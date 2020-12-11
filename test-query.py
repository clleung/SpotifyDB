#-----------------------------------------------------------------
# Working with psycopg2
#-----------------------------------------------------------------

import psycopg2
import sys

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
    
#-----------------------------------------------------------------
# post_song
#-----------------------------------------------------------------

def post_song():
    print("post_song")
    songname = input("Song Name: ")
    release_date = input("Release Date: (yyyy-mm-dd) ")
    genre = input("Genre: ")
    num_plays = ("Number of Plays: ")
    duration = ("Duration: ")
    artist_name = ("Artist Name: ")

    add_song(songname, release_date, genre, num_plays, duration, artist_name)

def add_song(songname, release_date, genre, num_plays, duration, artist_name):
    tmpl = '''
        INSERT INTO Songs (songname, release_date, genre, num_plays, duration, artist_name)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''
    cmd = cur.mogrify(tmpl, (songname, release_date, genre, num_plays, duration, artist_name))
    print_cmd(cmd)
    cur.execute(cmd)
    cmd = cur.mogrify(tmpl, (songname, release_date, genre, num_plays, duration, artist_name))
    print_cmd(cmd)
    cur.execute(cmd)
    show_songs(artist_name)
    
#-----------------------------------------------------------------
# show_songs
#-----------------------------------------------------------------

def show_songs_menu():
    heading("Show songs")    
    songname = input("Song Name: ")
    show_songs(songname)

def show_songs(songname):
    tmpl = '''
        SELECT song_name, release_date, genre, num_plays, duration, artist_id
          FROM songs as f
          JOIN Users as s
            ON s.uid = f.uid_2
         WHERE f.uid_1 = %s
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
    username = input("Username: ")
    friend_username = input("Friend's Username: ")
    add_friend(username, friend_username)

def add_friend(username, friend_username):
    tmpl = '''
        INSERT INTO Users (username, friend_username) VALUES (%s, %s)
    '''
    cmd = cur.mogrify(tmpl, (username, friend_username))
    print_cmd(cmd)
    cur.execute(cmd)
    cmd = cur.mogrify(tmpl, (friend_username, username))
    print_cmd(cmd)
    cur.execute(cmd)
    show_friends(username)
    show_friends(friend_username)
    
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


    
# We leverage the fact that in Python functions are first class
# objects and build a dictionary of functions numerically indexed 

actions = { 1:list_users_menu,    2:show_user_menu,   3:new_user_menu,
            4:show_friends_menu,  5:add_friend_menu,
            6:show_messages_menu, 7:post_message_menu }


if __name__ == '__main__':
    try:
        # default database and user
        db, user = 'socnet', 'isdb'
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
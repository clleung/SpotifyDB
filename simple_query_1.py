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
This is simple_query_1

User Story 1:
As an Artist, 
I want to post songs 
so that I can gain revenue and followers.
--------------------------------------------------
1. List Songs
2. New Song

Choose (1-2, 0 to quit): '''

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
        elif choice in range(1, 1+2):
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
# list_songs
#------------------------------------------------------------

def list_songs_menu():
    heading('List Users:')
    list_songs()

def list_songs():
    tmpl = '''
        SELECT *
          FROM Songs as s
         ORDER BY song_id DESC
    '''
    cur.execute(tmpl)
    rows = cur.fetchall()
    table = PrettyTable(['song_id','song_name','release_date','genre','num_plays','duration','artist_id'])
    for row in rows:
        table.add_row(row)
    print(table)


#-----------------------------------------------------------------
# new_song
#-----------------------------------------------------------------

def new_song_menu():
    heading('''
            new_song: this query will add in a new song: "Vibes for Quarantine"

            we will be inserting it into the Songs table, and print the table with the most recent 
            entry on top ("High Hopes" before the query and "Vibes for Quarantine" after)

            we have hard coded these values:
            
                song_name = "Vibes for Quarantine"
                release_date = "2020-04-04"
                genre = "Chill"
                num_plays = "100000"
                duration = "0:02:10"
                artist_id = 2
    ''')
    song_name = "Vibes for Quarantine"
    release_date = "2020-04-04"
    genre = "Chill"
    num_plays = "100000"
    duration = "0:02:10"
    artist_id = 2
    
    new_song(song_name = song_name, release_date = release_date, genre = genre, num_plays = num_plays, duration = duration, artist_id = artist_id)

def new_song(song_name, release_date, genre, num_plays, duration, artist_id):
    tmpl = '''
        INSERT INTO Songs (song_name, release_date, genre, num_plays, duration, artist_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''
    cmd = cur.mogrify(tmpl, (song_name, release_date, genre, num_plays, duration, artist_id))
    print_cmd(cmd)
    cur.execute(cmd)
    print("note that Vibes for Quarantine is a new song in the table")
    list_songs()
    

    
# We leverage the fact that in Python functions are first class
# objects and build a dictionary of functions numerically indexed 

actions = { 1:list_songs_menu,    2:new_song_menu }


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

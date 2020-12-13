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
This is analytical_query_1

User Story 2:
As an Artist,
I want to see how many people stream my content 
so that I know what kind of content I should create in the future and what my followers like.
--------------------------------------------------
1. List All Artists and Streams
2. View Total Streamers

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
# list_artists_and_streams
#------------------------------------------------------------

def list_artists_and_streams_menu():
    heading('List Artists and Streams:')
    list_artists_and_streams()

def list_artists_and_streams():
    tmpl1 = '''
        SELECT *
          FROM Artists as s
         ORDER BY artist_id DESC
    '''
    cur.execute(tmpl1)
    rows = cur.fetchall()
    table1 = PrettyTable(['artist_id','artist_name','monthly_listeners'])
    for row in rows:
        table1.add_row(row)
    print(table1)

    tmpl2 = '''
        SELECT *
          FROM Stream as s
         ORDER BY stream_id DESC
    '''
    cur.execute(tmpl2)
    rows = cur.fetchall()
    table2 = PrettyTable(['stream_id','uid','song_id', 'date', 'time'])
    for row in rows:
        table2.add_row(row)
    print(table2)




#-----------------------------------------------------------------
# new_song
#-----------------------------------------------------------------

def view_streamers_menu():
    heading('''
            view_streamers: this query will add in a new song: "Vibes for Quarantine"

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
    
    view_streamers(artist_id = artist_id)

def view_streamers(artist_id):
    tmpl = '''
        SELECT a.artist_id, a.artist_name, so.song_id, so.song_name, COUNT(st.song_id)
          FROM Artists as a
          JOIN Songs as so 
               ON a.artist_id = so.artist_id
          JOIN Stream as st
               ON so.song_id = st.song_id
         WHERE (a.artist_id = %s)
         GROUP BY a.artist_id, so.song_id
         
    '''
    cmd = cur.mogrify(tmpl, (artist_id,))
    print_cmd(cmd)
    cur.execute(cmd)
    
    rows = cur.fetchall()
    table = PrettyTable(['artist_id', 'artist_name', 'song_id', 'song_name', 'stream_count'])
    for row in rows:
        table.add_row(row)
    print(table)
    

    
# We leverage the fact that in Python functions are first class
# objects and build a dictionary of functions numerically indexed 

actions = { 1:list_artists_and_streams_menu,    2:view_streamers_menu }


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

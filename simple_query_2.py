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
This is simple_query_2

User Story 4:
As an Artist, 
I want to take down content
so that I can post my content with a different company
--------------------------------------------------
1. List Songs and Streams
2. Delete All Songs (and stream history as a result)

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
# list_songs_and_streams
#------------------------------------------------------------

def list_songs_and_streams_menu():
    heading('List Songs and Streams:')
    list_songs_and_streams()

def list_songs_and_streams():
    tmpl = '''
        SELECT *
          FROM Songs as s
         ORDER BY song_id DESC
    '''
    cur.execute(tmpl)
    rows = cur.fetchall()
    table = PrettyTable(['song_id','song_name','release_date','genre','duration','artist_id'])
    for row in rows:
        table.add_row(row)
    print(table)

    tmpl2 = '''
        SELECT *
          FROM Stream as s
         ORDER BY stream_id DESC
    '''
    cur.execute(tmpl2)
    rows = cur.fetchall()
    table1 = PrettyTable(['stream_id','uid','song_id', 'date', 'time'])
    for row in rows:
        table1.add_row(row)
    print(table1)


#-----------------------------------------------------------------
# delete_all_songs
#-----------------------------------------------------------------

def delete_all_songs_menu():
    heading('''
            delete_all_songs: this query will delete all songs under the provided artist_id 2, or Justhis
            
            this user story requires a deletion in the Stream and a deletion in the Songs tables,
            as song_id is used in both Stream and Songs and there cannot be any dangling references.

            if you run simple_query_1.py before this, both Vibes for Quarantine and That Ain't Real will be deleted

            we also will not be deleting the account, as the user story is just for deleting all songs.
            
    ''')
   
    artist_id = 2
    
    delete_all_songs(artist_id = artist_id)

def delete_all_songs(artist_id):
    tmpl = '''
        DELETE FROM Stream as st
         WHERE (st.song_id IN (SELECT so.song_id
                                FROM Songs as so
                               WHERE (so.artist_id = %s)))
        
    '''
    cmd = cur.mogrify(tmpl, (artist_id,))
    print_cmd(cmd)
    cur.execute(cmd)

    tmpl2 = '''
        DELETE FROM Songs as s
         WHERE (s.artist_id = %s)
    '''
    cmd2 = cur.mogrify(tmpl2, (artist_id,))
    print_cmd(cmd2)
    cur.execute(cmd2)
    print("Note that This Ain't Real from the Songs Table and stream_id 5 (or song_id 1) have been deleted from the Stream Table")
    list_songs_and_streams()
    

    
# We leverage the fact that in Python functions are first class
# objects and build a dictionary of functions numerically indexed 

actions = { 1:list_songs_and_streams_menu,    2:delete_all_songs_menu }


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

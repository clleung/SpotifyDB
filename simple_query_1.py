import psycopg2
import sys    
from prettytable import from_csv
with open("Songs.csv") as fp:
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
Simple Query 1:
As an Artist, I want to post songs so that I can gain revenue and followers.
--------------------------------------------------

1. Add Song

Select 1 to start, 0 to quit: '''

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
        elif choice == 1:
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
    
#-----------------------------------------------------------------
# print the PrettyTable
#-----------------------------------------------------------------
print("Below is the Songs Table")

x = mytable
x.align = "r"
print("Songs Table")
print(x)

#-----------------------------------------------------------------
# post_song
#-----------------------------------------------------------------

def post_song():
    print("post_song")
    songname = input("Song Name: ")
    release_date = input("Release Date: (yyyy-mm-dd) ")
    genre = input("Genre: ")
    num_plays = input("Number of Plays: ")
    duration = input("Duration: ")
    artist_name = input("Artist Name: ")

    add_song(songname, release_date, genre, num_plays, duration, artist_id)

def add_song(songname, release_date, genre, num_plays, duration, artist_id):
    tmpl = '''
        INSERT INTO Songs (songname, release_date, genre, num_plays, duration, artist_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''
    cmd = cur.mogrify(tmpl, (songname, release_date, genre, num_plays, duration, artist_id))
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    print_rows(rows)
    print()

print("Song Name: Vibes for Quarantine")
print("Release Date: 2020-04-04")
print("Genre: Chill")
print("Number of Plays: 100000")
print("Duration: 0:02:10")
print("Artist Id: 2")

add_song("Vibes for Quarantine", "2020-04-04", "Chill", "100000", "0:02:10", "2")
x.align = "r"
print("Songs Table")
print(x)


actions = { 1:add_song}


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

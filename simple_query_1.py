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

    '''
    print(menu)
    
#-----------------------------------------------------------------
# print the PrettyTable
#-----------------------------------------------------------------
print("Below is the Songs Table")

x = mytable
x.align = "r"
print("Songs Table")
print(x)

#-----------------------------------------------------------------
# list_songs
#-----------------------------------------------------------------
def list_users():
    tmpl = '''
        SELECT *
          FROM Songs as s
         ORDER BY song_id ASC
    '''
    cur.execute(tmpl)
    rows = cur.fetchall()
    print_rows(rows)
    print()
    for row in rows:
        username, email, country, fname, lname, join_date, friend_username = row
        print("%s. %s, %s, %s, %s, %s (%s)" % (username, email, country, fname, lname, join_date, friend_username))

#-----------------------------------------------------------------
# show_song
#-----------------------------------------------------------------

def show_song():
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
    for row in rows:
        username, email, country, fname, lname, join_date, friend_username = row
        print("%s. %s, %s, %s, %s, %s (%s)" % (username, email, country, fname, lname, join_date, friend_username))
        
#-----------------------------------------------------------------
# add_song
#-----------------------------------------------------------------

def add_song(song_name, release_date, genre, num_plays, duration, artist_id):
    tmpl = '''
        INSERT INTO Songs (song_name, release_date, genre, num_plays, duration, artist_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''
    cmd = cur.mogrify(tmpl, (song_name, release_date, genre, num_plays, duration, artist_id))
    print_cmd(cmd)
    cur.execute(cmd)
    show_friends(userID)
    


#-----------------------------------------------------------------
# song details we are adding
#-----------------------------------------------------------------
print("Song Name: Vibes for Quarantine")
print("Release Date: 2020-04-04")
print("Genre: Chill")
print("Number of Plays: 100000")
print("Duration: 0:02:10")
print("Artist Id: 2")



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

add_song("Vibes for Quarantine", "2020-04-04", "Chill", "100000", "0:02:10", "2")
x.align = "r"
print("Songs Table")
print(x)

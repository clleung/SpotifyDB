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
    This is Complex Query 3

    User Story 10:
        As a sponsor, I want to advertise new releases for my content creator
        so that they can get more followers (increasing followers and royalties) 
        and specifically reach out to their current followers


--------------------------------------------------
1. List artists
---
2. Make an Ad
4. List all Ads
---
4. Make Artist Ad
5. List Artist Ads

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

def list_artists_menu():
    heading('List Artists:')
    list_artists()

def list_artists():
    tmpl = '''
        SELECT *
          FROM Artists as u
         ORDER BY artist_id DESC
    '''
    cur.execute(tmpl)
    rows = cur.fetchall()
    table = PrettyTable(['artist_id', 'artist_name', 'monthly_listeners'])
    for row in rows:
        table.add_row(row)
    print(table)

#-----------------------------------------------------------------
# create ad
#-----------------------------------------------------------------
    
def make_ad_menu():
     heading('''Make an AD''')
     duration = "00:00:15"
     frequency = "1500"
     ad_message = "Welcome to McDonald's"
     cost = "$999.00"
     sponsorID = "8"
     make_ad(duration=duration, frequency=frequency, information=ad_message, cost=cost, sponsor_id=sponsorID)

def make_ad(duration, frequency, information, cost, sponsor_id):
    tmpl = '''INSERT INTO Ads (duration, frequency, information, cost, sponsor_id) VALUES (%s, %s, %s, %s, %s)'''
    cmd = cur.mogrify(tmpl, (duration, frequency, information, cost, sponsor_id))
    print_cmd(cmd)
    cur.execute(cmd)
    list_ads()

#-----------------------------------------------------------------
# show ad
#----------------------------------------------------------------- 

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
# make artist ad
#----------------------------------------------------------------- 

def make_artist_ad_menu():
    heading('Make artist ad')
    adID = "11"
    artistID = "5"
    eventDate = "2019-12-01"
    print("Ad ID: " + adID)
    print("Artist ID: " + artistID)
    print("Event Date: " + eventDate)
    make_artist_ad(adID, artistID, eventDate)

def make_artist_ad(adID, artistID, eventDate):
    tmpl = '''INSERT INTO Artist_Ads (ad_id, artist_id, event_date) VALUES (%s, %s, %s)'''
    cmd = cur.mogrify(tmpl, (adID, artistID, eventDate))
    print_cmd(cmd)
    cur.execute(cmd)
    list_artist_ads()

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


actions = { 1:list_artists_menu,  2:make_ad_menu, 
            3:list_ads_menu, 4:make_artist_ad_menu, 
            5:list_artist_ads_menu }


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

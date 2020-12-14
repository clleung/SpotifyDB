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
    This is Complex Query 2

    User Story 9:
    As an advertiser, I want to advertise on the homepage so that
    I can increase ny client base and have more people use my goods
    and services (external company)

    This query lets us classify if an ad is an external ad
    by having us insert the ad into the external ads table
    using the ad_id
--------------------------------------------------
1. List users 
---
2. Make an Ad
3. Show Ad
4. List all Ads
---
5. Make External Ad
6. List External Ads


Choose (1-6, 0 to quit): '''

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
        elif choice in range(1,1+6):
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
# create ad
#-----------------------------------------------------------------
    
def make_ad_menu():
     heading('''Make a new ad''')
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

def show_ad_menu():
    heading("show_ad")
    ad_id = input("Ad ID: ")
    show_ad(ad_id)

def show_ad(ad_id):
    tmpl = '''
        SELECT *
          FROM Ads
         WHERE (ad_id = %s)
    '''
    cmd = cur.mogrify(tmpl, (ad_id))
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    table = PrettyTable(['ad_id', 'duration', 'frequency', 'information', 'cost', 'sponsor_id'])
    for row in rows:
        table.add_row(row)
    print(table)

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
# make external ad
#----------------------------------------------------------------- 

def make_external_ad_menu():
    heading('''Makes an ad an external ad''')
    adID = "12"
    clientName = "Pokimane"
    make_external_ad(adID, clientName)

def make_external_ad(adID, clientName):
    tmpl = '''INSERT INTO External_Ads (ad_id, client_name) VALUES (%s, %s)'''
    cmd = cur.mogrify(tmpl, (adID, clientName))
    print_cmd(cmd)
    cur.execute(cmd)
    list_external_ads()

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


# We leverage the fact that in Python functions are first class
# objects and build a dictionary of functions numerically indexed 

actions = { 1:list_users_menu, 2:make_ad_menu, 3:show_ad_menu, 4:list_ads_menu, 
            5:make_external_ad_menu, 6:list_external_ads_menu}


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

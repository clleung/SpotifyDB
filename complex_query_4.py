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
    This is Complex Query 4

    User Story 11: 
        As a sponsor, I want to find out how much my ads
        have cost me

    This query will give the sponsor how much his ad costs given
    his uid and the ad_id.
--------------------------------------------------
1. List all Ads
2. Find ad cost


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
        elif choice in range(1,1+2):
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
# find ad cost
#----------------------------------------------------------------- 

def find_ad_cost_menu():
    heading("Finds the cost of an ad")
    sponsorID = "6"

    print("Sponsor ID: " + sponsorID)
    find_ad_cost(sponsorID)

def find_ad_cost(sponsorID):
    tmpl = '''
        SELECT s.sponsor_id, s.sponsor_name, a.ad_id, a.duration, a.frequency, a.information, a.cost
          FROM Sponsors as s
          JOIN Ads as a 
               ON s.sponsor_id = a.sponsor_id
         WHERE (s.sponsor_id = %s)
    '''
    cmd = cur.mogrify(tmpl, (sponsorID,))
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    table = PrettyTable(['sponsor_id', 'sponsor_name', 'ad_id', 'duration','frequency', 'information', 'cost'])
    for row in rows:
        table.add_row(row)
    print(table)


actions = { 1:list_ads_menu, 2:find_ad_cost_menu}


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

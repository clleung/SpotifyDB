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
This is complex_query_4

User Story 11:
As an Sponsor, 
I want to find out how much my ads have cost me in the past
so that I can budget accordingly and decide how I’ll advertise on Spotify in the future.
--------------------------------------------------
1. List Sponsors and Ads
2. Get Song and Creator Info

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
# list_sponsors_and_ads
#------------------------------------------------------------

def list_sponsors_and_ads_menu():
    heading('List Artists and Songs:')
    list_sponsors_and_ads()

def list_sponsors_and_ads():

    tmpl1 = '''
        SELECT *
          FROM Sponsors as s
         ORDER BY sponsor_id DESC
    '''
    cur.execute(tmpl1)
    rows = cur.fetchall()
    table1 = PrettyTable(['sponsor_id','sponsor_name'])
    for row in rows:
        table1.add_row(row)
    print(table1)

    tmpl2 = '''
        SELECT *
          FROM Ads as a
         ORDER BY ad_id DESC
    '''
    cur.execute(tmpl2)
    rows = cur.fetchall()
    table2 = PrettyTable(['ad_id', 'duration', 'frequency', 'information', 'cost', 'sponsor_id'])
    for row in rows:
        table2.add_row(row)
    print(table2)




#-----------------------------------------------------------------
# get_all_ad_costs
#-----------------------------------------------------------------

def get_all_ad_costs_menu():
    heading('''
            get_all_ad_costs: this query will find all of the ads for sponsor_id 14, Wonderful Pistachios
    ''')
    
    sponsor_id = 14
    get_all_ad_costs(sponsor_id = sponsor_id)

def get_all_ad_costs(sponsor_id):
    tmpl = '''
        SELECT s.sponsor_id, s.sponsor_name, a.ad_id, a.duration, a.frequency, a.information, a.cost
          FROM Sponsors as s
          JOIN Ads as a 
               ON s.sponsor_id = a.sponsor_id
         WHERE (s.sponsor_id = %s)
    '''
    cmd = cur.mogrify(tmpl, (sponsor_id, ))
    print_cmd(cmd)
    cur.execute(cmd)

    rows = cur.fetchall()
    table = PrettyTable(['sponsor_id', 'sponsor_name', 'ad_id', 'duration','frequency', 'information', 'cost'])
    for row in rows:
        table.add_row(row)
    print(table)
    

    
# We leverage the fact that in Python functions are first class
# objects and build a dictionary of functions numerically indexed 

actions = { 1:list_sponsors_and_ads_menu,    2:get_all_ad_costs_menu }


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

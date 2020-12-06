-- Setup the database for a very simple 'social network'.
-- Friends - Users - Messages 

\c postgres
DROP DATABASE IF EXISTS socnet;

CREATE database socnet;
\c socnet

\i socnet_create.SQL

-- Users.csv
-- Friends.csv
-- Messages.csv

-- In this lab, as preparation for the project, you need to create the
-- three csv files Users.csv, Friends.csv and Messages.csv.  Create at
-- least 6 entries in each of these files.  
--
-- Look previous lab CSV files to guide your effort.

-- Modeling the structure of the 'Users' table,
-- read data from a csv file Users.csv
--
-- insert at least 6 users

\copy Users(first_name, last_name, email)     FROM 'Users.csv' csv header

-- Similarly load the table 'Friends'
-- 
-- In our model we view friendship is a symmetrical relationship.
-- Hence when ever (i,j) is inserted we also explicitly insert (j,i)
-- 
-- insert at least 6 friendship links

\copy Friends(uid_1, uid_2)     FROM 'Friends.csv' csv header

-- Create Messages.csv with at least 6 messages

\copy Messages(posted_by, posted_to, message)     FROM 'Messages.csv' csv header

-- ============================================================
  

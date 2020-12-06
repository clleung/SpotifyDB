-- Setup the database for a very simple 'social network'.
-- Friends - Users - Messages 

\c postgres
DROP DATABASE IF EXISTS socnet;

CREATE database socnet;
\c socnet

\i socnet_create.SQL

\copy Users(username, email, country, fname, lname, join_date, friend_username)     FROM 'Users.csv' csv header

-- ============================================================
  

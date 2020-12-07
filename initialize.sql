-- Setup the database for a very simple 'social network'.
-- Friends - Users - Messages 

\c postgres
DROP DATABASE IF EXISTS spotifydb;

CREATE database spotifydb;
\c spotifydb;

\i create.SQL

\copy Users(username, email, country, fname, lname, join_date, friend_username)     FROM 'Users.csv' csv header

-- ============================================================
  

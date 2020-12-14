-- Setup the database for a very simple 'social network'.
-- Friends - Users - Messages 

\c postgres
DROP DATABASE IF EXISTS spotifydb;

CREATE database spotifydb;
\c spotifydb;

\i create.SQL



\copy Users(username, email, country, fname, lname, join_date)     FROM 'Users.csv' csv header
\copy Artists(artist_id, artist_name, monthly_listeners)     FROM 'Artists.csv' csv header
\copy Sponsors(sponsor_id, sponsor_name)     FROM 'Sponsors.csv' csv header
\copy Songs(song_name, release_date, genre, duration, artist_id)     FROM 'Songs.csv' csv header

\copy Ads(duration, frequency, information, cost, sponsor_id)     FROM 'Ads.csv' csv header
\copy Artist_Ads(ad_id, artist_id, event_date)     FROM 'Artist_Ads.csv' csv header
\copy External_Ads(ad_id, client_name)     FROM 'External_Ads.csv' csv header
\copy Friends(uid1, uid2, simultaneous_play)     FROM 'Friends.csv' csv header
\copy Stream(uid, song_id, date, time)     FROM 'Stream.csv' csv header

-- ============================================================
  

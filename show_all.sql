\copy Users(username, email, country, fname, lname, join_date)     FROM 'Users.csv' csv header
\copy Artists(artist_id, artist_name, monthly_listeners)     FROM 'Artists.csv' csv header
\copy Sponsors(sponsor_id, sponsor_name)     FROM 'Sponsors.csv' csv header
\copy Songs(song_name, release_date, genre, num_plays, duration, artist_id)     FROM 'Songs.csv' csv header

\copy Ads(duration, frequency, information, cost, sponsor_id)     FROM 'Ads.csv' csv header
\copy Artist_Ads(ad_id, artist_id, event_date)     FROM 'Artist_Ads.csv' csv header
\copy External_Ads(ad_id, client_name)     FROM 'External_Ads.csv' csv header
\copy Friends(uid1, uid2, simultaneous_play)     FROM 'Friends.csv' csv header
\copy Stream(uid, song_id, date, time)     FROM 'Stream.csv' csv header

 \! echo "Ads Table, ordered by ad_id (ascending)";
SELECT *
  FROM Ads
 ORDER BY ad_id ASC;

 \! echo "Artist_Ads Table, ordered by ad_id (ascending)";
SELECT *
  FROM Artist_Ads
 ORDER BY ad_id ASC;

 \! echo "Artist Table, ordered by artist_id (ascending)";
SELECT *
  FROM Artists
 ORDER BY artist_id ASC;

 \! echo "External_Ads Table, ordered by ad_id (ascending)";
SELECT *
  FROM External_Ads
 ORDER BY ad_id ASC;

 \! echo "Friends Table, ordered by uid1 (ascending)";
SELECT *
  FROM Friends
 ORDER BY uid1 ASC;

 \! echo "Songs Table, ordered by song_id (ascending)";
SELECT *
  FROM Songs
 ORDER BY song_id ASC;

 \! echo "Sponsors Table, ordered by sponsor_id (ascending)";
SELECT *
  FROM Sponsors
 ORDER BY sponsor_id ASC;

 \! echo "Stream Table, ordered by stream_id (ascending)";
SELECT *
  FROM Stream
 ORDER BY stream_idASC;

 \! echo "User Table, ordered by uid";
SELECT *
  FROM Users
 ORDER BY uid ASC;


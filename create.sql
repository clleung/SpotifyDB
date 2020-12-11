-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2020-12-11 05:36:44.496
-- tables

DROP TABLE IF EXISTS Ads CASCADE;
DROP TABLE IF EXISTS Artist_Ads CASCADE;
DROP TABLE IF EXISTS Artists CASCADE;
DROP TABLE IF EXISTS External_Ads CASCADE;
DROP TABLE IF EXISTS Friends CASCADE;
DROP TABLE IF EXISTS Ranking CASCADE;
DROP TABLE IF EXISTS Songs CASCADE;
DROP TABLE IF EXISTS Sponsors CASCADE;
DROP TABLE IF EXISTS Stream CASCADE;
DROP TABLE IF EXISTS Users CASCADE;


-- Table: Ads
CREATE TABLE Ads (
    ad_id int  NOT NULL,
    duration time  NOT NULL,
    frequency int  NOT NULL,
    information text  NOT NULL,
    cost money  NOT NULL,
    sponsor_id int  NOT NULL,
    CONSTRAINT Ads_pk PRIMARY KEY (ad_id)
);

-- Table: Artist_Ads
CREATE TABLE Artist_Ads (
    ad_id int  NOT NULL,
    artist_name text  NOT NULL
);

-- Table: Artists
CREATE TABLE Artists (
    artist_id int  NOT NULL,
    artist_name text  NOT NULL,
    monthly_listeners int  NOT NULL,
    CONSTRAINT Artists_pk PRIMARY KEY (artist_id)
);

-- Table: External_Ads
CREATE TABLE External_Ads (
    ad_id int  NOT NULL,
    client_name text  NOT NULL
);

-- Table: Friends
CREATE TABLE Friends (
    uid1 int  NOT NULL,
    uid2 int  NOT NULL,
    simultaneous_play boolean  NOT NULL
);

-- Table: Ranking
CREATE TABLE Ranking (
    sponsor_id int  NOT NULL,
    ranking int  NOT NULL
);

-- Table: Songs
CREATE TABLE Songs (
    song_id int  NOT NULL,
    song_name text  NOT NULL,
    release_date date  NOT NULL,
    genre text  NOT NULL,
    num_plays int  NOT NULL,
    duration time  NOT NULL,
    artist_id int  NOT NULL,
    CONSTRAINT Songs_pk PRIMARY KEY (song_id)
);

-- Table: Sponsors
CREATE TABLE Sponsors (
    sponsor_id int  NOT NULL,
    sponsor_name text  NOT NULL,
    CONSTRAINT Sponsors_pk PRIMARY KEY (sponsor_id)
);

-- Table: Stream
CREATE TABLE Stream (
    uid int  NOT NULL,
    song_id int  NOT NULL,
    date date  NOT NULL,
    time time  NOT NULL
);

-- Table: Users
CREATE TABLE Users (
    uid int  NOT NULL,
    username text  NOT NULL,
    email text  NOT NULL,
    country text  NOT NULL,
    fname text  NOT NULL,
    lname text  NOT NULL,
    join_date date  NOT NULL,
    CONSTRAINT Users_pk PRIMARY KEY (uid)
);

-- foreign keys
-- Reference: Ads_Sponsors (table: Ads)
ALTER TABLE Ads ADD CONSTRAINT Ads_Sponsors
    FOREIGN KEY (sponsor_id)
    REFERENCES Sponsors (sponsor_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Artist_Ads_Ads (table: Artist_Ads)
ALTER TABLE Artist_Ads ADD CONSTRAINT Artist_Ads_Ads
    FOREIGN KEY (ad_id)
    REFERENCES Ads (ad_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Artists_Users (table: Artists)
ALTER TABLE Artists ADD CONSTRAINT Artists_Users
    FOREIGN KEY (artist_id)
    REFERENCES Users (uid)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: External_Ads_Ads (table: External_Ads)
ALTER TABLE External_Ads ADD CONSTRAINT External_Ads_Ads
    FOREIGN KEY (ad_id)
    REFERENCES Ads (ad_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Friends_users_1 (table: Friends)
ALTER TABLE Friends ADD CONSTRAINT Friends_users_1
    FOREIGN KEY (uid1)
    REFERENCES Users (uid)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Friends_users_2 (table: Friends)
ALTER TABLE Friends ADD CONSTRAINT Friends_users_2
    FOREIGN KEY (uid2)
    REFERENCES Users (uid)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Ranking_Sponsors (table: Ranking)
ALTER TABLE Ranking ADD CONSTRAINT Ranking_Sponsors
    FOREIGN KEY (sponsor_id)
    REFERENCES Sponsors (sponsor_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Songs_Artists (table: Songs)
ALTER TABLE Songs ADD CONSTRAINT Songs_Artists
    FOREIGN KEY (artist_id)
    REFERENCES Artists (artist_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Sponsors_Users (table: Sponsors)
ALTER TABLE Sponsors ADD CONSTRAINT Sponsors_Users
    FOREIGN KEY (sponsor_id)
    REFERENCES Users (uid)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Stream_Songs (table: Stream)
ALTER TABLE Stream ADD CONSTRAINT Stream_Songs
    FOREIGN KEY (song_id)
    REFERENCES Songs (song_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Stream_Users (table: Stream)
ALTER TABLE Stream ADD CONSTRAINT Stream_Users
    FOREIGN KEY (uid)
    REFERENCES Users (uid)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.
\copy Ads(ad_id, duration, frequency, information, cost, sponsor_id)     FROM 'Ads.csv' csv header
\copy Artist_Ads(ad_id, artist_name)     FROM 'Artist_Ads.csv' csv header
\copy Artists(artist_id, artist_name, monthly_listeners)     FROM 'Artists.csv' csv header
\copy External_Ads(ad_if, client_name)     FROM 'External_Ads.csv' csv header
\copy Friends(uid1, uid2, simultaneous_play)     FROM 'Friends.csv' csv header
\copy Ranking(sponsor_id, ranking)     FROM 'Ranking.csv' csv header
\copy Songs(song_id, song_name, release_date, genre, num_plays, duration, artist_id)     FROM 'Songs.csv' csv header
\copy Sponsors(sponsor_id, sponsor_name)     FROM 'Sponsors.csv' csv header
\copy Stream(uid, song_id, date, time)     FROM 'Stream.csv' csv header
\copy Users(uid, username, email, country, fname, lname, join_date)     FROM 'Users.csv' csv header
-- End of file.

--Use SERIAL to allocate ids
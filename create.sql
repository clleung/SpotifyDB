-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2020-10-07 23:02:25.274

CREATE TABLE Users (
    username text  NOT NULL,
    email text  NOT NULL,
    country text  NOT NULL,
    fname text  NOT NULL,
    lname text  NOT NULL,
    join_date date  NOT NULL,
    friend_username text  NOT NULL,
    CONSTRAINT Users_pk PRIMARY KEY (username,friend_username)
);


-- End of file.
--Hi I found this

-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2020-10-07 23:02:25.274

-- tables
-- Table: Friends
CREATE TABLE Friends (
    uid_1 int  NOT NULL,
    uid_2 int  NOT NULL,
    CONSTRAINT check_1 CHECK (uid_1 <> uid_2) NOT DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT Friends_pk PRIMARY KEY (uid_1,uid_2)
);

-- Table: Messages
CREATE TABLE Messages (
    mid serial  NOT NULL,
    posted_to int  NOT NULL,
    posted_by int  NOT NULL,
    message text  NOT NULL,
    time_stamp timestamp  NOT NULL DEFAULT LOCALTIMESTAMP(0),
    CONSTRAINT Messages_pk PRIMARY KEY (mid)
);

-- Table: Users 
CREATE TABLE Users  (
    uid serial  NOT NULL,
    first_name text  NOT NULL,
    last_name text  NOT NULL,
    email text  NOT NULL,
    CONSTRAINT Users_pk PRIMARY KEY (uid)
);

-- foreign keys
-- Reference: Friends_Users_1 (table: Friends)
ALTER TABLE Friends ADD CONSTRAINT Friends_Users_1
    FOREIGN KEY (uid_1)
    REFERENCES Users  (uid)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Friends_Users_2 (table: Friends)
ALTER TABLE Friends ADD CONSTRAINT Friends_Users_2
    FOREIGN KEY (uid_2)
    REFERENCES Users  (uid)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Messages_Users_posted_by (table: Messages)
ALTER TABLE Messages ADD CONSTRAINT Messages_Users_posted_by
    FOREIGN KEY (posted_by)
    REFERENCES Users  (uid)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Messages_Users_posted_to (table: Messages)
ALTER TABLE Messages ADD CONSTRAINT Messages_Users_posted_to
    FOREIGN KEY (posted_to)
    REFERENCES Users  (uid)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.
--Hi I found this

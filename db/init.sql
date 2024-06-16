DROP TABLE IF EXISTS users;

CREATE TABLE Users (
    id SERIAL, 
    email varchar(256) DEFAULT NULL,
    username varchar(45) DEFAULT NULL,
    first_name varchar(45) DEFAULT NULL,
    last_name varchar(45) DEFAULT NULL,
    hashed_password varchar(200) DEFAULT NULL,
    is_active BOOLEAN DEFAULT NULL,
    role varchar(45) DEFAULT NULL,
    PRIMARY KEY (id)
),
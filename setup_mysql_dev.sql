-- This script prepares a MySQL server for the project:


-- Creates a new database
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Creates a new user
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Gives the newly created user 'hbnb_dev' all privileges on the database hbnb_dev_db
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost' WITH GRANT OPTION;

-- Gives the newly created user 'hbnb_dev' SELECT privilege on the database performance_schema
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost' WITH GRANT OPTION;

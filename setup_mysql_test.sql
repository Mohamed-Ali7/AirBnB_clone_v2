-- This script prepares a MySQL server for the project

-- Create a new database
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create a new user
CREATE USER IF NOT EXISTS 'hbnb_test '@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Gives the newly created user 'hbnb_test' all privileges on the database hbnb_test_db
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost' WITH GRANT OPTION;

-- Gives the newly created user 'hbnb_dev' SELECT privilege on the database performance_schema
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost' WITH GRANT OPTION;

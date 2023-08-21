CREATE DATABASE IF NOT EXISTS meteo;
USE meteo;

CREATE TABLE IF NOT EXISTS users (email varchar(255) NOT NULL PRIMARY KEY, password varchar(255) NOT NULL);
CREATE TABLE IF NOT EXISTS results_requests (user_email varchar(255) NOT NULL, request varchar(255) NOT NULL, result varchar(255) NOT NULL, FOREIGN KEY (user_email) REFERENCES users (email));

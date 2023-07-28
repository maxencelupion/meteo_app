import mysql.connector
import os
from dotenv import load_dotenv
import bcrypt


def connect_to_db():
    load_dotenv()
    my_db = mysql.connector.connect(
        host=os.getenv("host"),
        user=os.getenv("user"),
        password=os.getenv("password"),
    )
    return my_db


def create_db():
    my_db = connect_to_db()
    my_cursor = my_db.cursor()
    my_cursor.execute("CREATE DATABASE IF NOT EXISTS meteo")


def create_tables():
    my_db = connect_to_db()
    my_cursor = my_db.cursor()
    my_cursor.execute("USE meteo;")
    my_cursor.execute("CREATE TABLE IF NOT EXISTS users (email varchar(255) NOT NULL PRIMARY KEY, password varchar(255) NOT NULL);")
    my_cursor.execute("CREATE TABLE IF NOT EXISTS results_requests (user_email varchar(255) NOT NULL, request varchar(255) NOT NULL, result varchar(255) NOT NULL, FOREIGN KEY (user_email) REFERENCES users (email));")


def init_db():
    create_db()
    create_tables()
    return connect_to_db()


def add_to_db(email, hashed_password):
    error_message = None
    my_db = init_db()
    my_cursor = my_db.cursor()
    try:
        my_cursor.execute("USE meteo;")
        my_cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s);", (email, hashed_password))
        my_db.commit()
        my_cursor.close()
        my_db.close()
    except Exception as e:
        my_cursor.close()
        my_db.close()
        if "Duplicate entry" in str(e):
            error_message = "Cet email est déjà utilisé."
        else:
            error_message = "Erreur lors de la création du compte."
    return error_message


def log_user(email, password):
    error_message = None
    my_db = init_db()
    my_cursor = my_db.cursor()
    try:
        my_cursor.execute("USE meteo;")
        my_cursor.execute("SELECT password FROM users WHERE email=%s;", (email,))
        row = my_cursor.fetchone()
        my_cursor.close()
        my_db.close()
        if row is not None and bcrypt.checkpw(password.encode('utf-8'), row[0].encode('utf-8')):
            return error_message
        else:
            error_message = "Mauvais email ou mot de passe."
            return error_message
    except Exception:
        error_message = "Erreur lors de la connexion."
        return error_message


def add_to_history(email, city, result):
    error_message = None
    my_db = init_db()
    my_cursor = my_db.cursor()
    try:
        my_cursor.execute("USE meteo;")
        my_cursor.execute("INSERT INTO results_requests (user_email, request, result) VALUES (%s, %s, %s);", (email, city, result))
        my_db.commit()
        my_cursor.close()
        my_db.close()
    except Exception as e:
        my_cursor.close()
        my_db.close()
        if "Duplicate entry" in str(e):
            error_message = "Cet email est déjà utilisé."
        else:
            error_message = "Erreur lors de la création du compte."
    return error_message


def show_history(email):
    error_message = None
    my_db = init_db()
    my_cursor = my_db.cursor()
    try:
        my_cursor.execute("USE meteo;")
        my_cursor.execute("SELECT * FROM results_requests WHERE user_email=%s;", (email,))
        row = my_cursor.fetchall()
        my_cursor.close()
        my_db.close()
        if row is not None:
            return row
    except Exception:
        error_message = "Erreur lors de la requête."
        return error_message

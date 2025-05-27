import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="kavin@123",  # replace with your MySQL password
        database="hospital_db"       # ensure this database exists
    )

import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  
        port=3306,       
        password="Ravi@9532",
        database="expense_manager"
    )

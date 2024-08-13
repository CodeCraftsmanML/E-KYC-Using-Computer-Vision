import mysql.connector
import pandas as pd
import logging

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ekyc"
)
mycursor = mydb.cursor()
print("Connection Established")


def insert_records(text_info):
    """
    I insert a new record into the `user_info` table in the database.
    I use the `INSERT INTO` SQL statement to add a record with `id`, `name`, and `id_type` fields.
    I pass the values from the `text_info` dictionary into the SQL query.
    After executing the query, I commit the transaction to save the changes.
    I log a message indicating that the record for the specified ID has been inserted successfully.
    """    

    sql = """
    INSERT INTO user_info(id, name, id_type) 
    VALUES (%s, %s, %s)
    """
    value = (
        text_info['ID'],
        text_info['Name'],
        text_info['ID Type']
    )
    mycursor.execute(sql, value)
    mydb.commit()
    logging.info(f"Record for {text_info['ID']} inserted successfully")


def fetch_records(text_info):
    """
    I retrieve records from the `user_info` table based on the provided `id`.
    I use the `SELECT * FROM` SQL statement with a `WHERE` clause to filter records by `id`.
    I execute the query and fetch all results into a DataFrame.
    If records are found, I log a success message and return the DataFrame.
    If no records are found, I log a message indicating this and return an empty DataFrame.
    """
    
    sql = "SELECT * FROM user_info WHERE id = %s"
    value = (text_info['ID'],)
    mycursor.execute(sql, value)
    result = mycursor.fetchall()

    if result:
        df = pd.DataFrame(result, columns=[desc[0] for desc in mycursor.description])
        logging.info(f"Record for {text_info['ID']} fetched successfully")
        return df
    else:
        logging.info(f"No record found for {text_info['ID']}")
        return pd.DataFrame()
    

def check_duplicacy(text_info):
    """
    I check if there is a duplicate record in the `user_info` table for the given `id`.
    I first call the `fetch_records` function to get records for the specified ID.
    If any records are found (i.e., the DataFrame has more than 0 rows), I set `is_duplicate` to True and log a message indicating a duplicate record.
    If no records are found, I log a message indicating no duplicates.
    I return the boolean value `is_duplicate` to indicate whether a duplicate record was found.
    """ 
    
    is_duplicate = False
    df = fetch_records(text_info)
    if df.shape[0] > 0:
        is_duplicate = True
        logging.info(f"Duplicate record found for {text_info['ID']}")
    else:
        logging.info(f"No duplicate record found for {text_info['ID']}")
    return is_duplicate


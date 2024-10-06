import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="19112005"
    )

    cursor = conn.cursor()

    # Check if the database exists by attempting to use it
    try:
        cursor.execute("USE jwst_exploration")
        print("Database exists.")
    except mysql.connector.Error as err:
        if err.errno == 1049:  # Database does not exist error
            print("Database does not exist.")
        else:
            print("Error:", err)

finally:
    if conn:
        conn.close()
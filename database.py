import mysql.connector
from mysql.connector import Error
# Function to establish the database connection
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='19112005',
        database='jwst_exploration'  # Ensure this is your correct database
    )
# Function to initialize the database and create the media table
def initialize_database():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='19112005'
        )
        cursor = conn.cursor()

        # Create database if it does not exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS jwst_exploration")
        conn.database = 'jwst_exploration'

        # Create table if it does not exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS media (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_path VARCHAR(256) NOT NULL,
                category VARCHAR(64) NOT NULL,
                media_type ENUM('image', 'audio') NOT NULL  -- Added ENUM to clarify the media type
            )
        ''')

        conn.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# Function to fetch media (images or music) by category
def fetch_media_by_category(category, media_type=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    # If media_type is provided, filter by both category and media_type (e.g., only fetch images or only audio)
    if media_type:
        cursor.execute("SELECT file_path FROM media WHERE category=%s AND media_type=%s", (category, media_type))
    else:
        # If no media_type is provided, fetch all media (both images and audio) in that category
        cursor.execute("SELECT file_path, media_type FROM media WHERE category=%s", (category,))

    media_files = cursor.fetchall()
    cursor.close()
    conn.close()

    return media_files


# Function to add media (image or music) into the database
def add_media(file_path, category, media_type):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO media (file_path, category, media_type) VALUES (%s, %s, %s)",
        (file_path, category, media_type)
    )

    conn.commit()
    cursor.close()
    conn.close()


# Function to add all media from directories
def add_media_from_directory(directory, category, media_type):
    import os

    # Loop through each file in the directory and insert into the database
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if media_type == 'image' and filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            add_media(file_path, category, media_type)
        elif media_type == 'audio' and filename.lower().endswith(('.mp3', '.wav')):
            add_media(file_path, category, media_type)
        else:
            print(f"Skipping {file_path}, unsupported file type.")


# Initialize the database
initialize_database()

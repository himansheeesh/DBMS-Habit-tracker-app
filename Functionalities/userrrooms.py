import mysql.connector
from datetime import date

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'jebasither',
    'database': 'habit_tracker_app'
}

# Function to establish a database connection
def connect_to_database():
    return mysql.connector.connect(**db_config)

# Function to add a user to a room
def add_user_to_room(user_id, room_id):
    connection = connect_to_database()
    cursor = connection.cursor()

    query = """
    INSERT INTO userrooms (UserID, RoomID)
    VALUES (%s, %s)
    """

    values = (user_id, room_id)

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()

# Function to get all users in a room
def get_users_in_room(room_id):
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT u.* FROM users u
    JOIN userrooms ur ON u.UserID = ur.UserID
    WHERE ur.RoomID = %s
    """

    cursor.execute(query, (room_id,))
    users = cursor.fetchall()


    cursor.close()
    connection.close()

    return users

# Function to remove a user from a room
def remove_user_from_room(user_id, room_id):
    connection = connect_to_database()
    cursor = connection.cursor()

    query = """
    DELETE FROM userrooms
    WHERE UserID = %s AND RoomID = %s
    """

    values = (user_id, room_id)

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()
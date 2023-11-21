import mysql.connector
from datetime import date

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'jebasither',
    'database': 'habit_tracker_app'
}

# Function to establish a database connection
def connect_to_database():
    return mysql.connector.connect(**db_config)

# Function to create a new room
def create_room(name, user_id):
    connection = connect_to_database()
    cursor = connection.cursor()

    query = """
    INSERT INTO rooms (Name, CreatedAt, UpdatedAt)
    VALUES (%s, %s, %s)
    """

    current_date = date.today()
    values = (name, current_date, current_date)

    cursor.execute(query, values)
    connection.commit()

    room_id = cursor.lastrowid

    # Add the user to the room in the userrooms table
    cursor.execute("INSERT INTO userrooms (UserID, RoomID) VALUES (%s, %s)", (user_id, room_id))
    connection.commit()

    cursor.close()
    connection.close()

    return room_id

# Function to retrieve all rooms for a user
def get_user_rooms(user_id):
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT r.* FROM rooms r
    JOIN userrooms ur ON r.RoomID = ur.RoomID
    WHERE ur.UserID = %s
    """

    cursor.execute(query, (user_id,))
    rooms = cursor.fetchall()

    cursor.close()
    connection.close()

    return rooms

# Function to update a room
def update_room(room_id, name):
    connection = connect_to_database()
    cursor = connection.cursor()

    query = """
    UPDATE rooms
    SET Name = %s, UpdatedAt = %s
    WHERE RoomID = %s
    """

    current_date = date.today()
    values = (name, current_date, room_id)

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()

# Function to delete a room
def delete_room(room_id):
    connection = connect_to_database()
    cursor = connection.cursor()

    # Check for foreign key relations in userrooms table
    cursor.execute("SELECT * FROM userrooms WHERE RoomID = %s", (room_id,))
    userroom_records = cursor.fetchall()

    if userroom_records:
        # If users are associated with the room, you may choose to handle this scenario based on your application logic.
        # For example, you might want to remove the association or prevent the deletion.
        print("Cannot delete the room. Users are associated with the room.")
    else:
        # No users associated, proceed with room deletion
        cursor.execute("DELETE FROM rooms WHERE RoomID = %s", (room_id,))
        connection.commit()

    cursor.close()
    connection.close()

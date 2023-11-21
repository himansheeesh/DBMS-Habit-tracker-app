import mysql.connector
from datetime import *

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

def create_reminder(habit_id, time_period, time_length, time_unit):
    connection = connect_to_database()
    cursor = connection.cursor()
    created_at = datetime.now().date()

    query = """
    INSERT INTO reminders (HabitID, TimePeriod, TimeLength, TimeUnit, CreatedAt)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (habit_id, time_period, time_length, time_unit, created_at)

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()

# Function to retrieve all reminders for a user
def get_user_reminders(user_id):
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT * FROM reminders r
    JOIN habits h ON r.HabitID = h.HabitID
    WHERE h.UserID = %s
    """

    cursor.execute(query, (user_id,))
    reminders = cursor.fetchall()

    cursor.close()
    connection.close()

    return reminders

# Function to update a reminder
def update_reminder(reminder_id, time_length, time_unit):
    connection = connect_to_database()
    cursor = connection.cursor()


    query = """
    UPDATE reminders
    SET TimeLength = %s, TimeUnit = %s
    WHERE HabitID = %s
    """

    values = (time_length, time_unit, reminder_id)

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()

# Function to delete a reminder
def delete_reminder(reminder_id):
    connection = connect_to_database()
    cursor = connection.cursor()

    query = """
    DELETE FROM reminders
    WHERE HabitID = %s
    """

    cursor.execute(query, (reminder_id,))
    connection.commit()

    cursor.close()
    connection.close()

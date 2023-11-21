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

# Function to insert a new habit
def create_habit(title, description, user_id):
    connection = connect_to_database()
    cursor = connection.cursor()

    query = """
    INSERT INTO habits (Title, Description, CreatedAt, UpdatedAt, Streak, MaxStreak, UserID)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    current_date = date.today()
    values = (title, description, current_date, current_date, 0, 0, user_id)

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()

# Function to retrieve all habits for a user
def get_user_habits(user_id):
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT * FROM habits WHERE UserID = %s
    """

    cursor.execute(query, (user_id,))
    habits = cursor.fetchall()

    cursor.close()
    connection.close()

    return habits

# Function to update a habit
def update_habit(habit_id, title, description):
    connection = connect_to_database()
    cursor = connection.cursor()

    query = """
    UPDATE habits
    SET Title = %s, Description = %s, UpdatedAt = %s
    WHERE HabitID = %s
    """

    current_date = date.today()
    values = (title, description, current_date, habit_id)

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()

# Function to delete a habit
def delete_habit(habit_id):
    connection = connect_to_database()
    cursor = connection.cursor()

        # Delete related goals first
    cursor.execute("DELETE FROM goals WHERE HabitID = %s", (habit_id,))
        # Delete related reminders
    cursor.execute("DELETE FROM reminders WHERE HabitID = %s", (habit_id,))
        # Now delete the habit
    cursor.execute("DELETE FROM habits WHERE HabitID = %s", (habit_id,))
    connection.commit()

    cursor.close()
    connection.close()

# Function to calculate completion percentage
def calculate_completion_percentage(habit_id):
    connection = connect_to_database()
    cursor = connection.cursor()

    try:
        # Execute the function using a SELECT statement
        cursor.execute("SELECT CalculateCompletionPercentage(%s);", (habit_id,))

        # Fetch the result
        result = cursor.fetchone()[0]


    except Exception as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
        connection.close()
        return result

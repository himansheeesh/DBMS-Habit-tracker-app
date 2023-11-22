import mysql.connector
from datetime import date
from dotenv import load_dotenv
import os

load_dotenv()

db_config = {
    "host": os.getenv("host"),
    "user": os.getenv("user"),
    "password": os.getenv("password"),
    "database": os.getenv("database"),
}

# Function to establish a database connection
def connect_to_database():
    return mysql.connector.connect(**db_config)

def create_goal(title, description, counter, target, habit_id):
    connection = connect_to_database()
    cursor = connection.cursor()

    query = """
    INSERT INTO goals (Title, Description, CreatedAt, UpdatedAt, Counter, Target, Completed, HabitID)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    current_date = date.today()
    values = (title, description, current_date, current_date, counter, target, 0, habit_id)

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()

# Function to retrieve all goals for a specified user
def get_user_goals(habit_id):
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT * FROM goals WHERE HabitID = %s
    """

    cursor.execute(query, (habit_id,))
    goals = cursor.fetchall()

    cursor.close()
    connection.close()

    return goals

# Function to update a goal
def update_goal(goal_id, title, description, counter, target):
    connection = connect_to_database()
    cursor = connection.cursor()

    query = """
    UPDATE goals
    SET Title = %s, Description = %s, UpdatedAt = %s, Counter = %s, Target = %s
    WHERE GoalID = %s
    """

    current_date = date.today()
    values = (title, description, current_date, counter, target, goal_id)

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()

# Function to delete a goal
def delete_goal(goal_id):
    connection = connect_to_database()
    cursor = connection.cursor()

    query = """
    DELETE FROM goals
    WHERE GoalID = %s
    """

    cursor.execute(query, (goal_id,))
    connection.commit()

    cursor.close()
    connection.close()
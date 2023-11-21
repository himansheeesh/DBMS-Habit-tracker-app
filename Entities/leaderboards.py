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

# Function to get the leaderboard for a room
def get_room_leaderboard(room_id):
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)

    # Example: Get users in the room with their achievements
    query = """
    SELECT
        u.*,
        (
            SELECT COUNT(*)
            FROM goals g
            JOIN habits h ON g.HabitID = h.HabitID
            JOIN userrooms ur ON h.UserID = ur.UserID
            WHERE g.Completed = 1 AND ur.RoomID = %s AND ur.UserID = u.UserID
        ) as Achievements
    FROM users u
    JOIN userrooms ur ON u.UserID = ur.UserID
    WHERE ur.RoomID = %s
    ORDER BY Achievements DESC
    """

    cursor.execute(query, (room_id, room_id))
    leaderboard = cursor.fetchall()

    cursor.close()
    connection.close()

    return leaderboard

# Function to get the overall leaderboard across all rooms
def get_overall_leaderboard():
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)

    # Example: Get users with their total achievements across all rooms
    query = """
    SELECT
        u.*,
        (
            SELECT COUNT(*)
            FROM goals g
            JOIN habits h ON g.HabitID = h.HabitID
            JOIN userrooms ur ON h.UserID = ur.UserID
            WHERE g.Completed = 1 AND ur.UserID = u.UserID
        ) as TotalAchievements
    FROM users u
    ORDER BY TotalAchievements DESC
    """

    cursor.execute(query)
    overall_leaderboard = cursor.fetchall()

    cursor.close()
    connection.close()

    return overall_leaderboard

# Example: Function to get the top achiever in each room
def get_top_achiever_in_each_room():
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)

    # Example: Get the user with the highest achievements in each room
    query = """
    SELECT
    u.*,
    Achievements.Achievements
FROM users u
JOIN userrooms ur ON u.UserID = ur.UserID
JOIN (
    SELECT ur.RoomID, ur.UserID, COUNT(*) as Achievements
    FROM goals g
    JOIN habits h ON g.HabitID = h.HabitID
    JOIN userrooms ur ON h.UserID = ur.UserID
    WHERE g.Completed = 1
    GROUP BY ur.RoomID, ur.UserID
) Achievements ON ur.RoomID = Achievements.RoomID AND ur.UserID = Achievements.UserID
JOIN (
    SELECT RoomID, MAX(Achievements) as MaxAchievements
    FROM (
        SELECT ur.RoomID, ur.UserID, COUNT(*) as Achievements
        FROM goals g
        JOIN habits h ON g.HabitID = h.HabitID
        JOIN userrooms ur ON h.UserID = ur.UserID
        WHERE g.Completed = 1
        GROUP BY ur.RoomID, ur.UserID
    ) user_achievements
    GROUP BY RoomID
) max_achiever ON ur.RoomID = max_achiever.RoomID AND Achievements.Achievements = max_achiever.MaxAchievements;

    """

    cursor.execute(query)
    top_achievers = cursor.fetchall()

    cursor.close()
    connection.close()

    return top_achievers

# Additional complex queries can be added as needed.

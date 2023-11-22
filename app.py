import streamlit as st
import mysql.connector
from datetime import *
from Entities.habits import *
from Entities.goals import *
from Entities.leaderboards import *
from Entities.reminders import *
from Entities.rooms import *
from Entities.userrrooms import *

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'habit_tracker_app'
}

# Function to establish a database connection
def connect_to_database():
    return mysql.connector.connect(**db_config)

def check_credentials(email, password):
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM users WHERE Email = %s AND Password = %s"
    cursor.execute(query, (email, password))
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    return user

def get_session_state():
    session_state = st.session_state
    if not hasattr(session_state, "initialized"):
        session_state.initialized = True
        session_state.user_id = None
    return session_state

session_state = get_session_state()

def get_user_id(email):
    connection = connect_to_database()
    cursor = connection.cursor()

    query = "SELECT UserID FROM users WHERE Email = %s"
    cursor.execute(query, (email,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result:
        return result[0]
    else:
        return None


def get_user_ids():
    connection = connect_to_database()
    cursor = connection.cursor()

    query = "SELECT UserID FROM users"
    cursor.execute(query)
    user_ids = [user[0] for user in cursor.fetchall()]

    cursor.close()
    connection.close()

    return user_ids

def create_user(name, email, password):
    connection = connect_to_database()
    cursor = connection.cursor()

    if not check_credentials(email, password):
        query = """
        INSERT INTO users (Name, Email, Password, CreatedAt,UpdatedAt)
        VALUES (%s, %s, %s, %s,%s)
        """

        current_date = datetime.now().date()
        values = (name, email, password, current_date,current_date)

        cursor.execute(query, values)
        connection.commit()

        st.success("User created successfully.")
    else:
        # If the user already exists, return an error message
        st.error("User with this email already exists.")

    cursor.close()
    connection.close()


st.title("Habit Tracker App")
logged_in = False


def login():
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = check_credentials(email, password)
        if user:
            session_state.user_id = user["UserID"]
            st.success("Login Successful!")
            st.rerun()

def register():
    st.subheader("Register")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        # Check if the user already exists
        if not check_credentials(email,password):
            create_user(name, email, password)
            st.success("Registration Successful! Please log in.")
        else:
            st.error("User already exists. Please log in.")

selected_user_id = session_state.user_id

if selected_user_id is None:
    st.write("User not logged in.")
    login_email = st.text_input("Email:")
    login_password = st.text_input("Password:", type="password")
    if st.button("Login"):
        if check_credentials(login_email, login_password):
            user_id = get_user_id(login_email)
            st.session_state.user_id = user_id
        else:
            st.error("Invalid credentials. Please try again.")
    
    st.subheader("Sign Up")
    signup_name = st.text_input("Name:", key="signup_name")
    signup_email = st.text_input("Email:", key="signup_email")
    signup_password = st.text_input("Password:", type="password", key="signup_password")

    if st.button("Sign Up"):
        if not check_credentials(signup_email, signup_password):
            create_user(signup_name, signup_email, signup_password)
            st.success("Registration Successful! Please log in.")
            # Automatically fill in the login fields after successful signup
            login_email = signup_email
            login_password = signup_password
            st.session_state.user_id = get_user_id(login_email)
        else:
            st.error("User already exists. Please log in.")

else:
    st.write(f"Welcome, User {st.session_state.user_id}")
    logout_button = st.sidebar.button("Logout")
    if logout_button:
        st.session_state.user_id = None
        logged_in = False
        st.rerun()

all_user_ids = get_user_ids()

if selected_user_id:
    logged_in = True



if logged_in:
    selected_option = st.sidebar.radio("Select Option", ["Habits","Goals","Rooms","Reminders","Leaderboards"])  

    
    if selected_option == "Habits":
        st.header("Create, Read, Update, or Delete Habit")
        selected_operation = st.radio("Choose Operation", ["Create", "Read", "Update", "Delete", "Calculate Percentage"])
        user_habits = get_user_habits(selected_user_id)

        if selected_operation == "Read":
            st.header("Your Habits")
            for habit in user_habits:
                st.write(f"**{habit['Title']}** - {habit['Description']}")

        if selected_operation == "Create":
            habit_title = st.text_input("Title")
            habit_description = st.text_area("Description") 
            if st.button("Create Habit"):
                create_habit(habit_title, habit_description, selected_user_id)
                
        elif selected_operation == "Update":
            habit_title = st.text_input("Title")
            habit_description = st.text_area("Description")
            selected_habit_id = st.selectbox("Select Habit to Update", [habit['HabitID'] for habit in get_user_habits(selected_user_id)])
            if st.button("Update Habit"):
                update_habit(selected_habit_id, habit_title, habit_description)

        elif selected_operation == "Delete":
            selected_habit_id = st.selectbox("Select Habit to Delete", [habit['HabitID'] for habit in get_user_habits(selected_user_id)])
            if st.button("Delete Habit"):
                delete_habit(selected_habit_id)
        
        elif selected_operation == "Calculate Percentage":
            selected_habit_id = st.selectbox("Select Habit to Calculate Completion Percentage", [habit['HabitID'] for habit in get_user_habits(selected_user_id)])
            if st.button("Calculate Percentage"):
                result = calculate_completion_percentage(selected_habit_id)
                st.write(result)


    if selected_option == 'Goals':
        st.header("Create, Read, Update, or Delete Goals")

        selected_operation = st.radio("Choose Operation", ["Create", "Read", "Update", "Delete"])
        habit_id = st.selectbox("Select Habit", [habit['HabitID'] for habit in get_user_habits(selected_user_id)])
        user_goals = get_user_goals(habit_id)

        # Create Goal Section
        if selected_operation == 'Create':
            st.subheader("Create Goal")
            goal_title = st.text_input("Title")
            goal_description = st.text_area("Description")
            goal_counter = st.number_input("Counter", min_value=0)
            goal_target = st.number_input("Target", min_value=0)
            
            if st.button("Create Goal"):
                create_goal(goal_title, goal_description, goal_counter, goal_target, habit_id)

        if selected_operation == "Read":
            st.subheader("Your Goals")
            for goal in user_goals:
                st.write(f"**{goal['Title']}** - {goal['Description']} - Counter: {goal['Counter']} - Target: {goal['Target']}")

        if selected_operation == "Update":
            st.subheader("Update Goal")
            selected_goal_id = st.selectbox("Select Goal to Update", [goal['GoalID'] for goal in user_goals])
            if selected_goal_id:
                updated_goal_title = st.text_input("Updated Title")
                updated_goal_description = st.text_area("Updated Description")
                updated_goal_counter = st.number_input("Updated Counter", min_value=0)
                updated_goal_target = st.number_input("Updated Target", min_value=0)

                if st.button("Update Goal"):
                    update_goal(selected_goal_id, updated_goal_title, updated_goal_description, updated_goal_counter, updated_goal_target)

        if selected_operation == "Delete":
            st.subheader("Delete Goal")
            selected_goal_id_delete = st.selectbox("Select Goal to Delete", [goal['GoalID'] for goal in user_goals])
            if selected_goal_id_delete:
                if st.button("Delete Goal"):
                    delete_goal(selected_goal_id_delete)


    if selected_option == 'Rooms':
        selected_option = st.radio("Select Room Function", ["Create", "Read", "Update", "Delete", "Add User", "Remove User","View Users"])
        user_rooms = get_user_rooms(selected_user_id)
        # Main content based on user's choice

        if selected_option == "Create":
            st.header("Create Room")
            room_name = st.text_input("Room Name")
            if st.button("Create Room"):
                created_room_id = create_room(room_name, selected_user_id)
                st.success(f"Room '{room_name}' created with ID: {created_room_id}")

        elif selected_option == "Read":
            st.header("Read Rooms")
            for room in user_rooms:
                st.write(f"Room ID: {room['RoomID']}, Name: {room['Name']}")

        elif selected_option == "Update":
            st.header("Update Room")
            selected_room_id = st.selectbox("Select Room to Update", [room['RoomID'] for room in user_rooms])
            if selected_room_id:
                updated_room_name = st.text_input("Updated Room Name")
                if st.button("Update Room"):
                    update_room(selected_room_id, updated_room_name)
                    st.success(f"Room with ID {selected_room_id} updated")

        elif selected_option == "Delete":
            st.header("Delete Room")
            selected_room_id_delete = st.selectbox("Select Room to Delete", [room['RoomID'] for room in user_rooms])
            if selected_room_id_delete:
                if st.button("Delete Room"):
                    delete_room(selected_room_id_delete)
                    st.success(f"Room with ID {selected_room_id_delete} deleted")
        
        elif selected_option == "Add User":
            st.header("Add User to Room")
            selected_room_id_add_user = st.selectbox("Select Room to Add User", [room['RoomID'] for room in user_rooms])
            user_ids = get_user_ids()
            if selected_room_id_add_user:
                user_to_add = st.selectbox("Select User to Add", user_ids)  
                if st.button("Add User to Room"):
                    add_user_to_room(user_to_add, selected_room_id_add_user)
                    st.success(f"User {user_to_add} added to Room {selected_room_id_add_user}")

        elif selected_option == "Remove User":
            st.header("Remove User from Room")
            selected_room_id_remove_user = st.selectbox("Select Room to Remove User", [room['RoomID'] for room in user_rooms])
            if selected_room_id_remove_user:
                users_in_room = get_users_in_room(selected_room_id_remove_user)
                users_in_room = [user['Name'] for user in users_in_room]
                user_to_remove = st.selectbox("Select User to Remove",users_in_room)
                if st.button("Remove User from Room"):
                    remove_user_from_room(user_to_remove['UserID'], selected_room_id_remove_user)
                    st.success(f"User {user_to_remove['UserID']} removed from Room {selected_room_id_remove_user}")
        
        elif selected_option == "View Users":
            st.header("View Users in Room")
            selected_room_id_view_users = st.selectbox("Select Room to View Users", [room['RoomID'] for room in user_rooms])
            if selected_room_id_view_users:
                users_in_room = get_users_in_room(selected_room_id_view_users)
                for user in users_in_room:
                    st.write(f"User {user['UserID']} in Room {selected_room_id_view_users}")


    if selected_option == 'Reminders':
        st.header("Create, Read, Update, or Delete Reminders")
        selected_option = st.radio("Select Reminder Function", ["Create", "Read", "Update", "Delete"])
        user_reminders = get_user_reminders(selected_user_id)
        user_habits = get_user_habits(selected_user_id)
        user_habits = [habit['HabitID'] for habit in user_habits]


        if selected_option == "Create":
            st.header("Create Reminder")
            habit_id = st.selectbox("Select Habit",user_habits) 
            time_period = st.date_input("Reminder Date")
            time_length = st.number_input("Time Length", min_value=1)
            time_unit = st.selectbox("Time Unit", ["minutes", "hours", "days"])
            if st.button("Create Reminder"):
                create_reminder(habit_id, time_period, time_length, time_unit)
                st.success("Reminder created successfully")

        elif selected_option == "Read":
            st.header("Read Reminders")
            for reminder in user_reminders:
                st.write(f"Reminder for Habit {reminder['HabitID']} on {reminder['TimePeriod']}, Length: {reminder['TimeLength']} {reminder['TimeUnit']}")

        elif selected_option == "Update":
            st.header("Update Reminder")
            selected_reminder_id = st.selectbox("Select Habit Reminder to Update", [reminder['HabitID'] for reminder in user_reminders])
            if selected_reminder_id:
                updated_time_length = st.number_input("Updated Time Length", min_value=1)
                updated_time_unit = st.selectbox("Updated Time Unit", ["minutes", "hours", "days"])
                if st.button("Update Reminder"):
                    update_reminder(selected_reminder_id, updated_time_length, updated_time_unit)
                    st.success(f"Reminder on {selected_reminder_id} updated")

        elif selected_option == "Delete":
            st.header("Delete Reminder")
            selected_reminder_id_delete = st.selectbox("Select Habit Reminder to Delete", [reminder['HabitID'] for reminder in user_reminders])
            if selected_reminder_id_delete:
                if st.button("Delete Reminder"):
                    delete_reminder(selected_reminder_id_delete)
                    st.success(f"Reminder on {selected_reminder_id_delete} deleted")
    

    if selected_option == 'Leaderboards':
        selected_option = st.radio("Select Leaderboard Function", ["Room Leaderboard", "Overall Leaderboard", "Top Achiever in Each Room"])
        user_rooms = get_user_rooms(selected_user_id)
        user_rooms = [room['RoomID'] for room in user_rooms]

        if selected_option == "Room Leaderboard":
            st.header("Room Leaderboard")
            selected_room_id = st.selectbox("Select Room", user_rooms)  # Replace with your actual room IDs
            room_leaderboard = get_room_leaderboard(selected_room_id)

            for i, user in enumerate(room_leaderboard, start=1):
                st.write(f"{i}. User {user['UserID']} - Achievements: {user['Achievements']}")

        elif selected_option == "Overall Leaderboard":
            st.header("Overall Leaderboard")
            overall_leaderboard = get_overall_leaderboard()

            for i, user in enumerate(overall_leaderboard, start=1):
                st.write(f"{i}. User {user['UserID']} - Total Achievements: {user['TotalAchievements']}")

        elif selected_option == "Top Achiever in Each Room":
            st.header("Top Achiever in Each Room")
            top_achievers = get_top_achiever_in_each_room()

            for i, user in enumerate(top_achievers, start=1):
                st.write(f"{i}. User {user['UserID']} - Achievements: {user['Achievements']}")


            
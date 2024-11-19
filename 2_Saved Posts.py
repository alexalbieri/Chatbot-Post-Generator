import sqlite3
import streamlit as st
from datetime import datetime

st.title("Saved Posts")
st.write("Here are your Saved Posts!")

# Database setup functions
def initialize_database():
    try:
        conn = sqlite3.connect("posts.db")
        cursor = conn.cursor()

        # Create a new table 'posts_new' with a correct 'created_at' column and move data
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts_new (
            id INTEGER PRIMARY KEY,
            content TEXT,
            created_at TEXT NOT NULL DEFAULT (DATETIME('now'))
        )
        """)

        # Migrate data from old 'posts' table to 'posts_new' table if it exists
        cursor.execute("PRAGMA table_info(posts)")
        columns = [info[1] for info in cursor.fetchall()]
        if 'created_at' in columns:
            cursor.execute("INSERT INTO posts_new (id, content, created_at) SELECT id, content, COALESCE(created_at, DATETIME('now')) FROM posts")
        else:
            cursor.execute("INSERT INTO posts_new (id, content, created_at) SELECT id, content, DATETIME('now') FROM posts")

        # Replace old 'posts' table with the new one
        cursor.execute("DROP TABLE IF EXISTS posts")
        cursor.execute("ALTER TABLE posts_new RENAME TO posts")

        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        st.error(f"Database initialization failed: {e}")

# Function to get database connection
def get_connection():
    try:
        conn = sqlite3.connect("posts.db")
        return conn
    except sqlite3.Error as e:
        st.error(f"Database connection failed: {e}")
        return None

# Function to save a post to the database
def save_post(content):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO posts (content, created_at) VALUES (?, ?)", (content, created_at))
        conn.commit()
        conn.close()

# Function to get saved posts from the database
def get_saved_posts():
    conn = get_connection()
    if conn is None:
        return []  # Return empty list if connection fails

    cursor = conn.cursor()
    # Use datetime() to ensure proper ordering
    cursor.execute("SELECT id, content, COALESCE(created_at, 'No Date Available') FROM posts ORDER BY datetime(created_at) DESC")
    posts = cursor.fetchall()
    conn.close()
    return posts or []  # Return an empty list if no posts found

# Function to delete a post from the database
def delete_post(post_id):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        conn.commit()
        conn.close()

# Initialize the database
initialize_database()

# Retrieve and display saved posts
saved_posts = get_saved_posts()

# Group posts by date
posts_by_date = {}
for post_id, content, created_at in saved_posts:
    if created_at and len(created_at.strip()) > 0 and created_at.lower() != "none":
        try:
            # Extract only the date part (YYYY-MM-DD)
            date_str = created_at.split(" ")[0]
        except ValueError:
            date_str = "No Date Available"
    else:
        date_str = "No Date Available"

    if date_str not in posts_by_date:
        posts_by_date[date_str] = []
    posts_by_date[date_str].append((post_id, content))

# Check if there are any posts to display
if not saved_posts:
    st.write("No saved posts available.")
else:
    for date_str, posts in posts_by_date.items():
        st.header(f"Posts from {date_str}")
        for post_id, content in posts:
            # Display post content with delete button for each post
            st.markdown(f"**Post ID {post_id}**: {content}")

            # Delete button for each post, unique key to avoid button duplication
            if st.button("Delete", key=f"delete_{post_id}"):
                delete_post(post_id)
                st.rerun()  # Refresh the app to show updated list

        # Add a line break or horizontal line after each group of posts
        st.markdown("<hr style='border: 1px solid #ddd;' />", unsafe_allow_html=True)
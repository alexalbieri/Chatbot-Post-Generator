import sqlite3
import streamlit as st

st.title("Image Gallery")
st.write("### Your Saved Images")

# Database setup functions
def initialize_database():
    # Connect to SQLite database and create table if it doesn't exist
    try:
        conn = sqlite3.connect("images.db")
        conn.execute("CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY, url TEXT)")
        conn.close()
    except sqlite3.Error as e:
        st.error(f"Database initialization failed: {e}")

# Function to get database connection
def get_connection():
    try:
        conn = sqlite3.connect("images.db")
        return conn
    except sqlite3.Error as e:
        st.error(f"Database connection failed: {e}")
        return None

# Function to get saved images from the database
def get_saved_images():
    conn = get_connection()
    if conn is None:
        return []  # Return empty list if connection fails

    cursor = conn.cursor()
    cursor.execute("SELECT id, url FROM images")
    images = cursor.fetchall()
    conn.close()
    return images or []  # Return an empty list if no images found

# Function to delete an image from the database
def delete_image(image_id):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM images WHERE id = ?", (image_id,))
        conn.commit()
        conn.close()

# Function to save an image to the database
def save_image_to_db(url):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO images (url) VALUES (?)", (url,))
        conn.commit()
        conn.close()

# Initialize the database
initialize_database()

# Retrieve and display saved images
saved_images = get_saved_images()

# Check if there are any images to display
if not saved_images:
    st.write("No saved images available.")
else:
    # Display images in two columns
    for i in range(0, len(saved_images), 2):
        cols = st.columns(2)
        for idx, (image_id, url) in enumerate(saved_images[i:i + 2]):
            col = cols[idx]
            with col:
                # Display saved image with delete button for each image
                st.image(url, use_column_width=True)

                # Delete button for each image, unique key to avoid button duplication
                if st.button("Delete Image", key=f"delete_image_{image_id}"):
                    delete_image(image_id)
                    st.rerun()  # Refresh the app to show updated list

        # Add a line after each row of images (i.e., every two images)
        st.markdown("<hr style='border: 1px solid #ddd;' />", unsafe_allow_html=True)
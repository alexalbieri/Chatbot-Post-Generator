import streamlit as st
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading
import time

# Your predefined sender email and app-specific password
SENDER_EMAIL = "user"
APP_PASSWORD = "password"  

# Function to send email
def send_email(name, email):
    subject = "Publish your linkedIn Post"
    body = f"""Hi {name}, this is Chatty.

It is time to publish your LinkedIn post.

Lovely greetings, Chatty."""
    
    # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to Gmail's SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, email, msg.as_string())
        st.success(f"Reminder email sent to {email} successfully!")
    except Exception as e:
        st.error(f"An error occurred while sending email: {e}")

# Function to schedule email
def schedule_email(name, email, reminder_date, reminder_time):
    reminder_datetime = datetime.strptime(f"{reminder_date} {reminder_time}", "%Y-%m-%d %H:%M")
    delay = (reminder_datetime - datetime.now()).total_seconds()
    if delay > 0:
        threading.Timer(delay, send_email, args=(name, email)).start()
        st.success(f"Reminder set for {reminder_datetime}")
    else:
        st.error("Please enter a future time for the reminder")

# Streamlit user interface with custom CSS for centering the image
st.markdown(
    """
    <style>
    .center-img {
        display: flex;
        justify-content: center;
        align-items: center;\
        margin-top: 0px; 
        margin-bottom: 10px;  
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the image centered at the top of the page
st.markdown('<div class="center-img">', unsafe_allow_html=True)
st.image("/Users/alexandrealbieri/Documents/Personal/Berlin/WBS Coding School/WBS Bootcamp/Data Science/Final Project/Adds-on/linkedin2.png", use_column_width=False, width=250)  # Adjust the path and size as needed
st.markdown('</div>', unsafe_allow_html=True)

st.title("Publish alert")

name = st.text_input("Enter your name")
email = st.text_input("Enter your email address")

# Date picker for selecting the reminder date
reminder_date = st.date_input("Select reminder date", value=datetime.today().date())

# Time input for selecting the reminder time with placeholder text
default_time = datetime.now().time().strftime("%H:%M")
reminder_time = st.text_input("Reminder time", value=default_time, max_chars=5)

if st.button("Set Reminder"):
    if name and email and reminder_date and reminder_time:
        schedule_email(name, email, reminder_date, reminder_time)
    else:
        st.error("Please fill out all fields")

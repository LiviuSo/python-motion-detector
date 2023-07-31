import streamlit as st
from camera import run_camera

st.title("Indoor motion detector")

st.info(
    "Enter your email, start the camera and leave the scene within 5 seconds."
    " Once an object enters and exits the scene you'll be notified via "
    " email.")

email_input = st.text_input("Enter your email")
start_button = st.button("Start camera")
streamlit_image = st.image([], width=400)


def run_camera_streamlit(frame):
    streamlit_image.image(frame)


if start_button:
    if len(email_input) > 0:
        print(email_input)
        run_camera(camera_engine=run_camera_streamlit, receiver=email_input,
                   initial_delay=5)
    else:
        st.info("Enter an email address!")

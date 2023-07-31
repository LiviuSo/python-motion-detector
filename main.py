import streamlit as st
from camera import run_camera

st.title("Indoor motion detector")

st.info("Set delay (in seconds), start the camera and leave the scene."
        " Once an object enters and exits the scene you'll be notified via "
        " email.")

start_button = st.button("Start camera")
streamlit_image = st.image([])


def run_camera_streamlit(frame):
    streamlit_image.image(frame)


if start_button:
    run_camera(run_camera_streamlit, 5)

from pathlib import Path
import PIL
import mysql.connector
import io
import numpy as np
from ultralytics import YOLO
import streamlit as st
import cv2
import pafy

import settings


def load_model(model_path):
    """
    Loads a YOLO object detection model from the specified model_path.

    Parameters:
        model_path (str): The path to the YOLO model file.

    Returns:
        A YOLO object detection model.
    """
    model = YOLO(model_path)
    return model


def display_tracker_options():
    display_tracker = st.radio("Display Tracker", ('Yes', 'No'))
    is_display_tracker = True if display_tracker == 'Yes' else False
    if is_display_tracker:
        tracker_type = st.radio("Tracker", ("bytetrack.yaml", "botsort.yaml"))
        return is_display_tracker, tracker_type
    return is_display_tracker, None


def _display_detected_frames(conf, model, st_frame, image, is_display_tracking=None, tracker=None):
    """
    Display the detected objects on a video frame using the YOLOv8 model.

    Args:
    - conf (float): Confidence threshold for object detection.
    - model (YoloV8): A YOLOv8 object detection model.
    - st_frame (Streamlit object): A Streamlit object to display the detected video.
    - image (numpy array): A numpy array representing the video frame.
    - is_display_tracking (bool): A flag indicating whether to display object tracking (default=None).

    Returns:
    None
    """

    # Resize the image to a standard size
    image = cv2.resize(image, (720, int(720*(9/16))))

    # Display object tracking, if specified
    if is_display_tracking:
        res = model.track(image, conf=conf, persist=True, tracker=tracker)
    else:
        # Predict the objects in the image using the YOLOv8 model
        res = model.predict(image, conf=conf)

    # Plot the detected objects on the video frame
    res_plotted = res[0].plot()
    st_frame.image(res_plotted,
                   caption='Detected Video',
                   channels="BGR",
                   use_column_width=True)


def play_youtube_video(conf, model):
    """
    Plays a YouTube video. Detects objects in real-time using the YOLOv8 object detection model.

    Parameters:
        conf: Confidence of YOLOv8 model.
        model: An instance of the `YOLO` class containing the YOLOv8 model.

    Returns:
        None

    Raises:
        None
    """
    source_youtube = st.sidebar.text_input("YouTube Video URL")

    is_display_tracker, tracker = display_tracker_options()

    if st.sidebar.button('Detect Objects'):
        try:
            video = pafy.new(source_youtube)
            best = video.getbest(preftype="mp4")
            vid_cap = cv2.VideoCapture(best.url)
            st_frame = st.empty()
            while vid_cap.isOpened():
                success, image = vid_cap.read()
                if success:
                    _display_detected_frames(conf,
                                             model,
                                             st_frame,
                                             image,
                                             is_display_tracker,
                                             tracker
                                             )
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Error loading video: " + str(e))


def play_rtsp_stream(conf, model):
    """
    Plays an RTSP stream. Detects objects in real-time using the YOLOv8 object detection model.

    Parameters:
        conf: Confidence of YOLOv8 model.
        model: An instance of the `YOLO` class containing the YOLOv8 model.

    Returns:
        None

    Raises:
        None
    """
    source_rtsp = st.sidebar.text_input("RTSP Stream URL")
    is_display_tracker, tracker = display_tracker_options()
    if st.sidebar.button('Detect Objects'):
        try:
            vid_cap = cv2.VideoCapture(source_rtsp)
            st_frame = st.empty()
            while vid_cap.isOpened():
                success, image = vid_cap.read()
                if success:
                    _display_detected_frames(conf,
                                             model,
                                             st_frame,
                                             image,
                                             is_display_tracker,
                                             tracker
                                             )
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Error loading RTSP stream: " + str(e))


def play_webcam(conf, model):
    """
    Plays a webcam stream. Detects objects in real-time using the YOLOv8 object detection model.

    Parameters:
        conf: Confidence of YOLOv8 model.
        model: An instance of the `YOLO` class containing the YOLOv8 model.

    Returns:
        None

    Raises:
        None
    """
    source_webcam = settings.WEBCAM_PATH
    is_display_tracker, tracker = display_tracker_options()
    if st.sidebar.button('Detect Objects'):
        try:
            vid_cap = cv2.VideoCapture(source_webcam)
            st_frame = st.empty()
            while vid_cap.isOpened():
                success, image = vid_cap.read()
                if success:
                    _display_detected_frames(conf,
                                             model,
                                             st_frame,
                                             image,
                                             is_display_tracker,
                                             tracker,
                                             )
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Error loading video: " + str(e))


def play_stored_video(conf, model, is_display_tracker=None, tracker=None):
    """
    Plays a stored video file. Tracks and detects objects in real-time using the YOLOv8 object detection model.

    Parameters:
        conf: Confidence of YOLOv8 model.
        model: An instance of the `YOLO` class containing the YOLOv8 model.
        is_display_tracker (bool): Flag indicating whether to display object tracking.
        tracker (str): The type of tracker to use.

    Returns:
        None
    """
    source_vid = st.sidebar.selectbox("Choose a video...", settings.VIDEOS_DICT.keys())

    if st.sidebar.button('Detect Video Objects'):
        try:
            vid_cap = cv2.VideoCapture(str(settings.VIDEOS_DICT.get(source_vid)))
            st_frame = st.empty()
            while vid_cap.isOpened():
                success, image = vid_cap.read()
                if success:
                    # Resize the image to a standard size
                    image = cv2.resize(image, (720, int(720*(9/16))))

                    # Display object tracking, if specified
                    if is_display_tracker:
                        res = model.track(image, conf=conf, persist=True, tracker=tracker)
                    else:
                        # Predict the objects in the image using the YOLOv8 model
                        res = model.predict(image, conf=conf)

                    # Plot the detected objects on the video frame
                    res_plotted = res[0].plot()
                    st_frame.image(res_plotted,
                                   caption='Detected Video',
                                   channels="BGR",
                                   use_column_width=True)
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Error loading video: " + str(e))


def main():
    st.title("CRACK AND DENT DETECTION")

    # Load YOLOv8 model
    model_path = Path(settings.MODEL_PATH)
    model = load_model(model_path)

    # Confidence threshold
    conf = st.sidebar.slider("Confidence Threshold", 0.0, 1.0, 0.5, 0.05)

    # Object detection options
    detection_options = ['YouTube Video', 'RTSP Stream', 'Webcam', 'Stored Video']
    selected_option = st.sidebar.selectbox("Select Detection Option", detection_options)

    if selected_option == 'YouTube Video':
        play_youtube_video(conf, model)
    elif selected_option == 'RTSP Stream':
        play_rtsp_stream(conf, model)
    elif selected_option == 'Webcam':
        play_webcam(conf, model)
    elif selected_option == 'Stored Video':
        is_display_tracker, tracker = display_tracker_options()
        play_stored_video(conf, model, is_display_tracker, tracker)


if __name__ == '__main__':
    main()

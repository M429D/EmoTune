#To run: streamlit run EmoTune.py [-- script args]

import streamlit as st
import cv2
import streamlit as st
from deepface import DeepFace
import numpy as np
import time

# Load Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to detect faces in the image
def detect_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces, frame

# Function to analyze emotion using DeepFace
def analyze_emotion(face_img):
    try:
        # Analyze emotion
        result = DeepFace.analyze(face_img, actions=['emotion'], enforce_detection=False)
        
        # Check if the result is a list and extract the first element
        if isinstance(result, list):
            result = result[0]

        # Extract the dominant emotion
        emotion = result.get('dominant_emotion')
    except Exception as e:
        emotion = None
        st.error(f"Emotion analysis failed: {str(e)}")
    return emotion

# Function to start the webcam and process the feed
def webcam_feed():
    cap = cv2.VideoCapture(0)
    stframe = st.empty()  # Placeholder for the video frame
    emotion_display = st.empty()  # Placeholder for the emotion output
    error_display = st.empty()  # Placeholder for the error message

    face_detected_time = None
    error_start_time = None  # Track when the error message is displayed

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.warning("Could not access the webcam.")
            break

        faces, frame = detect_faces(frame)

        if len(faces) == 1:  # Only process if exactly one face is detected
            error_display.empty()  # Clear the error message if exactly one face is detected
            error_start_time = None  # Reset error start time

            # If a face is detected, start or reset the timer
            if face_detected_time is None:
                face_detected_time = time.time()
            else:
                # Check if 3 seconds have passed since the face was detected
                if time.time() - face_detected_time >= 3:
                    # Pause the feed and analyze emotion
                    (x, y, w, h) = faces[0]
                    face_img = frame[y:y+h, x:x+w]
                    face_img_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
                    emotion = analyze_emotion(face_img_rgb)

                    if emotion:
                        emotion_display.markdown(f"<div class='body'>Your current emotion is: {emotion.capitalize()} 😄</div>", unsafe_allow_html=True)

                    # Reset the timer to continue detection
                    face_detected_time = None
                    # Add a short delay before resuming detection
                    time.sleep(2)

        elif len(faces) > 1:  # More than one face detected
            face_detected_time = None  # Reset the timer
            if error_start_time is None:
                error_start_time = time.time()
            error_display.error("Error: More than one face detected. Please ensure only one face is visible.")
            emotion_display.empty()  # Clear the emotion display as multiple faces are detected

            # Ensure the error message stays for at least 2 seconds
            if time.time() - error_start_time < 2:
                time.sleep(2 - (time.time() - error_start_time))

        else:  # No faces detected
            face_detected_time = None  # Reset the timer
            emotion_display.empty()  # Clear the emotion display if no face is detected
            error_display.empty()  # Clear any error if no faces are detected
            error_start_time = None  # Reset error start time

        # Display the frame with face detection rectangles
        for (x, y, w, h) in faces[:1]:  # Only draw the first detected face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame_rgb, channels="RGB")

        # Check if the Terminate button was clicked
        if st.session_state.get("genre_selected") == "terminated":
            break

    cap.release()

# Custom CSS for styling
st.markdown(
    """
    <style>
    /* General styling for the body */
    .body {
        font-family: 'MuseoSans-500', sans-serif;
        font-size: 20px;
        margin-top: 5px;
        margin-bottom: 15px;
        text-align: center;
        line-height: 1.5;
    }

    /* Title styling */
    .title {
        font-family: 'MuseoSans-900', sans-serif;
        font-size: 100px;
        text-align: center;
        color: #00a19c;
        text-shadow: 3px 3px 0px #ffffff;
        margin-bottom: 5px;
        line-height: 1.0;
    }

    /* Subheader styling */
    .subheader {
        font-size: 35px; /* Adjusted font size */
        text-align: center;
        color: #00a19c;
        margin-bottom: 15px;
        line-height: 1.2;
    }

    /* Key features list styling */
    .key-features {
        font-size: 20px;
        margin-top: 0px;
        margin-bottom: 15px;
        text-align: justify;
        line-height: 1.5;
    }

    /* Section headers */
    .section-header {
        font-size: 30px;
        margin-top: 15px;
        margin-bottom: 5px;
        color: #00a19c;
        text-align: center;
        line-height: 1.2;
    }

    /* Form headers */
    .form-header {
        font-size: 30px;
        margin-top: 0px;
        margin-bottom: 15px;
        color: #00a19c;
        text-align: left;
        line-height: 1.2;
    }

    /* Form styling */
    .genre-preferences-form {
        margin-top: 0px; /* Adjusted margin to remove space */
    }

    /* Button styling */
    .stButton>button {
        background-color: #00a19c;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        margin: auto; /* Center button */
        display: block; /* Center button */
    }

    /* Checkbox styling */
    .stCheckbox>label {
        font-size: 18px;
    }

    /* Maximize the width of the main container */
    .reportview-container .main .block-container {
        max-width: 100%;
        padding-top: 0rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 0rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Introduction and Key Features
if "genre_selected" not in st.session_state:
    st.session_state["genre_selected"] = "initial"

if st.session_state["genre_selected"] == "initial":
    
    # Using HTML to display the styled title
    st.markdown('<div class="title">EmoTune</div>', unsafe_allow_html=True)

    # Subheader and other content
    st.markdown('<div class="subheader">Facial Emotion Recognition Based Instrumental Music Recommendation Website</div>', unsafe_allow_html=True)

    # Display the image using Streamlit's built-in function
    st.image("EmoTune Welcome.jpg", use_column_width=True)

    st.markdown('<div class="key-features">👋🏻 Hello and welcome dear user, we\'re thrilled to have you here. EmoTune is designed to make your music experience truly personal and emotionally resonant. Here\'s how we do it:\n</div>', unsafe_allow_html=True)
    st.markdown('<div class="key-features">1. Genre Preferences: Customize your music journey by selecting your preferred instrumental genres for each of the 7 specific emotions, creating a truly personalized touch.\n</div>', unsafe_allow_html=True)
    st.markdown('<div class="key-features">2. Emotion Detection: Harness the power of cutting-edge facial emotion recognition algorithms to accurately identify your current emotion in real-time.\n</div>', unsafe_allow_html=True)
    st.markdown('<div class="key-features">3. Personalized Music Recommendations: Get instrumental music suggestions tailored to your emotional state, enhancing your listening experience.\n</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">Instrumental Music Genre Preference Customization</div>', unsafe_allow_html=True)
    st.markdown('<div class="body">Choose genres to link with the specific emotions, more than 1 may be selected:</div>', unsafe_allow_html=True)
    
    genres = [
        "Classical", "Jazz", "Ambient", "Electronic", "Piano Solos", 
        "Acoustic Guitar", "Orchestral", "Nature Sounds", "Meditation", 
        "Lo-fi Beats", "Chillhop", "World Music", 
        "Instrumental Rock", "Synthwave", "Upbeat"
    ]

    emotions = ["Anger", "Happy", "Surprise", "Fear", "Sadness", "Disgust", "Neutral"]

    genre_preferences = {}

    with st.form(key='genre_preferences_form',):
        st.markdown("<div class='genre-preferences-form'>", unsafe_allow_html=True)
        for emotion in emotions:
            st.markdown(f"<div class='form-header'>{emotion}</div>", unsafe_allow_html=True)
            cols = st.columns(3)
            for i, genre in enumerate(genres):
                with cols[i % 3]:
                    genre_preferences[f"{emotion}_{genre}"] = st.checkbox(f"{genre}", key=f"{emotion}_{genre}")
        st.markdown("</div>", unsafe_allow_html=True)
        submit_button = st.form_submit_button(label='Launch Now!')

    if submit_button:
        st.session_state["genre_selected"] = "customized"
        st.rerun()

# Emotion Capture State
elif st.session_state["genre_selected"] == "customized":
    st.markdown('<div class="title">EmoTune</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Facial Emotion Recognition Based Instrumental Music Recommendation Website</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Facial Expression Capture </div>', unsafe_allow_html=True)
    st.markdown('<div class="body">Please ensure your device\'s camera is \'ON\' for automatic capture of your amazing facial expression and the image will appear below ⬇⬇.</div>', unsafe_allow_html=True)

    # Start the webcam feed and run face detection
    webcam_feed()
        
    st.markdown('<div class="section-header">Recommended Instrumental Music</div>', unsafe_allow_html=True)
    # Placeholder for recommended song title
    st.markdown('<div class="body">Cherry Love by Mark Andrew Hansen (Piano Solos)</div>', unsafe_allow_html=True)
    
    # Code to embed music player
    st.image("Cherry Love Spotify.png", use_column_width=True)
    st.audio("Cheery Love.mp3")
    Termination = st.button("Terminate Session")

    if Termination:
        st.session_state["genre_selected"] = "terminated"
        st.rerun()

elif st.session_state["genre_selected"] == "terminated":

    st.markdown('<div class="title">EmoTune</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Facial Emotion Recognition Based Instrumental Music Recommendation Website</div>', unsafe_allow_html=True)
    st.markdown('<div class="body">Thank you for your patronage, and we hope to see you again soon! 👋🏽👋🏽\n</div>', unsafe_allow_html=True)

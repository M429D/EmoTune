#To run: streamlit run EmoTune.py [-- script args]

import streamlit as st

# Custom CSS for styling
st.markdown(
    """
    <style>
    /* General styling for the body */
    body {
        font-family: 'MuseoSans-500', sans-serif;
        background-color: #f0f2f6;
        color: #333333;
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
        text-align: left;
        line-height: 1.5;
    }

    /* Section headers */
    .section-header {
        font-size: 30px;
        margin-top: 15px;
        margin-bottom: 15px;
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
        text-align: center;
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
    st.session_state["emotion_captured"] = False

if st.session_state["genre_selected"] == "initial":
    
    # Using HTML to display the styled title
    st.markdown('<div class="title">EmoTune</div>', unsafe_allow_html=True)

    # Subheader and other content
    st.markdown('<div class="subheader">Facial Emotion Recognition Based Instrumental Music Recommendation Website</div>', unsafe_allow_html=True)

    # Display the image using Streamlit's built-in function
    st.image("EmoTune Welcome.jpg", use_column_width=True)

    st.markdown('<div class="key-features">👋🏻 Hello and welcome dear user, we\'re thrilled to have you here. EmoTune is designed to make your music experience truly personal and emotionally resonant. Here\'s how we do it:\n</div>', unsafe_allow_html=True)
    st.markdown('<div class="key-features">✍🏻 Genre Preferences: Customize your music journey by selecting your preferred instrumental genres for each of the 7 specific emotions, creating a truly personalized touch.\n</div>', unsafe_allow_html=True)
    st.markdown('<div class="key-features">🎭 Emotion Detection: Harness the power of cutting-edge facial emotion recognition algorithms to accurately identify your current emotion in real-time.\n</div>', unsafe_allow_html=True)
    st.markdown('<div class="key-features">🎺 Personalized Music Recommendations: Get instrumental music suggestions tailored to your emotional state, enhancing your listening experience.\n</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Instrumental Music Genre Preference Customization</div>', unsafe_allow_html=True)
    st.markdown('<div class="key-features">Choose genres to link with the specific emotions, more than 1 may be selected:</div>', unsafe_allow_html=True)

    genres = [
        "Classical", "Jazz", "Ambient", "Electronic", "Piano Solos", 
        "Acoustic Guitar", "Orchestral", "Nature Sounds", "Meditation", 
        "Lo-fi Beats", "Chillhop", "World Music", 
        "Instrumental Rock", "Synthwave", "Upbeat"
    ]

    emotions = ["Anger", "Happy", "Surprise", "Fear", "Sadness", "Disgust", "Neutral"]

    genre_preferences = {}

    with st.form(key='genre_preferences_form'):
        st.markdown("<div class='genre-preferences-form'>", unsafe_allow_html=True)
        for emotion in emotions:
            st.markdown(f"<div class='form-header'>{emotion}</div>", unsafe_allow_html=True)
            cols = st.columns(3)
            for i, genre in enumerate(genres):
                with cols[i % 3]:
                    genre_preferences[f"{emotion}_{genre}"] = st.checkbox(f"{genre}", key=f"{emotion}_{genre}")
        st.markdown("</div>", unsafe_allow_html=True)
        submit_button = st.form_submit_button(label='Submit Preferences')

    if submit_button:
        st.session_state["genre_selected"] = "customized"
        st.session_state["emotion_captured"] = False
        st.experimental_rerun()

# Emotion Capture State
elif st.session_state["genre_selected"] == "customized":
    st.markdown('<div class="title">EmoTune</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Facial Emotion Recognition Based Instrumental Music Recommendation Website</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Emotion Capture</div>', unsafe_allow_html=True)
    st.markdown('<div class="key-features">Please ensure your device\'s camera is \'ON\' before pressing the button below to capture your amazing facial expression and the image will appear below ⬇⬇.</div>', unsafe_allow_html=True)

    if st.button("Capture Emotion"):
        # Code to capture and display emotion
        st.markdown('<div class="key-features">Your current emotion is: Happy 😆</div>', unsafe_allow_html=True)  # Placeholder for emotion output
        # Display the image using Streamlit's built-in function
        st.image("Captured Image.jpg", use_column_width=True)
        st.session_state["emotion_captured"] = True
        st.experimental_rerun()

    if st.session_state["emotion_captured"]:
        st.markdown('<div class="key-features">Your current emotion is: Happy 😆</div>', unsafe_allow_html=True)  # Placeholder for emotion output
        st.image("Captured Image.jpg", use_column_width=True)
        if st.button("Recommendation"):
            st.session_state["genre_selected"] = "captured"
            st.experimental_rerun()

# Song Recommendation State
elif st.session_state["genre_selected"] == "captured":
    st.markdown('<div class="title">EmoTune</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Facial Emotion Recognition Based Instrumental Music Recommendation Website</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Recommended Music</div>', unsafe_allow_html=True)
    # Placeholder for recommended song title
    st.markdown('<div class="key-features">Cherry Love by Mark Andrew Hansen (Piano Solos)</div>', unsafe_allow_html=True)
    
    # Code to embed music player
    st.image("Cherry Love Spotify.png", use_column_width=True)
    st.audio("Cheery Love.mp3")
    st.markdown('<div class="key-features">Flashing Lights by Kanye West (Electronic)</div>', unsafe_allow_html=True)
    st.image("Flashing Lights Spotify.png", use_column_width=True)
    st.audio("Flashing Lights.mp3")
    st.markdown('<div class="key-features">Industry Baby by Lil Nas X (Upbeat)</div>', unsafe_allow_html=True)
    st.image("Industry Baby Spotify.png", use_column_width=True)
    st.audio("Industry Baby.mp3")




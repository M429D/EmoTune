# streamlit run EmoTune.py [arg--]

# Custom CSS for styling
st.markdown(
    """
    <style>
    .body {
        font-family: 'MuseoSans-500', sans-serif;
        font-size: 20px;
        margin-top: 5px;
        margin-bottom: 15px;
        text-align: center;
        line-height: 1.5;
    }

    .title {
        font-family: 'MuseoSans-900', sans-serif;
        font-size: 100px;
        text-align: center;
        color: #00a19c;
        text-shadow: 3px 3px 0px #ffffff;
        margin-bottom: 5px;
        line-height: 1.0;
    }

    .subheader {
        font-size: 35px;
        text-align: center;
        color: #00a19c;
        margin-bottom: 15px;
        line-height: 1.2;
    }

    .key-features {
        font-size: 20px;
        margin-top: 0px;
        margin-bottom: 15px;
        text-align: justify;
        line-height: 1.5;
    }

    .section-header {
        font-size: 30px;
        margin-top: 15px;
        margin-bottom: 5px;
        color: #00a19c;
        text-align: center;
        line-height: 1.2;
    }

    .form-header {
        font-size: 30px;
        margin-top: 10px;
        margin-bottom: 10px;
        color: #00a19c;
        text-align: left;
        line-height: 1.2;
    }

    .genre-preferences-form {
        margin-top: 10px;
    }

    .stButton>button {
        background-color: #00a19c;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        margin: auto;
        margin-top: 10px;
        display: block;
    }

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

# Load Haar cascades for face and eye detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eyes_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

# Function to detect faces and eyes in the image
def detect_faces_and_eyes(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(60, 60))
    
    for (x, y, w, h) in faces:

        # Draw rectangle around the face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (128, 0, 128), 2)
        
        # Detect eyes within the face region
        faceROI = gray[y:y + h, x:x + w]
        eyes = eyes_cascade.detectMultiScale(faceROI, scaleFactor=1.1, minNeighbors=10, minSize=(20, 20))

        for (x2, y2, w2, h2) in eyes:
            eye_center = (x + x2 + w2 // 2, y + y2 + h2 // 2)
            radius = int(round((w2 + h2) * 0.25))
            cv2.circle(frame, eye_center, radius, (0, 255, 255), 2)
    return faces, frame

# Function to analyze emotion using DeepFace
def analyze_emotion(face_img):
    try:
        result = DeepFace.analyze(face_img, actions=['emotion'], enforce_detection=False)
        if isinstance(result, list):
            result = result[0]
        emotion = result.get('dominant_emotion')
    except AttributeError as e:
        emotion = None
        st.error("Emotion analysis failed: DeepFace model might be incompatible. Ensure all dependencies are correctly installed.")
    except Exception as e:
        emotion = None
        st.error(f"Emotion analysis failed: {str(e)}")
    return emotion

# Function to start the webcam and process the feed
# Function to start the webcam and process the feed
def webcam_feed():
    cap = cv2.VideoCapture(0)

    face_detected_time = None
    error_start_time = None

    # Create placeholders for Streamlit components outside the loop
    stframe = st.empty()
    emotion_display = st.empty()
    error_display = st.empty()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.warning("Could not access the webcam.")
            break

        faces, frame = detect_faces_and_eyes(frame)

        if len(faces) == 1:
            error_display.empty()
            error_start_time = None
            if face_detected_time is None:
                face_detected_time = time.time()
            else:
                if time.time() - face_detected_time >= 3:
                    (x, y, w, h) = faces[0]
                    face_img = frame[y:y+h, x:x+w]
                    face_img_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
                    emotion = analyze_emotion(face_img_rgb)
                    border_color = (128, 0, 128)  # Purple color
                    frame = cv2.copyMakeBorder(frame, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=border_color)
                    
                    # Centering and resizing the webcam feed
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    stframe.image(frame_rgb, channels="RGB", use_column_width=True)

                    if emotion:
                        emotion_display.markdown(f"<div class='body'>Your current emotion is ▶▶ {emotion.capitalize()} </div>", unsafe_allow_html=True)

                    face_detected_time = None
                    time.sleep(5)
                    st.session_state["state"] = "active"
                    st.rerun()

        elif len(faces) > 1:
            face_detected_time = None
            if error_start_time is None:
                error_start_time = time.time()
            error_display.error("Error: More than one face detected. Please ensure only one face is visible.")
            emotion_display.empty()

            if time.time() - error_start_time < 2:
                time.sleep(2 - (time.time() - error_start_time))

        else:
            face_detected_time = None
            error_start_time = None

        # Display the frame with rectangles around faces and circles around eyes
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame_rgb, channels="RGB", use_column_width=True)

    cap.release()

# Session state initialization
if "state" not in st.session_state:
    st.session_state["state"] = "initial"

# Placeholder for clearing state
placeholder = st.empty()

# Introduction and Key Features
if st.session_state["state"] == "initial":
    with placeholder.container():  # Wrap the content in a placeholder container
        st.markdown('<div class="title">EmoTune</div>', unsafe_allow_html=True)
        st.markdown('<div class="subheader">Facial Emotion Recognition Based Instrumental Music Recommendation Website</div>', unsafe_allow_html=True)
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

        # Initialize the genre preferences dictionary in session state if it doesn't exist
        if "genre_preferences" not in st.session_state:
            st.session_state["genre_preferences"] = {emotion: [] for emotion in emotions}

        with st.form(key='genre_preferences_form'):
            for emotion in emotions:
                st.markdown(f"<div class='form-header'>{emotion}</div>", unsafe_allow_html=True)
                cols = st.columns(3)
                for i, genre in enumerate(genres):
                    with cols[i % 3]:
                        selected = st.checkbox(genre, key=f"{emotion}_{genre}")
                        if selected:
                            st.session_state["genre_preferences"][emotion].append(genre)
            submit_button = st.form_submit_button(label='Launch Now!')

        if submit_button:
            st.session_state["state"] = "customized"
            st.rerun()

# Emotion Capture State
elif st.session_state["state"] == "customized":
    st.write(st.session_state["genre_preferences"]) #<<To see Genre Preference Form Input
    st.markdown('<div class="title">EmoTune</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Facial Emotion Recognition Based Instrumental Music Recommendation Website</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Facial Expression Capture </div>', unsafe_allow_html=True)
    st.markdown('<div class="body">Please ensure your device\'s camera is \'ON\' for automatic capture of your amazing facial expression and the image will appear below ⬇⬇.</div>', unsafe_allow_html=True)
    
    # Start the webcam feed and run face detection
    webcam_feed()

elif st.session_state["state"] == "active":
    st.markdown('<div class="title">EmoTune</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Facial Emotion Recognition Based Instrumental Music Recommendation Website</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Recommended Instrumental Music</div>', unsafe_allow_html=True)
    st.markdown('<div class="body">Cherry Love by Mark Andrew Hansen (Piano Solos)</div>', unsafe_allow_html=True)
    st.image("Cherry Love Spotify.png", use_column_width=True)
    st.audio("Cheery Love.mp3")
    
    Termination = st.button("Terminate Session")

    if Termination:
        st.session_state["state"] = "terminated"
        st.rerun()

# Terminated Session State
elif st.session_state["state"] == "terminated":
    st.markdown('<div class="title">EmoTune</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Facial Emotion Recognition Based Instrumental Music Recommendation Website</div>', unsafe_allow_html=True)
    st.markdown('<div class="body">Thank you for your patronage, and we hope to see you again soon! 👋🏽👋🏽\n</div>', unsafe_allow_html=True)

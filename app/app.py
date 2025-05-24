import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import os

# Set page config as the first Streamlit command
st.set_page_config(page_title="Language Translator", layout="centered")

# Custom CSS to style the landing page
st.markdown("""
    <style>
        .main {
            background-color: #f0f8ff;
            color: #333;
            font-family: 'Helvetica', sans-serif;
        }
        .header {
            font-size: 40px;
            color: #4CAF50;
            font-weight: bold;
            text-align: center;
            padding: 20px;
        }
        .subheader {
            font-size: 18px;
            color: #555;
            text-align: center;
        }
        .button {
            background-color: #4CAF50;
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 16px;
        }
        .button:hover {
            background-color: #45a049;
        }
    </style>
""", unsafe_allow_html=True)

# Page header and sub-header
st.markdown('<div class="header">🌐 Language Translator</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Translate text between multiple languages instantly!</div>', unsafe_allow_html=True)

# Language selection and text input
languages = {
    "English": "en",
    "Urdu": "ur",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Chinese (simplified)": "zh-CN",
    "Arabic": "ar",
    "Hindi": "hi"
}

input_text = st.text_area("Enter text to translate")
target_lang = st.selectbox("Select Target Language", list(languages.keys()))

# Store translated text globally
translated = ""

if st.button("Translate", key="translate_button", help="Click to translate", use_container_width=True):
    if input_text:
        try:
            translated = GoogleTranslator(source='auto', target=languages[target_lang]).translate(input_text)
            st.session_state["translated"] = translated  # save in session
            st.success(f"**Translated Text:** {translated}")
        except Exception as e:
            st.error(f"Translation failed: {e}")
    else:
        st.warning("Please enter text.")

if st.button("Read Aloud", key="read_aloud_button", help="Click to hear the translation", use_container_width=True):
    if "translated" in st.session_state and st.session_state["translated"]:
        try:
            # Generate the speech
            tts = gTTS(text=st.session_state["translated"], lang=languages[target_lang])
            tts.save("translated_audio.mp3")
            
            # Use a context manager to ensure file is properly closed before opening for Streamlit
            with open("translated_audio.mp3", "rb") as audio_file:
                st.audio(audio_file.read(), format="audio/mp3")
            
            # Clean up audio file after playing
            os.remove("translated_audio.mp3")
        except Exception as e:
            st.error(f"TTS failed: {e}")
    else:
        st.warning("Please translate some text first.")

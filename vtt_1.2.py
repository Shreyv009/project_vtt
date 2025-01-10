import streamlit as st
import speech_recognition as sr
from googletrans import Translator
import pyttsx3

# Initialize Translator and TTS engine
translator = Translator()
engine = pyttsx3.init()

# Sidebar options
st.sidebar.header("Settings")
src_language = st.sidebar.selectbox("Select Speech-to-Text Language", [
    "English", "Hindi", "Tamil", "Telugu", "Bengali"
])
target_language = st.sidebar.selectbox("Select Translation Language", [
    "English", "Hindi", "Tamil", "Telugu", "Bengali"
])

# Map languages to their codes
lang_codes = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Bengali": "bn",
}

src_language_code = lang_codes[src_language]
target_language_code = lang_codes[target_language]

# App title
st.title("Real-Time Translation App")

# Placeholder for speech-to-text output
stt_text = st.empty()

# Placeholder for translated text
translated_text = st.empty()

# Start Listening button
if st.button("Start Listening"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening... Speak now.")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            st.write("Processing your speech...")
            text = recognizer.recognize_google(audio, language=src_language_code)
            stt_text.text_area("Speech-to-Text Output:", text)
        except sr.UnknownValueError:
            st.write("Sorry, could not understand the audio.")
        except sr.RequestError as e:
            st.write(f"Could not request results; {e}")

# Translate Text button
if st.button("Translate Text"):
    if stt_text:
        translation = translator.translate(stt_text, src=src_language_code, dest=target_language_code)
        translated_output = translation.text
        translated_text.text_area("Translated Text:", translated_output)
    else:
        st.write("Please perform speech-to-text conversion first.")

# Convert Translated Text to Voice button
if st.button("Convert Translated Text to Voice"):
    if translated_text:
        engine.setProperty("voice", target_language_code)
        engine.say(translated_text)
        engine.runAndWait()
        st.write("Playback completed.")
    else:
        st.write("Please translate text first.")

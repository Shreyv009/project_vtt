import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
import tempfile
import openai

# Configure OpenAI API key
openai.api_key = "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"  # Replace with your ChatGPT API key

# Streamlit App
st.title("Voice-to-Text and Text-to-Voice System for Indian Languages")
st.write("Convert your voice to text and text to voice in Indian languages.")

# Sidebar for language selection
languages = {
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Marathi": "mr",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Kannada": "kn",
    "Malayalam": "ml",
    "English": "en"
}
selected_language = st.sidebar.selectbox("Select Language", list(languages.keys()))

# Speech-to-Text Function
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak now.")
        try:
            audio = recognizer.listen(source, timeout=10)
            st.success("Processing audio...")
            # Recognize speech
            text = recognizer.recognize_google(audio, language=languages[selected_language])
            return text
        except sr.UnknownValueError:
            return "Sorry, could not understand the audio."
        except sr.RequestError as e:
            return f"API error: {e}"

# Text-to-Speech Function
def text_to_speech(text, language_code):
    tts = gTTS(text=text, lang=language_code, slow=False)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)
    return temp_file.name

# ChatGPT for Text Processing (Optional)
def process_text_with_chatgpt(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Translate and refine the following text to {selected_language}: {text}",
        max_tokens=100
    )
    return response.choices[0].text.strip()

# Tabs for functionalities
tab1, tab2 = st.tabs(["Voice-to-Text", "Text-to-Voice"])

# Voice-to-Text Tab
with tab1:
    st.header("Voice-to-Text")
    if st.button("Start Speaking"):
        transcribed_text = speech_to_text()
        st.write("Transcribed Text:")
        st.text_area("Output", transcribed_text, height=150)
        if st.checkbox("Process with ChatGPT (Optional)"):
            if transcribed_text:
                refined_text = process_text_with_chatgpt(transcribed_text)
                st.write("Refined Text:")
                st.text_area("Refined Output", refined_text, height=150)

# Text-to-Voice Tab
with tab2:
    st.header("Text-to-Voice")
    input_text = st.text_area("Enter text to convert into speech", height=150)
    if st.button("Convert to Voice"):
        if input_text:
            audio_file = text_to_speech(input_text, languages[selected_language])
            st.audio(audio_file, format="audio/mp3")
        else:
            st.warning("Please enter some text.")

# Footer
st.markdown("Developed by Shrey Vardhan. Supports multiple Indian languages.")

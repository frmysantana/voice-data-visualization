import streamlit as st
import pandas as pd
import speech_recognition as sr
import altair as alt
import tempfile
from st_audiorec import st_audiorec

#
st.title("Voice-Controlled CSV Data Visualization App")
st.write("Upload a CSV file and use voice commands to interact with the data.")

#
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

#
r = sr.Recognizer()

#
df = None

#
def visualize_data(command):
    if "pie chart" in command:
        #
        chart = alt.Chart(df).mark_circle().encode(
            x='X Axis',
            size='Y Axis',
            color='Category:N'
        ).properties(
            width=600,
            height=400
        )

        st.write("Pie Chart:")
        st.altair_chart(chart)
    elif "line chart" in command:
        #
        chart = alt.Chart(df).mark_line().encode(
            x='X Axis',
            y='Y Axis'
        ).properties(
            width=600,
            height=400
        )

        st.write("Line Chart:")
        st.altair_chart(chart)

#
def record_audio():
    st.write("Press the 'Record' button and speak your command...")

    wav_audio_data = st_audiorec()

    if wav_audio_data is not None:
        # st.audio(wav_audio_data, format='audio/wav')

        st.write("Recording stopped.")
        st.write("Recognizing command...")

        audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")

        with audio_file as f:
            f.write(wav_audio_data)

        #
        with sr.AudioFile(audio_file.name) as source:
            try:
                audio_data = r.record(source)
                command = r.recognize_google(audio_data)
                st.write(f"Recognized command: {command}")
                visualize_data(command)
            except sr.UnknownValueError:
                st.write("Sorry, I couldn't understand the command. Please try again.")

#
if uploaded_file:
    df = pd.read_csv(uploaded_file)

record_audio()

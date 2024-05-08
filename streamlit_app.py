import streamlit as st
import pandas as pd
import speech_recognition as sr
import altair as alt
import tempfile
from st_audiorec import st_audiorec

st.set_page_config(layout="wide")
st.title("Voice-Controlled CSV Data Visualization App")
st.write("Upload a CSV file and use voice commands to interact with the data.")

r = sr.Recognizer()
df = None

if "charts" not in st.session_state:
    st.session_state.charts = []

col1, col2 = st.columns([6,6])

with col1:
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)

def visualize_data(command):
    if df is not None:
        # todo: add checks to the uploaded data and return errors if not properly formtted for a chart type
        # todo: add a different chart type
        if "pie chart" in command:
            chart = alt.Chart(df).mark_arc().encode(
                theta=alt.Theta("Y Axis", type="quantitative"),
                color=alt.Color("Category:N")
            ).properties(
                width=600,
                height=400
            )
            st.session_state.charts.append(("Pie Chart", chart))
        elif "line chart" in command:
            chart = alt.Chart(df).mark_line().encode(
                x='X Axis',
                y='Y Axis'
            ).properties(
                width=600,
                height=400
            )
            st.session_state.charts.append(("Line Chart", chart))
        elif "bar chart" in command:
            chart = alt.Chart(df).mark_bar().encode(
                x='X Axis',
                y='Y Axis',
                color='Category:N'
            ).properties(
                width=600, 
                height=400
            )
            st.session_state.charts.append(("Bar Chart", chart))

with col2:
    st.write("Press the 'Record' button and speak your command...")

    wav_audio_data = st_audiorec()

    if wav_audio_data is not None:
        st.write("Recording stopped.")
        st.write("Recognizing command...")

        audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")

        with audio_file as f:
            f.write(wav_audio_data)

        with sr.AudioFile(audio_file.name) as source:
            try:
                audio_data = r.record(source)
                command = r.recognize_google(audio_data)
                st.write(f"Recognized command: {command}")
                visualize_data(command)
            except sr.UnknownValueError:
                st.write("Sorry, I couldn't understand the command. Please try again.")


if len(st.session_state.charts) != 0:
    st.write("Charts:")
    charts_col1, charts_col2 = st.columns(2)
    ind = 1
     # Display all charts
    for title, chart in st.session_state.charts:
        if ind % 2 == 1:
            with charts_col1:
                st.write(title)
                st.altair_chart(chart)
        else:
            with charts_col2:
                st.write(title)
                st.altair_chart(chart)
        ind += 1
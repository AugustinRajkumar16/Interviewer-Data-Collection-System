"""
Interviewer  Data Collection System - online_recording_voice-of-interview
Code Developed by Augustin Rajkumar -  October 14, 2024.
Copyright © Augustin Rajkumar. All rights reserved.
This program is the intellectual property of Augustin Rajkumar, and may not be distributed 
or reproduced without explicit authorization from the copyright holder.
--------------------------------------------------------------------------------------------------------------------------------

Python Packages Installation:

! pip install deepgram-sdk flask pydub jsonlines

"""
# Import Libraries
import streamlit as st
import sounddevice as sd
from scipy.io.wavfile import write
import jsonlines
import asyncio
from deepgram import Deepgram
import os
import threading

# Deepgram API key
DEEPGRAM_API_KEY = 'your own API key'

# Initialize the Deepgram client
deepgram = Deepgram(DEEPGRAM_API_KEY)

# Initialize session state for recording and button states
if 'is_recording' not in st.session_state:
    st.session_state.is_recording = False
if 'start_disabled' not in st.session_state:
    st.session_state.start_disabled = False
if 'stop_disabled' not in st.session_state:
    st.session_state.stop_disabled = True

# Function to handle audio recording in a separate thread
def record_audio_thread(duration=3600, sample_rate=44100):
    st.session_state.is_recording = True
    st.write("Recording...")

    # Record audio using sounddevice
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()  # Wait until the recording is finished
    st.session_state.is_recording = False
    st.write("Recording finished.")

    # Save the audio file as 'output.wav'
    write('output.wav', sample_rate, recording)
    st.write("Audio saved as output.wav")

# Asynchronous function to transcribe the audio using Deepgram
async def transcribe_audio(file_path):
    if not os.path.exists(file_path):  # Check if the file exists
        st.error(f"File '{file_path}' not found. Please check if recording was successful.")
        return

    with open(file_path, 'rb') as audio:
        source = {'buffer': audio, 'mimetype': 'audio/wav'}

        # Send the audio file to Deepgram for transcription
        response = await deepgram.transcription.prerecorded(source, {'punctuate': True, 'diarize': True})

        # Display the transcription result
        transcription = response['results']['channels'][0]['alternatives'][0]['transcript']
        st.write("Transcription:")
        st.write(transcription)

        # Save the transcription to a JSONL file
        with jsonlines.open('transcription.jsonl', mode='w') as writer:
            writer.write(response)

        st.write("Transcription saved in 'transcription.jsonl'.")

# Main Streamlit app interface
st.title("Interview Data Collection System")
st.write("This system records audio, transcribes it, and saves the transcription in JSONL format.")

# Button to start recording
if st.button("Start Recording", disabled=st.session_state.start_disabled):
    st.session_state.start_disabled = True  # Disable start button
    st.session_state.stop_disabled = False  # Enable stop button
    st.write("Starting the recording... Please wait.")
    
    # Start recording in a separate thread
    threading.Thread(target=record_audio_thread, args=(3600,)).start()

# Button to stop recording
if st.button("Stop Recording", disabled=st.session_state.stop_disabled):
    st.session_state.is_recording = False
    st.session_state.stop_disabled = True  # Disable stop button
    st.session_state.start_disabled = False  # Enable start button
    st.write("Recording stopped.")

# If recording has finished, transcribe the audio
if not st.session_state.is_recording and os.path.exists('output.wav'):
    audio_file = 'output.wav'
    asyncio.run(transcribe_audio(audio_file))

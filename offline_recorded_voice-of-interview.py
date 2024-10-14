"""
Interviewer  Data Collection System - offline_recorded_voice-of-interview
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
import jsonlines
import asyncio
from deepgram import Deepgram
import tempfile
import os

# Deepgram API key
DEEPGRAM_API_KEY = 'your own API key'

# Initialize the Deepgram client
deepgram = Deepgram(DEEPGRAM_API_KEY)

# Function to convert audio file to wav
def convert_to_wav(file):
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp_wav.write(file.read())
    temp_wav.close()
    return temp_wav.name

# Function to assign speaker labels and combine words into sentences
def assign_speaker_labels_and_combine(diarized_output):
    labeled_sentences = []
    current_speaker = None
    current_sentence = []

    for word_info in diarized_output:
        if 'speaker' in word_info:
            speaker_label = "Interviewee" if word_info['speaker'] == 1 else "Interviewer"

            # Start a new sentence if the speaker changes
            if speaker_label != current_speaker:
                if current_sentence:
                    labeled_sentences.append((current_speaker, ' '.join(current_sentence)))
                    current_sentence = []  # Reset current sentence
                current_speaker = speaker_label

            # Append the word to the current sentence
            current_sentence.append(word_info['word'])

    # Append the last sentence if any
    if current_sentence:
        labeled_sentences.append((current_speaker, ' '.join(current_sentence)))

    return labeled_sentences

# Function to transcribe audio
async def transcribe_audio(file, filename):
    if not file:
        st.error("No file uploaded.")
        return

    # Convert the file to a wav format
    wav_file_path = convert_to_wav(file)

    # Open the wav file in binary mode to send to Deepgram
    with open(wav_file_path, 'rb') as audio_file:
        source = {'buffer': audio_file, 'mimetype': 'audio/wav'}

        # Send the audio file to Deepgram for transcription with diarization
        response = await deepgram.transcription.prerecorded(source, {'punctuate': True, 'diarize': True})

        # Extract the diarized words
        if 'results' in response and 'channels' in response['results']:
            diarized_output = response['results']['channels'][0]['alternatives'][0]['words']

            # Assign speaker labels and combine words into sentences
            labeled_sentences = assign_speaker_labels_and_combine(diarized_output)

            # Display the transcription with full sentences and speaker differentiation
            st.write("Transcription with Speaker Differentiation:")
            for label, sentence in labeled_sentences:
                st.write(f"{label}: {sentence}")

            # Save the structured data to a JSONL file
            output_filename = f"{filename}_transcription.jsonl"
            with jsonlines.open(output_filename, mode='w') as writer:
                for label, sentence in labeled_sentences:
                    writer.write({label: sentence})

            st.write(f"Transcription saved in '{output_filename}'.")

        else:
            st.error("Diarization data not found in the transcription response.")

# Streamlit UI
st.title("Interview Data Collection System")
st.write("Upload an audio file to transcribe and save the transcription in JSONL format with speaker differentiation.")

uploaded_file = st.file_uploader("Upload audio file", type=["wav", "mp3"], label_visibility="visible")

if st.button("Transcribe"):
    if uploaded_file:
        # Get the filename without extension
        filename = os.path.splitext(uploaded_file.name)[0]
        asyncio.run(transcribe_audio(uploaded_file, filename))
    else:
        st.error("Please upload an audio file.")

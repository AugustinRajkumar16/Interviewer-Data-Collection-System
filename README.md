# Interviewer Data Collection System

## Overview
The Interviewer Data Collection System is designed to record conversations during interviews, transcribe them, and collect training data for fine-tuning an Interview Language Model (LLM). The system can differentiate between the candidate and the interviewer, and it stores transcribed data in JSONL format.

## Prerequisites

Before running the project, make sure you have the following installed:

- Python 3.10+
- pip (Python package installer)

## Get the Source Code

You can get the source code in two ways:

- **Download as a ZIP file:** [Download here](https://github.com/AugustinRajkumar16/Interviewer-Data-Collection-System/archive/refs/heads/main.zip), then extract it to a folder of your choice.
- **Clone the repository using Git:** 

    ```bash
    git clone https://github.com/AugustinRajkumar16/Interviewer-Data-Collection-System.git
    ```

## Install the Required Python Packages

In your project directory, install the necessary Python libraries:

```bash
  pip install deepgram-sdk pydub jsonlines streamlit sounddevice scipy
```

## Technical Specifications

- **Speech-to-Text Service:** [Deepgram (ensure you have an API key)](https://developers.deepgram.com/docs/create-additional-api-keys)
- **Output Data Format:** JSONL

## Features
- Hands-free operation during interviews.
- Speaker differentiation between candidate and interviewer.
- Timestamped transcriptions saved in a structured format.

## Notes
- Ensure that your Deepgram API key is correctly set in the code before running.
- Adjust the recording duration in the online mode code if necessary.

## Usage

### Running the System

#### Online Mode

1. Navigate to the directory where the online recording code is saved.
2. Run the Streamlit app:

   ```bash
   streamlit run online_recording_voice-of-interview.py
   ```

3. Open the provided URL in your web browser to access the interface.
4. Click the "Start Recording" button to begin recording the interview.
5. Click the "Stop Recording" button to finish recording.
6. The transcription will be automatically generated and saved in `transcription.jsonl`, where `filename` is the name of the uploaded audio file.

**Note:** The results may not be optimal, as I am currently using a CPU with only 8GB of RAM.

#### Offline Mode

1. Navigate to the directory where the offline recording code is saved.
2. Run the Streamlit app:

   ```bash
   streamlit run offline_recorded_voice-of-interview.py
   ```

3. Open the provided URL in your web browser to access the interface.
4. Upload an audio file (in WAV or MP3 format).
5. Click the "Transcribe" button to generate the transcription.
6. The transcription will be saved in `filename_transcription.jsonl`, where `filename` is the name of the uploaded audio file.

## Acknowledgements

- [Deepgram](https://deepgram.com/)
- [Streamlit](https://streamlit.io/)

## Contributions:

Contributions are welcome! Feel free to open issues, suggest improvements, or submit pull requests.

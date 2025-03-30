from dotenv import load_dotenv
import os
from transformers import pipeline
import requests
from google import genai
import streamlit as st
from PIL import Image
import io

# Load environment variables
load_dotenv()

# Get Hugging Face API key (if needed)
HF = os.getenv('HF')
google_api = os.getenv('google_api')

# Image-to-Text Function
def img2text(image):
    image_to_text = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
    result = image_to_text(image)
    text = result[0]['generated_text']
    return text

# Story Generation Function
def story_generate(scene,user_input):
    client = genai.Client(api_key=google_api)
    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents=f"Explain photo's features, aesthetic, and vibe in less than 300 words on {scene} to generate music on that and add notes on instruments which should be used and elements of sound which should be present. add according to {user_input}"
    )
    story = response.text
    return story

# Audio Generation Function
def audio_generate(message):
    API_URL = "https://router.huggingface.co/hf-inference/models/facebook/musicgen-small"
    headers = {"Authorization": f"Bearer {HF}"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.content

    audio_bytes = query({"inputs": message})
    return audio_bytes

# Main function
def main():
    st.title('Get Your Vibe')
    uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])
    user_input = st.text_input("Add enhancement")
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image)
        if st.button("Generate"):
            with st.spinner("Generating audio..."):
                prompt = img2text(image)
                story = story_generate(prompt,user_input)
                audio_bytes = audio_generate(story)
            # Save the audio to a file
            audio_file_path = "story_audio.wav"
            with open(audio_file_path, "wb") as audio_file:
                audio_file.write(audio_bytes)

            # Provide a play button for the audio
            st.audio(audio_file_path)

            # Add a download button for the audio
            st.download_button("Download Audio", data=audio_bytes, file_name='story_audio.wav', mime="audio/wav")
# Example Execution
if __name__ == "__main__":
    main()
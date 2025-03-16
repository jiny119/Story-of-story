import streamlit as st
from transformers import pipeline
from gtts import gTTS
from pydub import AudioSegment
import os

# Streamlit App Title
st.title("🎙️ Urdu Story Generator with Voiceover & Background Music")

# User Input: Story Title
story_title = st.text_input("Enter a Title for the Story (Urdu Allowed)")

if st.button("Generate Story"):
    if story_title:
        with st.spinner("Generating story... Please wait..."):
            # AI Story Generation
            generator = pipeline("text-generation", model="openai-community/gpt2")
            prompt = f"{story_title} - یہ کہانی اردو میں لکھی گئی ہے:"
            story = generator(prompt, max_length=5000, num_return_sequences=1)[0]["generated_text"]

            # Display Story Text
            st.subheader("Generated Story:")
            st.write(story)

            # Convert Story to Speech
            tts = gTTS(text=story, lang="ur")
            tts.save("story.mp3")

            # Add Background Music
            background_music = AudioSegment.from_file("background.mp3")  # Add a background.mp3 file
            voiceover = AudioSegment.from_file("story.mp3")

            # Adjust volume levels
            background_music = background_music - 20  # Lower background music volume
            final_audio = voiceover.overlay(background_music, loop=True)

            # Save Final Audio
            final_audio.export("final_story.mp3", format="mp3")

            # Play Audio
            st.subheader("Listen to the Story:")
            st.audio("final_story.mp3", format="audio/mp3")

            # Download Button for Audio
            with open("final_story.mp3", "rb") as file:
                btn = st.download_button(
                    label="Download Story Audio",
                    data=file,
                    file_name="urdu_story_with_music.mp3",
                    mime="audio/mp3"
                )
    else:
        st.warning("Please enter a title for the story!")

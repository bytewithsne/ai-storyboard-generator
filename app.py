import streamlit as st
from openai import OpenAI
import json

st.set_page_config(
    page_title="AI Storyboard Generator",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 AI Video Storyboard Generator")
st.write("Turn your video idea into a professional storyboard and AI video prompts.")

idea = st.text_area(
    "💡 Enter your video idea",
    placeholder="Example: A girl discovers a mysterious glowing forest at night.",
    height=120
)

col1, col2 = st.columns(2)

with col1:
    num_scenes = st.slider(
        "Number of scenes",
        min_value=3,
        max_value=10,
        value=5
    )

with col2:
    style = st.selectbox(
        "Video style",
        [
            "Cinematic",
            "Photorealistic",
            "3D Animation",
            "Anime",
            "Documentary",
            "Commercial"
        ]
    )

if st.button("🎬 Generate Storyboard", use_container_width=True):

    if not idea.strip():
        st.warning("Please enter a video idea first.")
        st.stop()

    try:
        client = OpenAI()

        prompt = f"""
You are an expert film director and AI video prompt engineer.

Create a professional storyboard for this video idea:

{idea}

Video style:
{style}

Create exactly {num_scenes} scenes.

For every scene provide:
- scene_number
- title
- duration
- shot_type
- camera_movement
- visual_description
- video_generation_prompt

The video generation prompt should be detailed and suitable for modern AI video generation models.

Return ONLY valid JSON in this exact structure:

{{
    "title": "Video title",
    "scenes": [
        {{
            "scene_number": 1,
            "title": "Scene title",
            "duration": "5 seconds",
            "shot_type": "Wide shot",
            "camera_movement": "Slow dolly forward",
            "visual_description": "Detailed description",
            "video_generation_prompt": "Detailed AI video prompt"
        }}
    ]
}}
"""

        with st.spinner("Creating your storyboard..."):

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

        result = json.loads(
            response.choices[0].message.content
        )

        st.success("Storyboard generated successfully!")

        st.header(result["title"])

        for scene in result["scenes"]:

            st.divider()

            st.subheader(
                f"🎬 Scene {scene['scene_number']}: {scene['title']}"
            )

            col1, col2 = st.columns(2)

            with col1:
                st.write(
                    f"**⏱ Duration:** {scene['duration']}"
                )
                st.write(
                    f"**📷 Shot:** {scene['shot_type']}"
                )

            with col2:
                st.write(
                    f"**🎥 Camera:** {scene['camera_movement']}"
                )

            st.write("### Visual Description")
            st.write(scene["visual_description"])

            st.write("### AI Video Prompt")
            st.code(
                scene["video_generation_prompt"],
                language="text"
            )

    except Exception as e:
        st.error("Something went wrong while generating the storyboard.")
        st.write(str(e))

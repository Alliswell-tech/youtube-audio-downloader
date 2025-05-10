import streamlit as st
from yt_dlp import YoutubeDL
import os

st.title("🎥 YouTube Video/Audio Downloader")

# Input: Paste one or more URLs
url = st.text_area("Paste YouTube URL(s), one per line")
urls = [line.strip() for line in url.splitlines() if line.strip()]

# Choose format
format_choice = st.selectbox("Select format to download", ("mp3/audio", "mp4/video"))

# Only show quality dropdown if MP4 is selected
selected_quality = None
if format_choice == "mp4/video":
    selected_quality = st.selectbox(
        "Select preferred video quality",
        ("1080p", "720p", "480p", "360p")
    )

if st.button("Download"):
    if not urls:
        st.warning("Please enter at least one YouTube URL.")
    else:
        # Set options based on format
        if format_choice == "mp3/audio":
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': '%(title)s.%(ext)s',
                'noplaylist': True,
                'quiet': False,
                'postprocessors': []
            }
        else:
            # Map selected quality to yt-dlp format string
            quality_map = {
                "1080p": "bestvideo[height>=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
                "720p": "bestvideo[height>=720][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
                "480p": "bestvideo[height>=480][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
                "360p": "bestvideo[height>=360][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]"
            }

            ydl_opts = {
                'format': quality_map[selected_quality],
                'outtmpl': '%(title)s.%(ext)s',
                'noplaylist': True,
                'quiet': False
            }

        downloaded_files = []

        with st.spinner("Downloading... Please wait. This may take some time."):
            with YoutubeDL(ydl_opts) as ydl:
                for url in urls:
                    try:
                        info = ydl.extract_info(url, download=True)
                        filename = ydl.prepare_filename(info)
                        downloaded_files.append(filename)
                    except Exception as e:
                        st.error(f"Error downloading {url}: {e}")

        st.success("✅ Download complete!")

        # Show download buttons
        for file in downloaded_files:
            with open(file, "rb") as f:
                st.download_button(
                    label=f"⬇️ Save '{file}' to Device",
                    data=f,
                    file_name=file,
                    mime="audio/mp3" if format_choice == "mp3/audio" else "video/mp4"
                )
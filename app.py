import streamlit as st
from yt_dlp import YoutubeDL
import os

st.title("🎥 YouTube Video/Audio Downloader")

# Input: Paste one or more URLs
url = st.text_area("Paste YouTube URL(s), one per line")
urls = [line.strip() for line in url.splitlines() if line.strip()]

# Choose format
format_choice = st.selectbox("Select format to download", ("mp3/audio", "mp4/video"))

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
            ydl_opts = {
                'format': 'mp4',
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
                    label=f"⬇️ Download {file}",
                    data=f,
                    file_name=file,
                    mime="audio/mp3" if format_choice == "mp3/audio" else "video/mp4"
                )
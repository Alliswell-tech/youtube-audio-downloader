import streamlit as st
from yt_dlp import YoutubeDL
import os

st.title("🎵 YouTube Audio Downloader")

count = st.number_input("How many songs?", min_value=1, step=1)

urls = []
for i in range(count):
    url = st.text_input(f"Enter Link {i+1}")
    if url:
        urls.append(url)

if st.button("Download"):
    if len(urls) != count:
        st.warning("Please fill all the URLs.")
    else:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'noplaylist': True,
            'quiet': False,
            'postprocessors': []  # No ffmpeg
        }

        with st.spinner("Downloading... Please wait. This may take some time."):
            with YoutubeDL(ydl_opts) as ydl:
                for url in urls:
                    try:
                        ydl.download([url])
                    except Exception as e:
                        st.error(f"Error downloading {url}: {e}")

        st.success("✅ Download complete!")

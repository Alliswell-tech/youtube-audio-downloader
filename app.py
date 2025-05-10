import streamlit as st
from yt_dlp import YoutubeDL
import os

st.title("🎵 YouTube Audio Downloader")

# Input for number of songs
count = st.number_input("How many YouTube audio downloads?", min_value=1, step=1)

urls = []
for i in range(1, count + 1):
    url = st.text_input(f"Enter Link {i}")
    if url:
        urls.append(url)

if st.button("Download All"):
    if len(urls) != count:
        st.warning("Please fill all the URLs.")
    else:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'noplaylist': True,
            'quiet': False,
            'postprocessors': []
        }

        with st.spinner("Downloading... Please wait. This may take some time."):
            with YoutubeDL(ydl_opts) as ydl:
                for url in urls:
                    try:
                        ydl.download([url])
                    except Exception as e:
                        st.error(f"Error downloading {url}: {e}")

        st.success("Download complete!")
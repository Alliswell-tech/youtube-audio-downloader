import streamlit as st
from yt_dlp import YoutubeDL
import os

st.title("🎥 YouTube Video/Audio Downloader")

# Input: Paste one or more URLs
url = st.text_area("Paste YouTube URL(s), one per line")
urls = [line.strip() for line in url.splitlines() if line.strip()]

# Choose format
format_choice = st.selectbox("Select format to download", ("mp3/audio", "mp4/video"))

# Store selected resolutions per URL
selected_resolutions = {}

if urls and format_choice == "mp4/video":
    st.subheader("Select Resolution for Each Video:")
    with st.spinner("Fetching available resolutions..."):
        for idx, url in enumerate(urls):
            ydl_opts = {
                'quiet': True,
                'noplaylist': True,
            }
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])
                
                # Extract available resolutions
                res_options = set()
                for f in formats:
                    res = f.get('resolution')
                    if res and 'x' in res:
                        height = res.split('x')[1]
                        res_options.add(height + "p")
                res_options = sorted(list(res_options), key=lambda x: int(x.replace('p', '')))

                if not res_options:
                    res_options = ["best", "worst"]

                # Let user select resolution
                selected = st.selectbox(f"Resolution for video {idx+1}: {info['title']}", res_options, key=f"res_{idx}")
                selected_resolutions[url] = selected

if st.button("Download"):
    if not urls:
        st.warning("Please enter at least one YouTube URL.")
    else:
        downloaded_files = []

        with st.spinner("Downloading... Please wait. This may take some time."):
            for url in urls:
                if format_choice == "mp3/audio":
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': '%(title)s.%(ext)s',
                        'noplaylist': True,
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                    }
                else:
                    selected_resolution = selected_resolutions.get(url, "best")
                    if selected_resolution == "best":
                        video_format = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]"
                    elif selected_resolution == "worst":
                        video_format = "worstvideo[ext=mp4]+worstaudio[ext=m4a]/worst[ext=mp4]"
                    else:
                        height = selected_resolution.replace("p", "")
                        video_format = f"bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/best[height<={height}][ext=mp4]"

                    ydl_opts = {
                        'format': video_format,
                        'outtmpl': '%(title)s.%(ext)s',
                        'noplaylist': True,
                        'merge_output_format': 'mp4'
                    }

                try:
                    with YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        filename = ydl.prepare_filename(info)
                        final_file = filename.rsplit(".", 1)[0] + ".mp4"
                        downloaded_files.append(final_file)
                except Exception as e:
                    st.error(f"Error downloading {url}: {e}")

        st.success("✅ Download complete!")

        for file in downloaded_files:
            if os.path.exists(file):
                with open(file, "rb") as f:
                    mime_type = "audio/mp3" if format_choice == "mp3/audio" else "video/mp4"
                    st.download_button(
                        label=f"⬇️ Download {file}",
                        data=f,
                        file_name=file,
                        mime=mime_type
                    )
            else:
                st.error(f"File not found: {file}")
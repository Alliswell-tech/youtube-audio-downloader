import streamlit as st
from yt_dlp import YoutubeDL
import os

st.set_page_config(page_title="YouTube Downloader", layout="centered")
st.title("🎥 YouTube Video/Audio Downloader")

url = st.text_area("📥 Paste YouTube URL(s), one per line")
urls = [line.strip() for line in url.splitlines() if line.strip()]

format_choice = st.selectbox("🎞️ Select format to download", ("mp3/audio", "mp4/video"))

# Dict to store selected format_id per URL
selected_format_ids = {}

if urls and format_choice == "mp4/video":
    st.subheader("🎯 Choose Quality for Each Video:")
    with st.spinner("Fetching available formats..."):
        for idx, url in enumerate(urls):
            try:
                ydl_opts = {
                    'quiet': True,
                    'skip_download': True,
                    'noplaylist': True,
                }
                with YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    st.markdown(f"**{info.get('title', 'Unknown Video')}**")

                    formats = info.get('formats', [])
                    video_options = []

                    for f in formats:
                        if f.get('vcodec', 'none') != 'none' and f.get('ext') == 'mp4':
                            res = f.get('format_note') or f.get('resolution') or f.get('height')
                            size = f.get('filesize') or f.get('filesize_approx') or 0
                            size_mb = round(size / (1024 * 1024), 2) if size else "?"
                            label = f"{res} | {size_mb} MB | {f['format_id']}"
                            video_options.append((label, f['format_id']))

                    if video_options:
                        option_labels = [v[0] for v in video_options]
                        default_format = st.selectbox(
                            f"Select quality for video {idx+1}:", option_labels, key=f"format_{idx}"
                        )
                        selected_format_ids[url] = dict(video_options)[default_format]
                    else:
                        st.warning("No suitable MP4 formats found.")

            except Exception as e:
                st.error(f"Failed to fetch info for {url}: {e}")

# Download handler
if st.button("⬇️ Download"):
    if not urls:
        st.warning("Please enter at least one YouTube URL.")
    else:
        downloaded_files = []
        with st.spinner("Downloading... Please wait."):
            for url in urls:
                try:
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
                        format_id = selected_format_ids.get(url)
                        ydl_opts = {
                            'format': format_id + '+bestaudio[ext=m4a]/' + format_id,
                            'outtmpl': '%(title)s.%(ext)s',
                            'noplaylist': True,
                            'merge_output_format': 'mp4',
                        }

                    with YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        filename = ydl.prepare_filename(info)
                        final_ext = "mp3" if format_choice == "mp3/audio" else "mp4"
                        final_file = filename.rsplit(".", 1)[0] + f".{final_ext}"
                        downloaded_files.append(final_file)

                except Exception as e:
                    st.error(f"❌ Error downloading {url}: {e}")

        st.success("✅ All downloads completed!")

        for file in downloaded_files:
            if os.path.exists(file):
                with open(file, "rb") as f:
                    mime = "audio/mp3" if format_choice == "mp3/audio" else "video/mp4"
                    st.download_button(
                        label=f"📥 Download {os.path.basename(file)}",
                        data=f,
                        file_name=os.path.basename(file),
                        mime=mime
                    )
            else:
                st.error(f"File not found: {file}")

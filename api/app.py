from flask import Flask, request, redirect, send_from_directory, render_template_string , render_template
# import yt_dlp
import os
COUNT = 0
app = Flask(__name__)

def VIdeo_download(URL):
    video_url = URL
    global COUNT
    custom_name = f'Your_youtube_video{COUNT}'
    save_path = f"./static/videos/{custom_name}.%(ext)s"
    ydl_opts = {
    'format': 'best',  # Automatically select the best available format
    'outtmpl': save_path,  # Save to specified folder with title as filename
}
    video_title = None
    video_ext = None
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video info without downloading
            info_dict = ydl.extract_info(video_url, download=False)
            video_title = info_dict.get('title', None)
            video_ext = info_dict.get('ext', 'mp4')
            if video_title:
                print(f"Video title: {video_title, video_ext}")
            else:
                print("Could not get video title.")
            # Now download the video
            ydl.download([video_url])
        print("Download completed!")
        COUNT += 1

    except Exception as e:
        print(f"An error occurred: {e}")
    return custom_name , video_ext
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['video_url']
        video_title, video_ext = VIdeo_download(name)
        if video_title:
            return render_template("video_downloader.html", video_title=video_title, video_ext=video_ext)
    return render_template("video_downloader.html", video_title='')


if __name__ == '__main__':
    app.run(port=5000)

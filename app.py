from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# Function to download YouTube video using yt-dlp
def download_youtube_video(url, quality="best"):
    try:
        ydl_opts = {
            'format': quality,
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save in downloads folder
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', None)
        return video_title
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the form submission
@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['url']
    quality = request.form['quality']
    
    if not video_url:
        return "Error: No URL provided."
    
    # Download the video
    video_title = download_youtube_video(video_url, quality)
    
    if video_title:
        # Path to the downloaded video
        video_path = os.path.join('downloads', f"{video_title}.mp4")
        return send_file(video_path, as_attachment=True)  # Download the file from server
    else:
        return "Error downloading the video."

if __name__ == "__main__":
    # Create downloads directory if not exists
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)

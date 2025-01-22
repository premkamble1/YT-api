from flask import Flask, request, jsonify
import yt_dlp

# Initialize Flask app
app = Flask(__name__)  # Corrected from _name_ to __name__

# Function to get audio URL for a given YouTube URL
def get_audio_urls(youtube_url):
    ydl_opts = {
        'format': 'bestaudio/best',  # Get the best audio quality
        'extractaudio': True,        # Extract audio only
        'audioquality': 1,           # Best audio quality
        'outtmpl': 'downloads/%(id)s.%(ext)s',  # Download location (optional)
        'quiet': True                # Suppress the console output
    }

    try:
        # Initialize yt-dlp with the options
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)
            # Check if it's a playlist
            if 'entries' in info_dict:
                audio_urls = []
                for video in info_dict['entries']:
                    if video:
                        audio_urls.append({'video_id': video.get('id'), 'audio_url': video.get('url')})
                return {'audio_urls': audio_urls}
            else:
                # Single video case
                return {'audio_url': info_dict.get('url')}
    
    except Exception as e:
        return {'error': str(e)}  # Return the error message

# API route to handle the request
@app.route('/extract-audio', methods=['GET'])
def extract_audio():
    youtube_url = request.args.get('url')  # Get YouTube URL from query string
    
    if not youtube_url:  # Check if the URL was provided
        return jsonify({'error': 'YouTube URL is required'}), 400
    
    # Call function to get the audio URLs
    audio_details = get_audio_urls(youtube_url)
    
    return jsonify(audio_details)  # Return the audio URLs (or error message)

if __name__ == '__main__':  # Corrected from _name_ to __name__
    app.run(debug=True)

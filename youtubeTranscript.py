from youtube_transcript_api import YouTubeTranscriptApi
import argparse
import re

def get_youtube_transcript(video_url):

    video_id_match = re.match(r'^https?://(?:www\.)?youtube\.com/watch\?v=([^&]+)', video_url)
    if not video_id_match:
        print("Invalid YouTube URL. Please provide a valid YouTube video URL.")
        return None

    video_id = video_id_match.group(1)

    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = ""

        for transcript in transcript_list:
            tscript_time = float(transcript['start']) + float(transcript['duration'])
            transcript_text += f"[{transcript['start']} - {round(tscript_time, 2)}] " + transcript['text'] + '\n'
            # transcript_text += transcript['text'].strip() + ' '

        # Accuracy of timestamp is dependent on the package model. End time is calculated based on the duration!
        return transcript_text

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch transcript of a YouTube video')
    parser.add_argument('video_url', type=str, help='URL of the YouTube video')
    args = parser.parse_args()

    video_url = args.video_url
    transcript = get_youtube_transcript(video_url)

    if transcript:
        print("Transcript:")
        print(transcript)

# python youtubeTranscript.py "https://www.youtube.com/watch?v=l-nM0EbpkpM"
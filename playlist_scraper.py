


from youtube_transcript_api import YouTubeTranscriptApi
import os
import json
from pytube import Playlist, Channel
import requests
from bs4 import BeautifulSoup

def _sanitize_filename(filename: str) -> str:
        # Remove any characters that are not alphanumeric, space, or underscores
        return "".join(c if c.isalnum() or c in (' ', '_') else "_" for c in filename).strip()

def transcript_scraper_tool(playlist_url: str, output_dir: str = 'transcripts'):
    """takes a playlist url and iterates through the videos within, scraping each video's transcript and saving to the transcripts directory"""
    print("Starting transcript scraping...")

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    try:
        # Get the playlist object
        playlist = Playlist(playlist_url)
    except Exception as e:
        print(f"Error fetching playlist: {e}")
        return

    print(f"Found {len(playlist.video_urls)} videos in the playlist.")

    # Iterate through each video in the playlist
    for video in playlist.videos:
        video_id = video.video_id
        print(f"Processing video: {video.title} (ID: {video_id})")

        try:
            # Fetch the transcript for the video
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = " ".join([entry['text'] for entry in transcript])

            # Save the transcript to a file named after the video title
            safe_title = _sanitize_filename(video.title)
            file_path = os.path.join(output_dir, f"{safe_title}.json")

            with open(file_path, 'w') as f:
                json.dump({"title": video.title, "transcript": transcript_text}, f, indent=4)

            print(f"Successfully fetched and saved transcript for: {video.title}")

        except Exception as e:
            print(f"Could not fetch transcript for: {video.title} due to {str(e)}")


if __name__ == "__main__":
    #  Anthony Chaffee ama playlist
    # url = "https://www.youtube.com/watch?v=dVo6BqWbe3c&list=PLkkRSboRx_u0Z8LshnDXVb8GUQeNFGULW&index=1"
    #  Anthony Chaffee carnivore_diet_for_beginners playlist
    url = "https://www.youtube.com/playlist?list=PLkkRSboRx_u2ymm3qL2PvUiwSa8KWvmk7"

    transcript_scraper_tool(playlist_url=url, output_dir="carnivore_diet_for_beginners")


    
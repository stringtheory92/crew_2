# from crewai_tools import BaseTool
# from pytube import Playlist
# from youtube_transcript_api import YouTubeTranscriptApi
# import json
# import os

# class YouTubeTranscriptScraperTool(BaseTool):
#     def __init__(self, playlist_url, output_dir='transcripts'):
#         self.playlist_url = playlist_url
#         self.transcripts = []
#         self.output_dir = output_dir

#         # Create output directory if it doesn't exist
#         if not os.path.exists(self.output_dir):
#             os.makedirs(self.output_dir)

#     def scrape_transcripts(self):
#         # Get the playlist object
#         playlist = Playlist(self.playlist_url)

#         # Iterate through each video in the playlist
#         for video in playlist.videos:
#             video_id = video.video_id

#             try:
#                 # Fetch the transcript for the video
#                 transcript = YouTubeTranscriptApi.get_transcript(video_id)
#                 transcript_text = " ".join([entry['text'] for entry in transcript])

#                 # Add the transcript text to the transcripts list
#                 self.transcripts.append({
#                     'title': video.title,
#                     'url': video.watch_url,
#                     'transcript': transcript_text
#                 })

#                 # Save the transcript to a file named after the video title
#                 self.save_transcript_to_file(video.title, transcript_text)

#                 print(f"Successfully fetched transcript for: {video.title}")

#             except Exception as e:
#                 print(f"Could not fetch transcript for: {video.title} due to {str(e)}")

#     def save_transcript_to_file(self, title, transcript_text):
#         # Create a safe file name from the video title
#         safe_title = self._sanitize_filename(title)
#         file_path = os.path.join(self.output_dir, f"{safe_title}.json")

#         with open(file_path, 'w') as f:
#             json.dump({"title": title, "transcript": transcript_text}, f, indent=4)

#         print(f"Transcript saved to {file_path}")

#     def _sanitize_filename(self, filename):
#         # Remove any characters that are not alphanumeric, space, or underscores
#         return "".join(c if c.isalnum() or c in (' ', '_') else "_" for c in filename).strip()
    
#     def _run(self, **kwargs):
#         # This method is required by the BaseTool and will be called when the tool is executed
#         self.playlist_url = kwargs.get('playlist_url', self.playlist_url)
#         self.output_dir = kwargs.get('output_dir', self.output_dir)

#         # Ensure necessary arguments are provided
#         if not self.playlist_url:
#             raise ValueError("Playlist URL is required for scraping transcripts.")
        
#         # Call the method to scrape transcripts
#         self.scrape_transcripts()

# Example usage:
# scraper = YouTubeTranscriptScraper('https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID')
# scraper.scrape_transcripts()


# if __name__ == "__main__":
#     tool = GetArticleLinkTool()
#     print(tool._run())








from crewai_tools import BaseTool
from pytube import Playlist
from youtube_transcript_api import YouTubeTranscriptApi
import json
import os
from pydantic import Field

from crewai_tools import BaseTool
from pytube import Playlist
from youtube_transcript_api import YouTubeTranscriptApi
import json
import os
from pydantic import Field

class YouTubeTranscriptScraperTool(BaseTool):
    # name: str = Field("YouTube Transcript Scraper", description="Tool to scrape YouTube video transcripts from a playlist.")
    # description: str = Field("Scrapes transcripts for all videos in a specified YouTube playlist.", description="Description of the tool's functionality.")
    # playlist_url: str = Field(..., description="URL of the YouTube playlist to scrape transcripts from.")
    # output_dir: str = Field(default='transcripts', description="Directory where transcripts will be saved.")
    # transcripts: list = Field(default_factory=list, description="List to store transcripts.")



    name: str = "YouTube Transcript Scraper"
    description: str = "Scrapes transcripts for all videos in a specified YouTube playlist."
    playlist_url: str = Field(..., description="URL of the YouTube playlist to scrape transcripts from.")
    output_dir: str = Field(default='transcripts', description="Directory where transcripts will be saved.")
    transcripts: list = Field(default_factory=list, description="List to store transcripts.")
   

    class Config:
        arbitrary_types_allowed = True
    
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     print("init!")
    #     # Create output directory if it doesn't exist
    #     if not os.path.exists(self.output_dir):
    #         os.makedirs(self.output_dir)

    def scrape_transcripts(self):
        print(f"Starting to scrape transcripts from playlist: {self.playlist_url}")

        # Get the playlist object
        try:
            playlist = Playlist(self.playlist_url)
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

                # Add the transcript text to the transcripts list
                self.transcripts.append({
                    'title': video.title,
                    'url': video.watch_url,
                    'transcript': transcript_text
                })

                # Save the transcript to a file named after the video title
                self.save_transcript_to_file(video.title, transcript_text)

                print(f"Successfully fetched and saved transcript for: {video.title}")

            except Exception as e:
                print(f"Could not fetch transcript for: {video.title} due to {str(e)}")

    # def scrape_transcripts(self):
    #     # Get the playlist object
    #     playlist = Playlist(self.playlist_url)

    #     # Iterate through each video in the playlist
    #     for video in playlist.videos:
    #         video_id = video.video_id

    #         try:
    #             # Fetch the transcript for the video
    #             transcript = YouTubeTranscriptApi.get_transcript(video_id)
    #             transcript_text = " ".join([entry['text'] for entry in transcript])

    #             # Add the transcript text to the transcripts list
    #             self.transcripts.append({
    #                 'title': video.title,
    #                 'url': video.watch_url,
    #                 'transcript': transcript_text
    #             })

    #             # Save the transcript to a file named after the video title
    #             self.save_transcript_to_file(video.title, transcript_text)

    #             print(f"Successfully fetched transcript for: {video.title}")

    #         except Exception as e:
    #             print(f"Could not fetch transcript for: {video.title} due to {str(e)}")

    def save_transcript_to_file(self, title, transcript_text):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        # Create a safe file name from the video title
        safe_title = self._sanitize_filename(title)
        file_path = os.path.join(self.output_dir, f"{safe_title}.json")

        with open(file_path, 'w') as f:
            json.dump({"title": title, "transcript": transcript_text}, f, indent=4)

        print(f"Transcript saved to {file_path}")

    def _sanitize_filename(self, filename):
        # Remove any characters that are not alphanumeric, space, or underscores
        return "".join(c if c.isalnum() or c in (' ', '_') else "_" for c in filename).strip()
    
    def _run(self, **kwargs):
        print('running...')
        # This method is required by the BaseTool and will be called when the tool is executed
        self.playlist_url = kwargs.get('playlist_url', self.playlist_url)
        self.output_dir = kwargs.get('output_dir', self.output_dir)

        # Ensure necessary arguments are provided
        if not self.playlist_url:
            raise ValueError("Playlist URL is required for scraping transcripts.")
        
        # Call the method to scrape transcripts
        self.scrape_transcripts()

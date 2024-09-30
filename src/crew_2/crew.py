from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool, tool
# from .tools.custom_tool import YouTubeTranscriptScraperTool
from langchain_anthropic import ChatAnthropic
from youtube_transcript_api import YouTubeTranscriptApi
import os
import json

# from .tools.custom_tool import GetUnanalyzedArticleLinksTool

# https://github.com/alejandro-ao/exa-crewai/blob/master/src/newsletter_gen/config/tasks.yaml
# website_search_tool = WebsiteSearchTool()
# get_unanalyzed_article_links_tool = GetUnanalyzedArticleLinksTool()

haiku = "claude-3-haiku-20240307"
Consistent = ChatAnthropic(
    temperature=0.0,
    model=haiku
)
url = 'https://www.youtube.com/playlist?list=PLkkRSboRx_u0Z8LshnDXVb8GUQeNFGULW'
# transcript_scraper_tool = YouTubeTranscriptScraperTool(playlist_url=url, output_dir='transcripts')
web_scraper_tool = ScrapeWebsiteTool(website_url=url)

@tool("transcript_scraper_tool")
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


def _sanitize_filename(filename: str) -> str:
    # Remove any characters that are not alphanumeric, space, or underscores
    return "".join(c if c.isalnum() or c in (' ', '_') else "_" for c in filename).strip()

@tool("Save Logs Tool")
def save_logs(logs: str, filename: str = None):
    """Saves the agent's thoughts and logs into a file in the logs directory."""
    # Ensure the logs directory exists
    logs_dir = 'logs'
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Use a default filename if none is provided
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"logs_{timestamp}.txt"

    file_path = os.path.join(logs_dir, filename)

    # Save the logs to the file
    with open(file_path, 'a') as log_file:
        log_file.write(logs + '\n')

    print(f"Logs saved to {file_path}")



scraper_agent = Agent(
    role="Transcript Scraper",
    goal="Try to use the transcript scraper tool to scrape the transcripts from each video within a youtube playlist url. If that tool doesn't work, systematically navigate to each video in the playlist and use the web_scraper_tool to extract the transcript from the page and manually save each transcript to the transcript directory, using the video's title as the name of the file",
    backstory="You are a master at scraping the transcripts from each video in the playlist at a provided url. You know that the transcript_scraper_tool is likely the best for the job, but are also capable of systematically navigating to each video in the playlist and using the web_scraper_tool to perform this task. Do not perform any other actions, or generate any other text.",
    verbose=True,
    allow_delegations=False,
    tools=[transcript_scraper_tool, web_scraper_tool, save_logs],
    llm=Consistent
)


scrape_task = Task(
    description=f"""Try to use the transcript scraper tool to scrape the transcripts from each video within a youtube playlist url. Log the entire processes using your tools
    url: {url}
    If that tool doesn't work, systematically navigate to each video in the playlist and use the web_scraper_tool to extract the 
    transcript from the page and manually save each transcript to the transcript directory, using the video's title as the name of the file. 
    DO NOT PERFORM ANY OTHER TASK OR GENERATE ADDITIONAL TEXT OR FILES""",
    expected_output='A series of transcript files in the transcripts directory',
    agent=scraper_agent,
)


crew = Crew(
    agents=[scraper_agent],
    tasks=[scrape_task],
    verbose=True
)

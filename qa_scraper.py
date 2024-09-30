import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from youtube_transcript_api import YouTubeTranscriptApi
from loguru import logger

# Global list of keywords/phrases to avoid downloading certain videos
DO_NOT_DOWNLOAD = ["Ketogenic Woman", 
                   "Carnivore Diet Weekly Group Live Q&A! | July 22, 2023", 
                   "Challenging the Carnivore Diet Q&A | Anthony Chaffee,MD", 
                   "Carnivore Diet Weekly Live Q&A! | July 8, 2023",
                   "Can You Get Scurvy on a Carnivore Diet? Dr Berry Explains.",
                   "Hanging With The Browns Q&A! | Dr Anthony Chaffee",
                   "Bread and Circuses for the Masses, Not the Masters",
                   "Live Chat with Dr Anthony Chaffee, Shawn White, Dave Mac, and Kipp BBQ!",
                   "30 day Carnivore Challenge Live Zoom call!",
                   "KetoCon Carnivore Panel with Dr Anthony Chaffee, Dr Shawn Baker, Nutrition with Judy, and more!",
                   "Hard Facts on How Diet and Nutrition Affect Your Health | Dr Ken Berry",
                   "EPIC Talk About All Things Health and Carnivore with Dr Paul Mason, MD!",
                   "Special Guest Interview with Dr Shawn Baker, MD!",
                   "The Big Fat Surprise! With Author Nina Teicholz | Ep 77",
                   "The Blue Zones: What They REALLY Eat! | Professor Bill Schindler",
                   "The Great Plant Based Con! | Jayne Buxton | Plant Free MD Ep 146",
                   "Dr Chaffee Clips",
                   "Debunking Carnivore Diet Myths! Live Challenge Q's from the Audience!",
                   "Dr Gary Fettke - Exposing Big Food: A Surgeon's Bold Revelations",
                   "10+ year Carnivore, mother, coach, and creator Kelly Hogan!",
                   "Treating Cancer & Autoimmune w/a Proper Human Diet | Dr Zsófia Clemens",
                   "Plant Based Doctor Turns Carnivore!",
                   "Clip from my recent talk with my good friend Dr Pran Yoganathan, a Consultant Gastroenterologist",
                   "Rancher and Carnivore for OVER 65 Years! (You Won't Believe Her Age!) | Rancher Maggie",
                   "Special Guest Interview with Bella Steak and Butter Gal!",
                   "Transform Your Health! Uncover The Truth About Visceral Fat | Ep 132",
                   "Is Ketosis Harmful To You? Here's The Evidence | PFMD 149",
                   "Controlling Type 1 Diabetes with Diet! | Tomer Pappe",
                   "The Science Behind Shredding Fat & Building Muscle | Richard Smith",
                   "Can You Reverse Schizophrenia? Harvard Professor Says You Can!",
                   "You Don't Need Carbs to Build Muscle! With Pro Bodybuilder Robert Sykes, the Keto Savage!",
                   "PCOS, fertility, and women's health. There is something you can do without medications!",
                   "The Hard Facts on Animal Nutrition and Agriculture | Peter Ballerstedt, PhD",
                   "The Carnivore Diet: A Game Changer for All-American Decathlete Ryan Talbot",
                   "Incredible Carnivore Diet Success Story! | Jess Randle",
                   "Carnivore Diet: Fighting Glioblastoma with Food | Ep 138",
                   "Helping 1 BILLION People Live Healthier Lives, with Ben Azadi!",
                   "The Problem with Modern Diet and Health, and How to Fix It!",
                   "Visceral Fat is Blocking Your Optimal Health, with Dr Sean O'Mara!",
                   "Building Muscle in Your 40's and Tackling Mental Health & Addiction",
                   "Special Guest Interview with a PhD in Exercise Physiology and Nutrition, Dr Sarah Zaldivar!",
                   "Antonio Sabato Jr Only Eats Meat for His Health!",
                   "Myth Busting the Food Lies of the Past 60 Years with Brian Sanders!",
                   "Dr Anthony Chaffee LIVE!",
                   "🔴He Only Ate Meat For 1 Year and This Is What Happened! Shawn White",
                   "🔴Overcoming Autoimmune Disease | Phil Escott | PFMD Ep 154",
                   "NCAA Div 1 All-American Decathlete and Big Ten Champion Ryan Talbot",
                   "The Great Plant Based Con Book Club with author Jayne Buxton!",
                   "From Vegan to Carnivore: Rory Bland's Remarkable Health Transformation",
                   "What Is The REAL Cause of Heart Disease | Dr Stephen Hussey | Ep 93",
                   "Mental Health with Clinical Psychotherapist Natalie E West",
                   "Optimizing Mental Health with Dr. Georgia Ede, Dr. Tony Hampton and Dr. Anthony Chaffee and more!",
                   "How to Optimize Metabolic Health, with Dr Tony Hampton",
                   "🔴Omega-6 Apocalypse: Vegetable Oils, Obesity, and Chronic Disease",
                   "Carnivore Bodybuilding with Jonathan Griffiths!",
                   "Reversing Crohn's Disease with the Carnivore Diet!",
                   "Recovering From Major Depression | Brett Lloyd",
                   "Carnivore Brain Cancer Survivor Pablo Kelly!",
                   "Regenerative Rancher Reveals Why GRASS-FED Beef Is Better | Amy Hay",
                   "Stay Jacked at 58 with 20+ Year Carnivore Michael Mason!",
                   "🔴Natural Living, Carnivore Diets, Grounding, and Circadian Rhythm",
                   "Kerry Mann Jr.",
                   "Health and Fitness with Casey Ruff!",
                    "Dr Anthony Chaffee on the Red Pill Buddhas Podcast with Phil Escott!",
                    "Special Guest interview w/Vinnie Tortrich maker of of Fat: A Documentary 1&2, and Beyond Impossible!",
                    "Is the Carnivore Diet the Future of Nutrition in 2024? | Jon Chavez",
                    "1 Million Strong for Cancer: Metabolic Therapy MISSION- with Jeff D & Kerry Mann!",
                    "What Humans ACTUALLY Evolved to Eat! | Dr Miki Ben-Dor, Ep 76",
                    "Hollywood goes Carnivore! Interview with Hollywood Actor and Calvin Klein Model Antonio Sabato Jr!",
                    "From Vegan and Dying, to Carnivore and Thriving!",
                    "Optimal Diet for Gut Health with Gastroenterologist Dr Pran Yoganathan",
                    "The Secret Diet of AFL Star Tom McDonald!",
                    "🔴Tara and Natalie Dropping Truth Bombs on the Agriculture Industry!",
                    "How To Carnivore Ep 25: Return of Dr John Jaquish!",
                    "🔴Transform Your Life with Martin Silva | Lean Muscle & Optimal Health",
                    "Let the Troops Eat Meat!",
                    "Physicist Turns To Carnivore Diet And This Happens... | Ally Houston",
                    "Reversing Diabetes with Diet Alone!",
                    "Special Guest Interview with Lillie Kane on The Plant Free MD Podcast!",
                    "Benefits of variable resistance training with Dr John Jaquish of the X3 Bar #shorts #short #fyp",
                    "Get Healthy & Lose Weight w/Carnivore Cookbook Author Craig Emmerich!",
                    "🔴Lioness Lifestyle Live with Dr Anthony Chaffee!",
                    "🔴CARNIVORE Success Story: From Orphan to Entrepreneur | Ep 140",
                    "Just Because You're Slim Doesn't Mean You're Healthy! #shorts #short #shortvideo",
                    "New interviews and CME with Dr Tony Hampton! #shorts #short #fyp",
                    "Metabolic Health and Anti-Aging w/Special Guest Dr Sarah Zalvidar!",
                    "My Interviews on Other Channels",
                    "🔴From Wheelchair to Walking: How Dr. Sarah Conquered Multiple Sclerosis (MS) With Her Diet!",
                    "Interviews on My Channel",
                    "New interview with return guest Dr Pran Yoganathan! #shorts #short #fyp #nutrition #cancer"
                   ]

# Setup Chrome options for headless mode
chrome_options = Options()
chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"  # Adjust this if necessary
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Path to the ChromeDriver (Ensure you have the correct path)
chrome_service = Service("./chromedriver")

# YouTube search results URL (Anthony Chaffee - Q&A search)
channel_url = "https://www.youtube.com/@anthonychaffeemd/search?query=q%26a"

# Output directory for transcripts
output_dir = "q&a_transcripts"

def _sanitize_filename(filename: str) -> str:
    """Sanitizes a string to create a valid filename."""
    return "".join(c if c.isalnum() or c in (' ', '_') else "_" for c in filename).strip()

def should_download_video(title: str, do_not_download_list: list) -> bool:
    """Determines whether a video should be downloaded based on the title."""
    for keyword in do_not_download_list:
        if keyword.lower() in title.lower():
            return False
    return True

def get_video_ids_and_titles_from_search(channel_url):
    """Scrapes video IDs and titles from the YouTube search results page using Selenium."""
    video_data = []
    
    # Start the WebDriver with the specified options and service
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    
    try:
        # Navigate to the search URL
        driver.get(channel_url)
        
        # Wait until the video elements under the div with id "contents" are present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "contents"))
        )
        
        # Give some time for the JavaScript to load all videos
        time.sleep(5)
        
        logger.debug("Successfully loaded the search page with Selenium.")

        # Find all video links inside the div with id 'contents'
        contents_div = driver.find_element(By.ID, "contents")
        video_elements = contents_div.find_elements(By.TAG_NAME, 'a')
        
        for video in video_elements:
            href = video.get_attribute('href')
            title = video.get_attribute('title')  # Extract the video title
            if href and '/watch?v=' in href:
                video_id = href.split('=')[1]
                if title:  # Only process videos that have a title
                    video_data.append({"id": video_id, "title": title})
        logger.info(f"Found {len(video_data)} videos on the search page.")
    
    except Exception as e:
        logger.error(f"Error retrieving video data: {e}")
    
    finally:
        # Always close the driver at the end
        driver.quit()

    return video_data  # Return list of video data (id and title)

def fetch_transcript(video_id):
    """Fetches transcript for a video using youtube_transcript_api."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        logger.debug(f"Transcript fetched for video ID {video_id}.")
        return " ".join([item['text'] for item in transcript])
    except Exception as e:
        logger.error(f"Could not fetch transcript for video {video_id}: {e}")
        return ""

def save_transcript(video_title, transcript_text):
    """Saves transcript to the specified directory."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    safe_title = _sanitize_filename(video_title)
    file_path = os.path.join(output_dir, f"{safe_title}.json")
    
    with open(file_path, 'w') as f:
        json.dump({"title": video_title, "transcript": transcript_text}, f, indent=4)
    logger.info(f"Transcript saved for: {video_title}")

def main():
    # Step 1: Get all video IDs and titles from the search results page
    videos = get_video_ids_and_titles_from_search(channel_url)
    
    # Step 2: For each video, fetch the transcript and save it if allowed by DO_NOT_DOWNLOAD
    for video in videos:
        video_id = video['id']
        video_title = video['title']
        
        # Check if this video should be skipped based on the title
        if not should_download_video(video_title, DO_NOT_DOWNLOAD):
            logger.info(f"Skipping video '{video_title}' because it matches DO_NOT_DOWNLOAD.")
            continue
        
        logger.info(f"Processing video ID: {video_id} with title: {video_title}")
        
        # Fetch the transcript and save it if it's available
        transcript = fetch_transcript(video_id)
        if transcript:
            save_transcript(video_title, transcript)
    
    logger.info("Script finished.")

if __name__ == "__main__":
    main()



# import os
# import json
# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from youtube_transcript_api import YouTubeTranscriptApi
# from loguru import logger

# chrome_options = Options()
# chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")

# chrome_service = Service("./chromedriver")


# # YouTube search results URL (Anthony Chaffee - Q&A search)
# channel_url = "https://www.youtube.com/@anthonychaffeemd/search?query=q%26a"

# # Output directory for transcripts
# output_dir = "q&a_transcripts"


# def _sanitize_filename(filename: str) -> str:
#     """Sanitizes a string to create a valid filename."""
#     return "".join(c if c.isalnum() or c in (' ', '_') else "_" for c in filename).strip()

# def get_video_ids_from_search(channel_url):
#     """Scrapes video IDs from the YouTube search results page using Selenium."""
#     video_ids = []
    
#     # Start the WebDriver with the specified options and service
#     driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    
#     try:
#         # Navigate to the search URL
#         driver.get(channel_url)
        
#         # Wait until the video elements under the div with id "contents" are present
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.ID, "contents"))
#         )
        
#         # Give some time for the JavaScript to load all videos
#         time.sleep(5)
        
#         logger.debug("Successfully loaded the search page with Selenium.")

#         # Find all video links inside the div with id 'contents'
#         contents_div = driver.find_element(By.ID, "contents")
#         video_elements = contents_div.find_elements(By.TAG_NAME, 'a')
        
#         for video in video_elements:
#             href = video.get_attribute('href')
#             if href and '/watch?v=' in href:
#                 video_id = href.split('=')[1]
#                 if video_id not in video_ids:
#                     video_ids.append(video_id)
#         logger.info(f"Found {len(video_ids)} video IDs on the search page.")
    
#     except Exception as e:
#         logger.error(f"Error retrieving video IDs: {e}")
    
#     finally:
#         # Always close the driver at the end
#         driver.quit()

#     return list(set(video_ids))  # Return unique video IDs


# def fetch_transcript(video_id):
#     """Fetches transcript for a video using youtube_transcript_api."""
#     try:
#         transcript = YouTubeTranscriptApi.get_transcript(video_id)
#         logger.debug(f"Transcript fetched for video ID {video_id}.")
#         return " ".join([item['text'] for item in transcript])
#     except Exception as e:
#         logger.error(f"Could not fetch transcript for video {video_id}: {e}")
#         return ""

# def save_transcript(video_title, transcript_text):
#     """Saves transcript to the specified directory."""
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
    
#     safe_title = _sanitize_filename(video_title)
#     file_path = os.path.join(output_dir, f"{safe_title}.json")
    
#     with open(file_path, 'w') as f:
#         json.dump({"title": video_title, "transcript": transcript_text}, f, indent=4)
#     logger.info(f"Transcript saved for: {video_title}")

# def main():
#     # Step 1: Get all video IDs from the search results page
#     video_ids = get_video_ids_from_search(channel_url)
    
#     # Step 2: For each video ID, fetch the transcript and save it
#     for video_id in video_ids:
#         logger.info(f"Processing video ID: {video_id}")
#         transcript = fetch_transcript(video_id)
#         if transcript:
#             # For simplicity, fetching title from the YouTube page
#             video_title = f"Video_{video_id}"  # Customize this to fetch the title from the video page if needed
#             save_transcript(video_title, transcript)
    
#     logger.info("Script finished.")

# if __name__ == "__main__":
#     main()

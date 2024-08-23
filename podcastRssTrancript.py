import argparse
import os
import feedparser
import requests
from bs4 import BeautifulSoup
import re


def fetch_podcast_with_transcript(rss_feed_url):
    feed = feedparser.parse(rss_feed_url)
    ask_pod = input('Do you want to download the audio file(y/n): ')
    for entry in feed.entries:
        non_allowed_chars = r'[<>:"/\\|?*]'
        episode_title = re.sub(non_allowed_chars, ' -', entry.title)
        episode_podcast_url = entry.enclosures[0].href  # Assuming audio URL is in the first enclosure

        if ask_pod.lower() == 'y':
            print(f"Fetching podcast episode: {episode_title}")
            podcast_filename = f"{episode_title}.mp3"
            download_podcast(episode_podcast_url, podcast_filename)
        elif ask_pod.lower() == 'n':
            pass
        else:
            print("Pass only 'Y' or 'N' ")
            break

        episode_transcript = None
        if entry.link:
            # tc_url = None
            # if entry.link:
            #     tc_url = entry.link
            # elif entry.links:
            #     tc_url = entry.links
            episode_transcript = fetch_transcript(entry.link)
        else:
            print("Transcript not found on the webpage")

        if episode_transcript:

            transcript_filename = f"{episode_title}_transcript.txt"
            f = os.open(transcript_filename, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
            data = episode_transcript.encode('utf-8')
            os.write(f, data)
            print(f"Transcript saved: {transcript_filename}")
            os.close(f)
        else:
            print("Transcript not found")
            return


def download_podcast(audio_url, filename):
    response = requests.get(audio_url)
    with open(filename, "wb") as audio_file:
        audio_file.write(response.content)
        print(f"Podcast saved: {filename}")

def fetch_transcript(episode_url):
    response = requests.get(episode_url)
    soup = BeautifulSoup(response.content, "lxml")
    transcript_url = None
    transcript = None
    p_tags = soup.find_all('p')

    for p_tag in p_tags:
        if "Transcript" in p_tag.get_text():
            transcript_link = p_tag.find('a')
            if transcript_link:
                transcript_url = transcript_link.get('href')
                break


    if transcript_url:
        transcript_response = requests.get(transcript_url)
        new_soup = BeautifulSoup(transcript_response.content, "html.parser")
        transcript = new_soup.get_text()
        # ,print(transcript)
    else:
        print("No Transcript url found!")
        return

    return transcript.strip()


if __name__ == "__main__":
    # rss_feed_url = "https://naval.libsyn.com/rss" # 'https://anchor.fm/s/599522d0/podcast/rss' -- doesn't have transcript
    # rss_feed_url = 'https://lexfridman.com/feed/podcast/'
    rss_feed_link = input("Enter the RSS feed link of the podcast: ")
    fetch_podcast_with_transcript(rss_feed_link)



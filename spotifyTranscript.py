import requests
from bs4 import BeautifulSoup
import re

def extract_transcript(spotify_url):
    response = requests.get(spotify_url)
    non_allowed_chars = r'[<>:"/\\|?*]'

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        title_with_tag = soup.find('title').get_text()
        title_rename = title_with_tag.split(' |')[0].strip()
        episode_title = re.sub(non_allowed_chars, ' -', title_rename)
        transcript_url = None
        meta_tags = soup.find_all('meta')

        for meta_tag in meta_tags:
            content = meta_tag.get('content', '')
            if 'Transcript' in content:
                match = re.search(r'Transcript\s*(.+)', content)
                if match:
                    transcript_garb = match.group(1)
                    url_pattern = r'https?://\S+'
                    urls = re.findall(url_pattern, transcript_garb)
                    transcript_url = urls[0] if urls else "No URL found"
                    break

        if transcript_url:
            transcript_response = requests.get(transcript_url)
            new_soup = BeautifulSoup(transcript_response.content, 'lxml')
            transcript = new_soup.get_text().strip()
            filename = f'{episode_title}.txt'

            if transcript:
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(transcript)
                    print(f"Transcript for the Podcast saved: {filename}")
        else:
            # return "Transcript not found on the webpage."
            print("Transcript not found on the webpage.")

    else:
        # return "Failed to retrieve webpage. Status code:", response.status_code
        print("Failed to retrieve webpage. Status code:", response.status_code)
if __name__ == '__main__':
    spotify_url = input("Enter the Spotify URL: ")
    transcript = extract_transcript(spotify_url)

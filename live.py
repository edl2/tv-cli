
import requests
import re
from bs4 import BeautifulSoup
from fzf import fzf_prompt
import subprocess 
BASE_URL = 'https://daddylivehd.sx'
CHANNELS = f'{BASE_URL}/24-7-channels.php'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
HEADERS = {
    'User-Agent': USER_AGENT,
    'Referer': f'{BASE_URL}/'
}

TITLE = re.compile(r'">(.+?)</')
SOURCE = re.compile("source:'(.+?)'")


response = requests.get(CHANNELS, headers=HEADERS)
soup = BeautifulSoup(response.text, 'html.parser')
titles = [a.text for a in soup.find_all('a')]
links = [f"{BASE_URL}{a['href']}" for a in soup.find_all('a')]
choice = fzf_prompt(titles)
index = next((i for i, title in enumerate(titles) if title == choice), None)
url = links[index]


response = requests.get(url, headers=HEADERS)
soup = BeautifulSoup(response.text, 'html.parser')
recent = soup.find(class_='recent')
iframe = recent.find('iframe')

if iframe:
    url2 = iframe.get('src')
    if url2:
        headers = {
            'User-Agent': USER_AGENT,
            'Referer': url
        }
        response2 = requests.get(url2, headers=headers)
        links = re.findall(SOURCE, response2.text)
        if links:
            link = f'{links[-1]}|Referer={url2}&User-Agent={USER_AGENT}'
m3u8 = links[-1]
referer= url2
mpv = subprocess.Popen(["mpv", f"{m3u8}", f"--user-agent={USER_AGENT}", f"--http-header-fields=Referer: {referer}"])
mpv.wait()
mpv.kill()
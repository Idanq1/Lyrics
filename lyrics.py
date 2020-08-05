import requests
import json
from bs4 import BeautifulSoup
import spotify_token as st
import time
import sys


def get_json():
    data = st.start_session("sassonidan1@gmail.com", "is035620")
    token = data[0]
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
    }
    response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers)
    return json.loads(response.text)


def get_song(json_data):
    song = json_data["item"]["name"]
    return song


def get_artist(json_data):
    artist = json_data["item"]["artists"][0]["name"]
    return artist


def get_song_lyrics(song):
    search = f"{song} lyrics"
    headers_get = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 '
                      'Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    lyrics = '\n'
    s = requests.Session()
    url = 'https://www.google.com/search?q=' + search
    r = s.get(url, headers=headers_get)
    soup = BeautifulSoup(r.text, "html.parser").find_all("span", {"jsname": "YS01Ge"})
    for link in soup:
        lyrics += (link.text + '\n')
    return lyrics


def main():
    if len(sys.argv) > 1:
        custom_search_name = " ".join(sys.argv[1:])
        lyrics = get_song_lyrics(custom_search_name)
        print("\n" + custom_search_name.title() + "\n")
        print(lyrics)
        sys.exit()
    song_json = get_json()
    try:
        song = get_song(song_json)
        artist = get_artist(song_json)
        lyrics = get_song_lyrics(song)
        print(f"\n\n{song} by {artist}")
        print(lyrics)

        while True:
            try:
                time.sleep(5)
            except KeyboardInterrupt:
                sys.exit()
            temp_json = get_json()
            if song != get_song(temp_json):
                main()

    except TypeError:
        try:
            time.sleep(10)
        except KeyboardInterrupt:
            sys.exit()
        main()


if __name__ == '__main__':
    main()

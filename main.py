#*******************************************************************METHOD-2**********************************************************************************
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

LIST_URL = "https://www.billboard.com/charts/hot-100/"

date = input("Type date in format YYYY-MM-DD: ")

data_from_website = requests.get(f"{LIST_URL}{date}")
webpage_html = data_from_website.text

soup = BeautifulSoup(webpage_html, "html.parser")
titles = soup.find_all("span", class_="chart-element__information__song text--truncate color--primary")
artists = soup.find_all("span", class_="chart-element__information__artist text--truncate color--secondary")
song_name=[song.getText() for song in titles]
print(song_name)
#Authentication
ID= 'f40a0324b2894d97a137ac8be60b0a88'
Secret= 'bae470342dae4951a349806dea87e42a'

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=ID,
        client_secret=Secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
year=date.split('-')[0]
#Searching Songs
song_uris=[]
for song in song_name:
    result=sp.search(q=f"track:{song} year: {year}",type='track')
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
#making a playlist
playlist=sp.user_playlist_create(user_id,name=f"{date} Billboard 100",public=False)
print(playlist)

#Adding sons found to the new playlist
sp.playlist_add_items(playlist_id=playlist['id'],items=song_uris)

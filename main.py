from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

BASE_URL = "https://www.billboard.com/charts/hot-100/"

REDIRECT_URI = "http://example.com"

date = "1992-08-06"
if not date:
    date = input("Enter date in YYYY-MM-DD format: ")
    print(date)

response = requests.get(f"{BASE_URL}{date}")

soup = BeautifulSoup(response.text, 'html.parser')
song_names_spans = soup.select("li ul li h3")
song_artist_spans = soup.select("li ul li span")
song_names = [song.getText().strip() for song in song_names_spans]
artist_names = [artist.getText().strip() for artist in song_artist_spans]
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope="playlist-modify-public"))

spotify_user_id = sp.current_user()["id"]
playlist = sp.user_playlist_create(name=f"TimeMachine Playlist - {date}", user=spotify_user_id)

tracks = []
for index, (track, artist) in enumerate(zip(song_names, artist_names)):
    result = sp.search(q=f"track: {track} artist: {artist}", limit=1)
    if result:
        tracks.append(result['tracks']['items'][0]['id'])

sp.user_playlist_add_tracks(user=spotify_user_id, playlist_id=playlist['id'], tracks=tracks)
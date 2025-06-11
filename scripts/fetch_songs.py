import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import time
from dotenv import load_dotenv

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

scope = "playlist-read-private playlist-read-collaborative"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=scope,
    cache_path=".spotify_token_cache"
))

hit_playlist_id = "37i9dQZF1DXcBWIGoYBM5M"
non_hit_playlist_id = "37i9dQZF1DWVFeEut75IAL"

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")

def fetch_playlist_tracks(sp, playlist_id, is_hit):
    results = sp.playlist_tracks(playlist_id, limit=100)
    songs = []
    for item in results.get('items', []):
        track = item.get('track')
        if not track or not track.get('id'):
            continue
        features = sp.audio_features(track['id'])[0]
        if features:
            song = {
                'id': track['id'],
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'popularity': track['popularity'],
                'is_hit': is_hit
            }
            song.update(features)
            songs.append(song)
    return songs

hit_songs = fetch_playlist_tracks(sp, hit_playlist_id, is_hit=1)

non_hit_songs = fetch_playlist_tracks(sp, non_hit_playlist_id, is_hit=0)

df_hits = pd.DataFrame(hit_songs)
df_non_hits = pd.DataFrame(non_hit_songs)

df_hits.to_csv(os.path.join(DATA_DIR, "top50_songs.csv"), index=False)
df_non_hits.to_csv(os.path.join(DATA_DIR, "non_hit_songs.csv"), index=False)

df_combined = pd.concat([df_hits, df_non_hits], ignore_index=True)
df_combined.to_csv(os.path.join(DATA_DIR, "combined_songs.csv"), index=False)
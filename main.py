import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re

CLIENT_ID = "TU_CLIENT_ID"
CLIENT_SECRET = "TU_CLIENT_SECRET"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

def get_album_id(url):
    match = re.search(r"album/([a-zA-Z0-9]+)", url)
    return match.group(1) if match else None

def get_album_info(album_url):
    album_id = get_album_id(album_url)
    if not album_id:
        print("Error: No se pudo extraer el ID del álbum.")
        return
    
    album = sp.album(album_id)
    album_cover = album['images'][0]['url']
    album_name = album['name']
    release_date = album['release_date']
    track_list = [track['name'] for track in album['tracks']['items']]
    artists = [artist['name'] for artist in album['artists']]
    total_tracks = album['total_tracks']
    label = album['label']

    print(f"Portada: {album_cover}")
    print(f"Artistas: {', '.join(artists)}")
    print(f"Álbum: {album_name}")
    print(f"Año de publicación: {release_date}")
    print(f"Número de canciones: {total_tracks}")
    print("Canciones:")
    for idx, track in enumerate(track_list, start=1):
        print(f"{idx}. {track}")
    print(f"Discográfica: {label}")

album_url = "https://open.spotify.com/intl-es/album/0hvT3yIEysuuvkK73vgdcW?si=-jMEej5tTpujarW7VcjXAQ"  
get_album_info(album_url)

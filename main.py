import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
import subprocess

CLIENT_ID = "f9e28d4bd2564294a35bf0dec4052225"
CLIENT_SECRET = "26417cfae02742c9a7a77deee06f93df"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

def get_album_id(url):
    match = re.search(r"album/([a-zA-Z0-9]+)", url)
    return match.group(1) if match else None

def format_duration(milliseconds):
    total_seconds = milliseconds // 1000
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    if hours > 0:
        return f"{hours} hr {minutes} min {seconds} sec"
    return f"{minutes} min {seconds} sec"

def get_album_info(album_url):
    album_id = get_album_id(album_url)
    if not album_id:
        print("Error: No se pudo extraer el ID del álbum.")
        return
    
    album = sp.album(album_id)
    album_cover = album['images'][0]['url']
    album_name = album['name']
    release_date = album['release_date']
    artists = [artist['name'] for artist in album['artists']]
    total_tracks = album['total_tracks']
    label = album['label']

    track_list = []
    total_duration_ms = 0
    
    for track in album['tracks']['items']:
        track_list.append(track['name'])
        total_duration_ms += track['duration_ms']  


    total_duration_str = format_duration(total_duration_ms)


    command = f"curl -o ./img.png {album_cover}"
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


    print(f"Portada: {album_cover}")
    print(f"Artistas: {', '.join(artists)}")
    print(f"Álbum: {album_name}")
    print(f"Año de publicación: {release_date}")
    print(f"Número de canciones: {total_tracks}")
    print(f"Duración total del álbum: {total_duration_str}")  
    print("Canciones:")
    for idx, track in enumerate(track_list, start=1):
        print(f"{idx}. {track}")
        # print(f"{track}")
    print(f"Discográfica: {label}")

album_url = "https://open.spotify.com/intl-es/album/2Ek1q2haOnxVqhvVKqMvJe?si=yviX1yZMRHKx3MHJkGEO_Q"  
get_album_info(album_url)

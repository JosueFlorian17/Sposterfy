import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
import subprocess
import svgwrite
import requests
from PIL import Image
from io import BytesIO

CLIENT_ID = "TU_CLIENT_ID"
CLIENT_SECRET = "TU_CLIENT_SECRET"

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

def create_album_poster_svg(album_name, artists, release_date, total_tracks, total_duration, track_list, label, album_cover_url, output_file="album_poster.svg"):
    WIDTH, HEIGHT = 800, 1200
    COVER_SIZE = 400

    dwg = svgwrite.Drawing(output_file, size=(f"{WIDTH}px", f"{HEIGHT}px"), profile='tiny')
    dwg.add(dwg.rect(insert=(0, 0), size=(WIDTH, HEIGHT), fill="black"))

    response = requests.get(album_cover_url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img_path = "album_cover.png"
        img.save(img_path)
        dwg.add(dwg.image(img_path, insert=(200, 50), size=(COVER_SIZE, COVER_SIZE)))

    dwg.add(dwg.text(album_name, insert=(50, 500), fill="white", font_size="32px", font_family="Arial", font_weight="bold"))
    dwg.add(dwg.text(f"Artista(s): {', '.join(artists)}", insert=(50, 540), fill="white", font_size="20px", font_family="Arial"))
    dwg.add(dwg.text(f"Año: {release_date}", insert=(50, 580), fill="white", font_size="20px", font_family="Arial"))
    dwg.add(dwg.text(f"Número de canciones: {total_tracks}", insert=(50, 610), fill="white", font_size="20px", font_family="Arial"))
    dwg.add(dwg.text(f"Duración total: {total_duration}", insert=(50, 640), fill="white", font_size="20px", font_family="Arial"))
    dwg.add(dwg.text(f"Discográfica: {label}", insert=(50, 670), fill="white", font_size="20px", font_family="Arial"))

    y_position = 710
    dwg.add(dwg.text("Lista de Canciones:", insert=(50, y_position), fill="white", font_size="20px", font_family="Arial"))
    for idx, track in enumerate(track_list[:10], start=1):
        y_position += 30
        dwg.add(dwg.text(f"{idx}. {track}", insert=(50, y_position), fill="white", font_size="16px", font_family="Arial"))

    dwg.save()
    print(f"Póster generado y guardado como {output_file}")

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
    print(album['images'][0]['url'])
    print(f"Nombre del álbum: {album_name}")
    print(f"Artista(s): {', '.join(artists)}")
    print(f"Año: {release_date}")
    print(f"Número de canciones: {total_tracks}")
    print(f"Duración total: {total_duration_str}")
    print(f"Discográfica: {label}")
    print("Lista de Canciones:")
    for idx, track in enumerate(track_list, start=1):
        print(f"{idx}. {track}")

    create_album_poster_svg(album_name, artists, release_date, total_tracks, total_duration_str, track_list, label, album_cover)

album_url = "https://open.spotify.com/intl-es/album/2Ek1q2haOnxVqhvVKqMvJe?si=2yiymctjSg-BSdXCbvUTDQ"  
get_album_info(album_url)

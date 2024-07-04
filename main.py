from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth, CacheFileHandler

load_dotenv()

SPOTIFY_ID = os.getenv("SPOTIFY_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URL = "http://example.com"
USERNAME = os.getenv("USERNAME")


def get_billboard_data(date):
    """
       Fetches the Billboard Hot 100 page for the given date.
       Args:
           date (str): The date in the format YYYY-MM-DD.
       Returns:
           str: The HTML content of the Billboard Hot 100 page.
       Raises:
           requests.exceptions.RequestException: If the request to the Billboard page fails.
       """
    billboard_url = f"https://www.billboard.com/charts/hot-100/{date}/"
    response = requests.get(billboard_url)
    response.raise_for_status()
    return response.text


def parse_billboard_data(billboard_page):
    """
    Parses the Billboard Hot 100 page to extract song names and artist names.
    Finds info about songs and artists from html page,
    search the necessary tags using select() and add that names to the lists
    by using getText().
    Elements are selected from the initial list of artists through step 7,
    because the list contains another information after parsing.
    Cut off artists' name to select the main artist.
    Args:
        billboard_page (str): The HTML content of the Billboard Hot 100 page.
    Returns:
        tuple: A tuple containing two lists:
            - song_names (list): A list of song names,
            - artist_names (list): A list of artist names.
    """

    soup = BeautifulSoup(billboard_page, "html.parser")
    song_list = soup.select("li ul li h3")
    song_names = [song.getText().strip() for song in song_list]

    artist_list = soup.select("li ul li span")
    artist_names = []
    for artist in artist_list[0::7]:
        artist_name = artist.getText().strip()
        separators = ["featuring", "&", "X", "x"]
        index = -1
        for separator in separators:
            index = artist_name.lower().find(separator)
            if index != -1:
                break
        if index != -1:
            artist_name = artist_name[:index].strip()
        artist_names.append(artist_name)

    return song_names, artist_names


def authenticate_spotify(spotify_id, spotify_client_secret, redirect_url, username):
    """
    Authenticates the Spotify user and returns a Spotify client instance.
    Args:
        spotify_id (str): The Spotify client ID,
        spotify_client_secret (str): The Spotify client secret,
        redirect_url (str): The redirect URI for Spotify authentication,
        username (str): The Spotify user ID.
    Returns:
        spotipy.Spotify: An authenticated Spotify client instance.
    """

    cache_handler = CacheFileHandler(cache_path="token.txt", username=username)
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_id,
                                                   client_secret=spotify_client_secret,
                                                   redirect_uri=redirect_url,
                                                   scope="playlist-modify-private",
                                                   cache_handler=cache_handler))
    return sp


def get_song_uris(sp, song_names, artist_names):
    """
    Searches for the Spotify URIs of the given songs and artists,
    if song not found, give an error indicating which song was not found.
    Args:
        sp (spotipy.Spotify): An authenticated Spotify client instance,
        song_names (list): A list of song names,
        artist_names (list): A list of artist names.
    Returns:
        list: A list of Spotify URIs for the given songs.
    """

    song_uris = []
    for i in range(len(song_names)):
        song = song_names[i]
        artist = artist_names[i]
        results = sp.search(q=f"track:{song} artist:{artist}", type="track", limit=1)
        try:
            track_uri = results["tracks"]["items"][0]["uri"]
            song_uris.append(track_uri)
        except IndexError:
            print(f"Song {i+1} not found: {song} - {artist}")
    return song_uris


def create_playlist(sp, user_id, date, song_uris):
    """
    Creates a new playlist in a user account using user_playlist_create().
    Adds songs using song_uris from a billboard list with playlist_add_items().
    Args:
        sp (spotipy.Spotify): An authenticated Spotify client instance,
        user_id (str): The Spotify user ID,
        date (str): The date in the format YYYY-MM-DD,
        song_uris (list): A list of Spotify URIs for the songs to be added to the playlist.
    Returns:
        str: The ID of the newly created playlist.
    """

    new_playlist = sp.user_playlist_create(user=user_id,
                                           name=f"{date} Billboard 100",
                                           public=False,
                                           description="Playlist of Billboard 100 on that date")
    playlist_id = new_playlist["id"]
    sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)
    return playlist_id


def main():
    """Main function to fetch Billboard data, authenticate Spotify, and create a playlist."""
    date = input(
        "Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
    billboard_page = get_billboard_data(date)
    song_names, artist_names = parse_billboard_data(billboard_page)

    sp = authenticate_spotify(SPOTIFY_ID, SPOTIFY_CLIENT_SECRET, REDIRECT_URL, USERNAME)
    user_id = sp.current_user()["id"]

    song_uris = get_song_uris(sp, song_names, artist_names)
    create_playlist(sp, user_id, date, song_uris)


if __name__ == "__main__":
    main()

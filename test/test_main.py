import unittest
from unittest.mock import patch, MagicMock
import main


class TestMainFunctions(unittest.TestCase):

    @patch('builtins.input', return_value="2020-01-01")
    def test_get_billboard_data(self, mock_input):
        date = mock_input()
        data = main.get_billboard_data(date)
        self.assertIn('<html', data)
        self.assertIn('Billboard', data)

    def test_parse_billboard_data(self):
        with open('sample_billboard_page.html', 'r') as file:
            billboard_page = file.read()
        song_names, artist_names = main.parse_billboard_data(billboard_page)
        self.assertEqual(len(song_names), 100)
        self.assertEqual(len(artist_names), 100)

    @patch('spotipy.Spotify')
    def test_authenticate_spotify(self, MockSpotify):
        mock_spotify_instance = MockSpotify.return_value
        sp = main.authenticate_spotify("SPOTIFY_ID", "SPOTIFY_CLIENT_SECRET", "REDIRECT_URL", "USER_ID")
        self.assertEqual(sp, mock_spotify_instance)

    @patch('spotipy.Spotify')
    def test_get_song_uris(self, MockSpotify):
        mock_spotify_instance = MockSpotify.return_value
        mock_spotify_instance.search.return_value = {
            "tracks": {
                "items": [
                    {"uri": "spotify:track:12345"}
                ]
            }
        }
        song_names = ["Song1"]
        artist_names = ["Artist1"]
        song_uris = main.get_song_uris(mock_spotify_instance, song_names, artist_names)
        self.assertEqual(song_uris, ["spotify:track:12345"])

    @patch('spotipy.Spotify')
    def test_create_playlist(self, MockSpotify):
        mock_spotify_instance = MockSpotify.return_value
        mock_spotify_instance.user_playlist_create.return_value = {"id": "playlist123"}
        user_id = "user123"
        date = "2020-01-01"
        song_uris = ["spotify:track:12345"]
        playlist_id = main.create_playlist(mock_spotify_instance, user_id, date, song_uris)
        self.assertEqual(playlist_id, "playlist123")


if __name__ == '__main__':
    unittest.main()

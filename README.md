# Billboard to Spotify Playlist

## Project Description

This project allows you to create a Spotify playlist based on the Billboard Hot 100 chart for a specified date. The script fetches the Billboard chart, extracts song names and artist names, and then creates a corresponding Spotify playlist with these songs.

## Technologies Used

- **Python**: The main programming language used for this project.
- **Requests**: For fetching the Billboard Hot 100 page.
- **BeautifulSoup**: For parsing the HTML content of the Billboard page.
- **Spotipy**: For interacting with the Spotify Web API.
- **dotenv**: For loading environment variables from a .env file.
- **unittes**t: For unit testing the functions.

## Setup and Installation

**1. Clone the repository**:

```python
git clone https://github.com/yourusername/billboard-to-spotify.git
cd billboard-to-spotify
```
**2. Create and activate a virtual environment (optional but recommended):**

```python
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
**3. Install the required dependencies:**

```python
pip install -r requirements.txt
```
**4. Create a .env file in the root directory of the project and add your Spotify API credentials:**

```python
SPOTIFY_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
REDIRECT_URL=http://example.com
USER_ID=your_spotify_user_id
```

## Running the Project

**1. Run the main script:**

```
python main.py
```

**2. Input the date:** When prompted, input the date in the format __YYYY-MM-DD__.

## Running Tests

**1. Run the tests:**

```
python -m unittest discover
```

## Project Structure

- `'main.py'`: The main script that fetches Billboard data, authenticates Spotify, and creates a playlist.
- `'test_main.py'`: The test script for unit testing the functions in `'main.py'`.
- `'requirements.txt'`: The dependencies required for the project.
- `'.env'`: The file containing environment variables (not included in the repository).
from pydantic import BaseModel
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()


class Spotify(BaseModel, spotipy.Spotify):

    client_credentials_manager:SpotifyClientCredentials = SpotifyClientCredentials()

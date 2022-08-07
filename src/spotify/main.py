import pandas as pd
import spotipy
import os
import json
from warnings import filterwarnings
from functools import reduce
import operator
from spotipy.oauth2 import SpotifyClientCredentials
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv


load_dotenv()
filterwarnings("ignore")
pd.set_option("display.max_columns", 10)

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
client_credentials_manager = SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET
)
sp_client = spotipy.Spotify(
    client_credentials_manager=client_credentials_manager
)


def main():
    print("Starting...")

    playlist_ids = [
        "https://open.spotify.com/playlist/3r2zTRHgnAuRxYshydsf7R",
        "https://open.spotify.com/playlist/1PGA7tTmbEwCE5n7I1ygGS",
    ]
    df = get_playlist_tracks(playlist_ids[0])
    print(df.shape, df.tail())

    features = get_track_info(df)
    print(features.shape, features.tail())

    genres = get_artist_info(df)
    print(genres.shape, genres.tail())

    genre_analysis = get_genre_analysis(genres)
    print(genre_analysis.shape, genre_analysis.head(10))
    print("Done!")


# insert the URI as a string into the function
def get_playlist_tracks(uri_info):
    uri = []
    added_at = []
    track = []
    artist = []
    artist_id = []
    playlist = sp_client.playlist_tracks(uri_info)
    df = pd.DataFrame(playlist)

    for _, x in df["items"].items():
        t_artists, t_artist_ids = [], []
        uri.append(x.get("track").get("uri"))
        added_at.append(x.get("added_at"))
        track.append(x.get("track").get("name"))
        n_artists = len(x.get("track").get("artists"))
        for a in range(n_artists):
            t_artists.append(x.get("track").get("artists")[a].get("name"))
            t_artist_ids.append(x.get("track").get("artists")[a].get("id"))
        artist.append(t_artists)
        artist_id.append(t_artist_ids)

    df = pd.DataFrame(
        {
            "uri": uri,
            "added_at": added_at,
            "track": track,
            "artist": artist,
            "artist_id": artist_id,
        }
    )

    return df


def get_track_info(df):
    danceability = []
    energy = []
    key = []
    loudness = []
    speechiness = []
    acousticness = []
    instrumentalness = []
    liveness = []
    valence = []
    tempo = []
    for i in df["uri"]:
        for x in sp_client.audio_features(tracks=[i]):
            danceability.append(x.get("danceability"))
            energy.append(x.get("energy"))
            key.append(x.get("key"))
            loudness.append(x.get("loudness"))
            speechiness.append(x.get("speechiness"))
            acousticness.append(x.get("acousticness"))
            instrumentalness.append(x.get("instrumentalness"))
            liveness.append(x.get("liveness"))
            valence.append(x.get("valence"))
            tempo.append(x.get("tempo"))
    print(f"sample: {json.dumps(x, indent=2)}")
    features = pd.DataFrame(
        {
            "uri": df["uri"],
            "danceability": danceability,
            "energy": energy,
            "key": key,
            "loudness": loudness,
            "speechiness": speechiness,
            "acousticness": acousticness,
            "instrumentalness": instrumentalness,
            "liveness": liveness,
            "valence": valence,
            "tempo": tempo,
        }
    )

    return features


def get_artist_info(df):
    genres = []
    for artist_ids in df["artist_id"]:
        t_genres = []
        for a in artist_ids:
            t_genres.append(sp_client.artist(artist_id=a).get("genres"))
        genres.append(reduce(operator.concat, t_genres))
    print(f"sample: {json.dumps(t_genres, indent=2)}")
    genres = pd.DataFrame({"uri": df["uri"], "genres": genres})
    return genres


def get_genre_analysis(genres):
    genre_analysis = genres.explode("genres")
    genre_analysis = genre_analysis.genres.value_counts().reset_index()
    return genre_analysis


if __name__ == "__main__":
    main()

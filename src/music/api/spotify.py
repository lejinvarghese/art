import json
from functools import reduce
import operator
import pandas as pd
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.client_credentials_manager = SpotifyClientCredentials(
            client_id=self.client_id, client_secret=self.client_secret
        )
        self.client = Spotify(
            client_credentials_manager=self.client_credentials_manager
        )

    def get_playlist_tracks(self, playlist_id, limit=None):
        uri = []
        added_at = []
        track = []
        artist = []
        artist_id = []
        playlist_uri_prefix = "https://open.spotify.com/playlist/"
        playlist_uri = [
            playlist_id
            if playlist_uri_prefix in playlist_id
            else playlist_uri_prefix + playlist_id
        ][0]
        playlist = self.client.playlist_tracks(playlist_uri, limit)
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
                "playlist_id": playlist_id,
                "uri": uri,
                "added_at": added_at,
                "track": track,
                "artist": artist,
                "artist_id": artist_id,
            }
        )

        return df

    def get_track_info(self, tracks):
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
        for i in tracks["uri"]:
            for x in self.client.audio_features(tracks=[i]):
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
        print(f"Sample: {json.dumps(x, indent=2)}")
        features = pd.DataFrame(
            {
                "uri": tracks["uri"],
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

    def get_genres(self, df):
        genres = []
        for artist_ids in df["artist_id"]:
            t_genres = []
            for a in artist_ids:
                t_genres.append(self.client.artist(artist_id=a).get("genres"))
            genres.append(reduce(operator.concat, t_genres))
        print(f"Sample: {json.dumps(t_genres, indent=2)}")
        genres = pd.DataFrame({"uri": df["uri"], "genres": genres}).explode(
            "genres"
        )
        return genres

import os
from warnings import filterwarnings
from dotenv import load_dotenv
import pandas as pd
from api.spotify import SpotifyClient

load_dotenv()
filterwarnings("ignore")
pd.set_option("display.max_columns", 10)

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_PLAYLIST_IDS = os.getenv("SPOTIFY_PLAYLIST_IDS")


sp_client = SpotifyClient(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)


def main():
    print("Starting...")
    playlist_ids = SPOTIFY_PLAYLIST_IDS.split(",")
    tracks = pd.DataFrame()
    for p_id in playlist_ids:
        tracks = tracks.append(sp_client.get_playlist_tracks(p_id))
    features = sp_client.get_track_info(tracks)
    genres = sp_client.get_genres(tracks)

    tracks.to_parquet(
        "data/tracks.parquet",
        engine="pyarrow",
        compression="gzip",
        index=False,
    )
    features.to_parquet(
        "data/features.parquet",
        engine="pyarrow",
        compression="gzip",
        index=False,
    )
    genres.to_parquet(
        "data/genres.parquet",
        engine="pyarrow",
        compression="gzip",
        index=False,
    )

    # genres = pd.read_parquet("data/genres.parquet")
    print("Done!")


def get_genre_analysis(genres):
    genre_analysis = genres.genres.value_counts().reset_index()
    return genre_analysis


if __name__ == "__main__":
    main()

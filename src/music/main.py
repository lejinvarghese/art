import os
from warnings import filterwarnings
from dotenv import load_dotenv
import pandas as pd
from api.spotify import SpotifyClient
from pathlib import Path

load_dotenv()
filterwarnings("ignore")
pd.set_option("display.max_columns", 10)

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_PLAYLIST_IDS = os.getenv("SPOTIFY_PLAYLIST_IDS")
file_dir = Path(__file__).parent.absolute()


sp_client = SpotifyClient(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)


def main():
    playlist_ids = SPOTIFY_PLAYLIST_IDS.split(",")

    attributes = {}

    tracks = pd.DataFrame()
    for p_id in playlist_ids:
        tracks = tracks.append(sp_client.get_playlist_tracks(p_id))
    attributes["tracks"] = tracks
    attributes["features"] = sp_client.get_track_info(attributes.get("tracks"))
    attributes["genres"] = sp_client.get_genres(attributes.get("tracks"))
    attributes["genre_graph"] = sp_client.get_genre_graph()

    for name, data in attributes.items():
        data.to_parquet(
            f"{file_dir}/data/{name}.parquet",
            engine="pyarrow",
            compression="gzip",
            index=False,
        )

    # g_i = pd.concat(
    #     [
    #         attributes["genres"]["uri"],
    #         pd.get_dummies(attributes["genres"]["genres"]),
    #     ],
    #     axis=1,
    # )

    print(attributes["genre_graph"].head())

    # genres = pd.read_parquet(f"{file_dir}/data/genres.parquet")
    # print(genres.head())


if __name__ == "__main__":
    main()

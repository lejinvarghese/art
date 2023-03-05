import os
from warnings import filterwarnings
from dotenv import load_dotenv
import pandas as pd
from api.spotify import SpotifyClient
from pathlib import Path
from pyvis import network as py_net

load_dotenv()
filterwarnings("ignore")
pd.set_option("display.max_columns", 10)

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_PLAYLIST_IDS = os.getenv("SPOTIFY_PLAYLIST_IDS")
file_dir = Path(__file__).parent.absolute()


sp_client = SpotifyClient(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)


class MusicGraph:
    def __init__(self, genres):
        self.genres = genres
        self.data = self.__preprocess()

    def __preprocess(self):
        genre_matrix = (
            pd.get_dummies(self.genres["genres"])
            .set_index(self.genres["track_uri"])
            .reset_index()
        )
        genre_matrix = genre_matrix.groupby("track_uri").max()
        genre_cooc_matrix = genre_matrix.T.dot(genre_matrix).reset_index()
        genre_cooc_deep = genre_cooc_matrix.melt(
            value_name="weight", id_vars="index", var_name="target"
        ).rename(columns={"index": "source"})
        genre_cooc_deep = genre_cooc_deep[
            (genre_cooc_deep.weight > 0)
            & (genre_cooc_deep.source != genre_cooc_deep.target)
        ]
        return genre_cooc_deep.sort_values(by="weight", ascending=False)

    def __node_segments(self):
        segment = (
            self.genres.groupby(["genres", "playlist_id"])
            .count()
            .reset_index()
            .sort_values(by="track_uri", ascending=False)
        )
        segment = segment.loc[
            segment.groupby(["genres"])["track_uri"].idxmax()
        ].reset_index(drop=True)
        segment.playlist_id = segment.playlist_id.astype("category").cat.codes

        return dict(zip(segment.genres, segment.playlist_id))

    def create(self):
        graph = py_net.Network(
            height="512px",
            width="100%",
            notebook=False,
            heading="Music Graph",
        )

        sources = self.data["source"]
        targets = self.data["target"]
        weights = self.data["weight"]

        edge_data = zip(sources, targets, weights)

        node_map = self.__node_segments()

        template_colors = [
            "red",
            "blue",
            "green",
            "black",
            "yellow",
            "orange",
            "purple",
            "pink",
        ]

        for e in edge_data:
            src = e[0]
            dst = e[1]
            w = e[2]

            graph.add_node(
                src, src, title=src, color=template_colors[node_map.get(src)]
            )
            graph.add_node(
                dst, dst, title=dst, color=template_colors[node_map.get(dst)]
            )
            graph.add_edge(src, dst, value=w)

        neighbor_map = graph.get_adj_list()

        for node in graph.nodes:
            node["title"] = node["title"].replace("_", " ")
            node["group"] = node_map.get(node["id"])
            node["value"] = len(neighbor_map[node["id"]])
        graph.repulsion()
        graph.show_buttons(filter_=["physics"])
        graph.write_html("assets/music_graph.html")


def main():
    playlist_ids = SPOTIFY_PLAYLIST_IDS.split(",")

    attributes = {}

    tracks = pd.DataFrame()

    for p_id in playlist_ids:
        tracks = tracks.append(sp_client.get_playlist_tracks(p_id))
    attributes["tracks"] = tracks
    attributes["features"] = sp_client.get_track_info(attributes.get("tracks"))
    attributes["genres"] = sp_client.get_genres(attributes.get("tracks"))

    for name, data in attributes.items():
        data.to_parquet(
            f"{file_dir}/data/{name}.parquet",
            engine="pyarrow",
            compression="gzip",
            index=False,
        )

    genres = pd.read_parquet(f"{file_dir}/data/genres.parquet")
    genre_graph = MusicGraph(genres)
    genre_graph.create()


if __name__ == "__main__":
    main()

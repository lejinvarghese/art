from bs4 import BeautifulSoup
import requests


def scrape_lyrics(artist_name, song_name):
    """
    Untested.
    """
    artist_name_mod = (
        str(artist_name.replace(" ", "-"))
        if " " in artist_name
        else str(artist_name)
    )
    song_name_mod = (
        str(song_name.replace(" ", "-")) if " " in song_name else str(song_name)
    )
    page = requests.get(
        "https://genius.com/"
        + artist_name_mod
        + "-"
        + song_name_mod
        + "-"
        + "lyrics"
    )
    html = BeautifulSoup(page.text, "html.parser")
    lyrics1 = html.find("div", class_="lyrics")
    lyrics2 = html.find("div", class_="Lyrics__Container-sc-1ynbvzw-2 jgQsqn")
    if lyrics1:
        lyrics = lyrics1.get_text()
    elif lyrics2:
        lyrics = lyrics2.get_text()
    elif lyrics1 == lyrics2 == None:
        lyrics = None
    return lyrics


# function to attach lyrics onto data frame
# artist_name should be inserted as a string
def lyrics_onto_frame(tracks, artist_name):
    """
    Untested.
    """
    for i, x in enumerate(tracks["track"]):
        test = scrape_lyrics(artist_name, x)
        tracks.loc[i, "lyrics"] = test
    return tracks

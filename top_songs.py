#! python3
"""
Top Songs
Caleb Webster
2020
This program requests the top songs from www.billboard.com/charts/hot-100
"""

import requests
import sys
from bs4 import BeautifulSoup


def main():
    """Request and display the specified number of songs. If no number
    is specified, display the top 10."""
    songs_count = get_songs_count()
    songs = get_top_songs(songs_count)
    print_songs(songs)


def get_songs_count():
    """Return the number passed in to windows run command, or 10 if no
    number is passed in or an error occurs."""
    try:
        return int(sys.argv[1])
    except ValueError:
        return 10
    except IndexError:
        return 10


def get_top_songs(n):
    """Request and return a number of the top songs from billboard.com."""
    top_100 = requests.get("https://www.billboard.com/charts/hot-100")
    top_100.raise_for_status()
    soup = BeautifulSoup(top_100.text, "html.parser")
    songs = []
    for song in soup.find_all("li", class_="chart-list__element")[:n]:
        name = song.find("span", class_="chart-element__information__song").text
        artist = song.find("span", class_="chart-element__information__artist").text
        songs.append([name, artist])
    return songs


def print_songs(songs):
    """Display songs as a numbered list."""
    print(f"Top {len(songs)} songs this week:")
    for number, song in enumerate(songs, 1):
        name = song[0]
        artist = song[1]
        if "Featuring" in artist:
            f_index = artist.find("Featuring")
            artist = artist[:f_index] + '(' + "ft." + artist[f_index + len("Featuring"):] + ')'
        print(f"{number:3}. {name} - {artist}")


if __name__ == '__main__':
    main()

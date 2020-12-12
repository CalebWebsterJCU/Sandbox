#! python3
"""
Top Games
2020
This program requests and displays the top new games released recently.
Data obtained from https://metacritic.com
"""

import requests
from bs4 import BeautifulSoup
import sys

VALID_PLATFORMS = {'ps5': 'PS5', 'ps4': 'PS4', 'xbox-series-x': 'Xbox Series X', 'xboxone': 'Xbox One', 'switch': 'Switch', 'pc': 'PC', 'ios': 'IOS', 'stadia': 'Stadia'}
DEFAULT_NUM_GAMES = 10
DEFAULT_PLATFORM = 'pc'


def main():
    """Get number of games, then request and display the top new games on metacritic.com."""
    num_of_games = get_num_of_games(DEFAULT_NUM_GAMES)
    platform = get_valid_platform(VALID_PLATFORMS, DEFAULT_PLATFORM)
    games = get_top_games(num_of_games, platform)
    print_games(games, VALID_PLATFORMS[platform])
    print("Available Platforms:")
    for platform, name in VALID_PLATFORMS.items():
        print(f"{name}: {platform}")


def get_num_of_games(default=10):
    """Get and return number of games from command line, otherwise return default."""
    try:
        return int(sys.argv[1])
    except ValueError:
        return default
    except IndexError:
        return default


def get_valid_platform(valid_platforms, default='pc'):
    """Get and return platform from command line if platform is valid, otherwise return default."""
    try:
        return sys.argv[2] if sys.argv[2] in valid_platforms else default
    except IndexError:
        return default


def get_top_games(n, platform):
    """Request games from metacritic.com and return a list of n dictionaries containing game details."""
    games = []
    metacritic = requests.get(
        f'https://www.metacritic.com/browse/games/release-date/new-releases/{platform}/metascore',
        headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    )
    metacritic.raise_for_status()
    soup = BeautifulSoup(metacritic.text, 'html.parser')
    for game in soup.find_all('td', class_='clamp-summary-wrap')[:n]:
        title = game.find('h3').text.strip()
        date = game.find('div', 'clamp-details').find_all('span')[-1].text.strip()
        score = game.find('div', class_='metascore_w').text.strip()
        summary = game.find('div', class_='summary').text.strip().replace('\n', ' ')
        games.append({'title': title, 'date': date, 'score': score, 'summary': summary})
    return games


def print_games(games, platform):
    """Print details of all games."""
    print(f"Top {len(games)} New Game Releases for {platform}:")
    for x, game in enumerate(games, 1):
        print(f"{x}. {game['title']} ({game['date']})")
        print(f"Score: {game['score']}")
        print(game['summary'])


if __name__ == '__main__':
    main()

"""
League Stats
Caleb Webster
2020
This program requests information about a summoner's League of Legends
statistics from op.gg and displays it to the screen.
"""

import sys
import requests
from bs4 import BeautifulSoup

STAT_NAMES = ["Summoner Name", "Level", "Rank", "LP", "Win Rate", "Games Played", "Games Won", "Games Lost", "Season Wins", "Season Losses", "Season Win Rate", "Season Most Played Champion"]


def main():
    """Get summoner name. While name is not blank, request information from op.gg and display summoner's statistics."""
    if len(sys.argv) > 1:
        summoner_name = ''.join(sys.argv[1:])
    else:
        summoner_name = input("Summoner name: ")
    stats = get_summoner_stats(summoner_name)
    print_stats(stats)


def get_summoner_stats(summoner):
    """
    Request summoner's statistics from op.gg.
    :return: dictionary of stat names to values
    """
    stats_dict = {}
    url = f"https://oce.op.gg/summoner/userName={summoner}"
    headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Mobile Safari/537.36"}
    op_gg = requests.get(url, headers=headers)
    soup = BeautifulSoup(op_gg.text, "html.parser")
    stats_dict[STAT_NAMES[0]] = soup.find("div", class_="SummonerName").text
    stats_dict[STAT_NAMES[1]] = soup.find("span", class_="Level tip").text
    stats_dict[STAT_NAMES[2]] = soup.find("div", class_="Tier").text.strip()
    if stats_dict[STAT_NAMES[2]] != "Unranked":
        stats_dict[STAT_NAMES[3]] = int(soup.find("div", class_="LP").text[:-3])
        stats_dict[STAT_NAMES[8]] = int(soup.find("span", class_="Wins").text[:-1])
        stats_dict[STAT_NAMES[9]] = int(soup.find("span", class_="Losses").text[:-1])
        stats_dict[STAT_NAMES[10]] = soup.find("span", class_="Ratio").text
    else:
        stats_dict[STAT_NAMES[3]] = "0"
    stats_dict[STAT_NAMES[4]] = soup.find("b", class_="WinRatio").text
    stats_dict[STAT_NAMES[6]] = int(soup.find("span", class_="win").text)
    stats_dict[STAT_NAMES[7]] = int(soup.find("span", class_="lose").text)
    stats_dict[STAT_NAMES[5]] = stats_dict.get(STAT_NAMES[6]) + stats_dict.get(STAT_NAMES[7])
    stats_dict[STAT_NAMES[11]] = soup.select_one("div.ChampionName a").text.strip()
    return stats_dict


def print_stats(stats_dict):
    """Print all stats to the console."""
    for stat_name in STAT_NAMES:
        print(f"{stat_name}: {stats_dict.get(stat_name)}")


if __name__ == "__main__":
    main()

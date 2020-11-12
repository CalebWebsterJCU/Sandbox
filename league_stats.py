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
from selenium import webdriver
from colours import BOLD, YELLOW, END

STAT_NAMES = ["Name", "Level", "Rank", "LP", "Win Rate (last 10 games)", "Average KDA", "Season Wins", "Season Losses", "Season Win Rate", "Season Most Played Champion", "Average KDA as Champion"]
REGIONS_TO_URLS = {"Oceania": "oce", "Korea": "kr", "Japan": "jp", "North America": "na", "Europe West": "euw", "Europe Nordic & East": "eune", "Brazil": "br", "LAS": "las", "lAN": "lan", "Russia": "ru", "Turkey": "tr"}
STARTING_REGION = "oce"
HEADERS = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Mobile Safari/537.36"}
CHROME_DRIVER_PATH = r"C:\Program Files\Chrome Driver\chromedriver.exe"


def main():
    """Get summoner name. While name is not blank, request information from op.gg and display summoner's statistics."""
    region = STARTING_REGION
    if len(sys.argv) > 1:
        summoner_name = ''.join(sys.argv[1:])
    else:
        summoner_name = '+'.join(input(f"{BOLD}Summoner name{END} (! to change region): ").split(' '))
    while summoner_name:
        if summoner_name == '!':
            region = change_region()
        else:
            url = build_url(region, summoner_name)
            if is_valid(url, HEADERS):
                stats = get_summoner_stats(url, HEADERS)
                print_stats(stats)
                print(url)
                # open_page(url, CHROME_DRIVER_PATH)
            else:
                print("This summoner is not registered at OP.GG. Please check spelling.")
        summoner_name = '+'.join(input(f"\n{BOLD}Summoner name{END} (! to change region): ").split(' '))


def change_region():
    """Display region options and keep getting input until user enters a valid region."""
    print(f"{YELLOW}Region Keys:{END}")
    for name, url in REGIONS_TO_URLS.items():
        print(f"{name}: {url}")
    region = input(f"{BOLD}Region: {END}")
    while region not in REGIONS_TO_URLS.values():
        print("Invalid region")
        region = input(f"{BOLD}\nRegion: {END}")
    print(f"Region changed to {list(REGIONS_TO_URLS.keys())[list(REGIONS_TO_URLS.values()).index(region)]}")
    return f"{region}" if region != "kr" else 'www'


def build_url(region, summoner):
    """Construct and return a valid op.gg url combining region and summoner name."""
    return f"https://{region}.op.gg/summoner/userName={summoner}"


def is_valid(url, headers):
    """Check whether the summoner name passed in is a valid summoner registered in op.gg."""
    op_gg = requests.get(url, headers=headers)
    soup = BeautifulSoup(op_gg.text, "html.parser")
    try:
        return soup.find("h2", class_="Title").text != "This summoner is not registered at OP.GG. Please check spelling."
    except AttributeError:
        return True


def get_summoner_stats(url, headers):
    """
    Request summoner's statistics from op.gg.
    :return: dictionary of stat names to values
    """
    stats_dict = {}
    op_gg = requests.get(url, headers=headers)
    soup = BeautifulSoup(op_gg.text, "html.parser")
    stats_dict[STAT_NAMES[0]] = soup.find("div", class_="SummonerName").text
    stats_dict[STAT_NAMES[1]] = soup.find("span", class_="Level tip").text
    stats_dict[STAT_NAMES[2]] = soup.find("div", class_="Tier").text.strip()
    if stats_dict[STAT_NAMES[2]] != "Unranked":
        stats_dict[STAT_NAMES[3]] = int(soup.find("div", class_="LP").text[:-3])
        stats_dict[STAT_NAMES[6]] = int(soup.find("span", class_="Wins").text[:-1])
        stats_dict[STAT_NAMES[7]] = int(soup.find("span", class_="Losses").text[:-1])
        stats_dict[STAT_NAMES[8]] = soup.find("span", class_="Ratio").text
    # The following stats may not be displayed on op.gg
    try:
        stats_dict[STAT_NAMES[4]] = soup.find("b", class_="WinRatio").text
        stats_dict[STAT_NAMES[5]] = "/".join([soup.select_one(f"div.KDA span.{word}").text for word in ["Kill", "Death", "Assist"]])
    except AttributeError:
        stats_dict[STAT_NAMES[4]] = "There are no results recorded."
    try:
        stats_dict[STAT_NAMES[9]] = soup.select_one("div.ChampionName a").text.strip()
        stats_dict[STAT_NAMES[10]] = "/".join([soup.select_one(f"div.KDAEach span.{word}").text for word in ["Kill", "Death", "Assist"]])
    except AttributeError:
        stats_dict[STAT_NAMES[0]] = "There are no results recorded."
    return stats_dict


def print_stats(stats_dict):
    """Print all stats to the console."""
    for stat_name in STAT_NAMES:
        if stat_name in stats_dict:
            print(f"{stat_name}: {stats_dict.get(stat_name)}")


def open_page(url, driver_path):
    """Open url with selenium Chrome webdriver."""
    driver = webdriver.Chrome(driver_path)
    driver.get(url)


if __name__ == "__main__":
    main()

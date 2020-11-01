#! python3.7

import sys
import webbrowser

arguments = sys.argv

if len(arguments) > 1:
    search = "+".join(arguments[1:])
    url = f"https://youtube.com/results?search_query={search}"
else:
    url = "https://youtube.com"

webbrowser.open(url)

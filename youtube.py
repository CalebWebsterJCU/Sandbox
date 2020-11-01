#! python3.7

import sys
import webbrowser

arguments = sys.argv
url = "https://youtube.com"

if len(arguments) > 1:
    search = "+".join(arguments[1:])
    url += f"/results?search_query={search}"

webbrowser.open(url)

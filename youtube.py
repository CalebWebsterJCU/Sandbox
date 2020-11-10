#! python3
"""
Youtube
Caleb Webster
2020
This program opens www.youtube.com and searches for a phrase if one is passed to the run command.
"""

import sys
import webbrowser


def main():
    """Open www.youtube.com, passing in any run command arguments as search terms."""
    arguments = sys.argv
    url = "https://youtube.com"
    if len(arguments) > 1:
        search = "+".join(arguments[1:])
        url += f"/results?search_query={search}"
    webbrowser.open(url)


if __name__ == '__main__':
    main()

"""
Top Songs App
2021
This tkinter application uses a GUI to get and display the top songs
from www.billboard.com with links to the music videos on youtube.
"""

from tkinter import *
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build


class TopSongsApp:
    """Top Songs Tkinter Application."""
    
    def __init__(self):
        self.root = Tk()
        self.root.title('Top Songs')
        self.root.geometry('500x500')
    
    def run(self):
        """Start app."""
        self.root.mainloop()


if __name__ == '__main__':
    TopSongsApp().run()

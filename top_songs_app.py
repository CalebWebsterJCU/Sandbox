"""
Top Songs App
2021
This tkinter application uses a GUI to get and display the top songs
from www.billboard.com with links to the music videos on youtube.
"""

import os
import io
from tkinter import *
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from PIL import ImageTk, Image
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials


class TopSongsApp:
    """Top Songs Tkinter Application."""
    
    DEFAULT_NUM_SONGS = 10
    GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
    LARGE_FONT = ('Goldman Regular', 20)
    SMALL_FONT = ('Goldman Regular', 10)
    
    def __init__(self):
        self.num_songs = self.DEFAULT_NUM_SONGS
        self.top_songs = []
        # self.yt_api = build('youtube', 'v3', developerKey=self.GOOGLE_API_KEY)
        self.sp_api = Spotify(client_credentials_manager=SpotifyClientCredentials())
        self.songs = self.get_top_songs()
        self.root = Tk()
        self.root.title('Top Songs')
        # self.root.geometry('400x400')
        self.images = {
            'refresh': ImageTk.PhotoImage(Image.open('refresh(24).png')),
            'album_covers': [],
            'youtube': ImageTk.PhotoImage(Image.open('youtube.png').resize((30, 30)))
        }
        self.widgets = {}
        self.create_ui()
        
    def create_ui(self):
        """Create buttons and sections and add them to the GUI."""
        top_frame = LabelFrame(self.root, bd=3, relief=SUNKEN)
        title = Label(top_frame, text='Top Songs', font=self.LARGE_FONT)
        num_songs = Entry(top_frame, width=3, bd=3, font=self.SMALL_FONT)
        refresh_btn = Button(top_frame, bd=3, image=self.images['refresh'])
        
        bottom_frame = LabelFrame(self.root, bd=3, relief=SUNKEN)
        
        top_frame.grid(row=0, column=0, padx=5, pady=5)
        title.grid(row=0, column=0, padx=75)
        num_songs.grid(row=0, column=1, padx=0)
        refresh_btn.grid(row=0, column=2, padx=15)
        bottom_frame.grid(row=1, column=0, padx=5, pady=5, sticky=W+E)
        
        self.widgets['top_frame'] = top_frame
        self.widgets['title'] = title
        self.widgets['num_songs'] = num_songs
        self.widgets['refresh_btn'] = refresh_btn
        self.widgets['bottom_frame'] = bottom_frame
        self.widgets['song_frames'] = []
        
        self.create_song_widgets()
    
    def create_song_widgets(self, remove=False):
        """Create buttons and labels for each song."""
        # If specified, remove all song widgets.
        if remove:
            for widget in self.widgets['song_frames']:
                widget.grid_forget()
            self.widgets['song_frames'].clear()
            self.images['album_covers'].clear()
        max_name_length = 20
        max_artist_length = 15
        # Add song widgets to bottom frame.
        bottom_frame = self.widgets['bottom_frame']
        for x in range(len(self.songs)):
            song = self.songs[x]
            # Shorten song and artist name if they exceed the maximum values.
            shortened_name = song['name'][:max_name_length + 1] + '...' if len(song['name']) > max_name_length else song['name']
            shortened_artist = song['artist'][:max_name_length + 1] + '...' if len(song['artist']) > max_name_length else song['artist']
            # Load, resize and store album cover image.
            image_data = requests.get(song['album_cover']).content
            loaded_image = ImageTk.PhotoImage(Image.open(io.BytesIO(image_data)).resize((30, 30)))
            self.images['album_covers'].append(loaded_image)
            # Create inner frame and buttons for song name, artist, album cover, and music video.
            inner_frame = LabelFrame(bottom_frame, bd=3, relief=RAISED)
            name_btn = Button(inner_frame, width=max_name_length, bd=0, text=shortened_name, padx=10, anchor=W, font=self.SMALL_FONT)
            artist_btn = Button(inner_frame, width=max_artist_length, bd=0, text=shortened_artist, padx=10, anchor=W, font=self.SMALL_FONT)
            album_btn = Button(inner_frame, bd=0, image=self.images['album_covers'][x])
            youtube_btn = Button(inner_frame, bd=0, image=self.images['youtube'])
            # Add buttons and frame to bottom frame.
            inner_frame.grid(row=x, column=0, padx=5, pady=5, sticky=W+E)
            name_btn.grid(row=0, column=0)
            artist_btn.grid(row=0, column=1)
            album_btn.grid(row=0, column=2, padx=10)
            youtube_btn.grid(row=0, column=3, padx=10)
            # Create and bind balloon tooltips to buttons.
            
            self.widgets['song_frames'].append(inner_frame)
    
    def get_top_songs(self):
        """Request and return a number of the top songs from billboard.com."""
        top_100 = requests.get('https://www.billboard.com/charts/hot-100')
        try:
            top_100.raise_for_status()
        except requests.HTTPError:
            return []
        soup = BeautifulSoup(top_100.text, 'html.parser')
        songs = []
        for number, song in enumerate(soup.find_all('li', class_='chart-list__element')[:self.num_songs], 1):
            name = song.find('span', class_='chart-element__information__song').text
            artist = song.find('span', class_='chart-element__information__artist').text.replace('Featuring', 'ft.')
            album_cover = self.get_album_cover_art(name, artist)
            
            songs.append({'number': number, 'name': name, 'artist': artist, 'album_cover': album_cover})
        return songs
    
    def get_album_cover_art(self, song_name, artist):
        """
        Search for a track using the Spotify API and return the
        smallest version of its album's cover art.
        """
        # TODO: album name
        # Remove featured artists.
        if ' ft.' in artist:
            artist = artist[:artist.find(' ft.')]
        # Send request and sift through json to find image url.
        result = self.sp_api.search(q=f'{song_name} {artist}', type='track', limit=1)
        return result['tracks']['items'][0]['album']['images'][2]['url']
        
    def run(self):
        """Start app."""
        self.root.mainloop()


if __name__ == '__main__':
    # root = Tk()
    # frame = LabelFrame(root, text='frame')
    # frame.pack()
    # mainloop()
    TopSongsApp().run()

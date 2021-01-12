"""
Top Songs App
2021
This tkinter application uses a GUI to get and display the top songs
from www.billboard.com with links to the music videos on youtube.
"""

import os
import io
from tkinter import *
from tkinter import ttk
import requests
import webbrowser
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from PIL import ImageTk, Image
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials


class TopSongsApp:
    """Top Songs Tkinter Application."""
    
    DEFAULT_NUM_SONGS = 10
    GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
    LARGE_FONT = ('Goldman', 22)
    SMALL_FONT = ('Sansation', 12)
    
    def __init__(self):
        self.num_songs = self.DEFAULT_NUM_SONGS
        self.top_songs = []
        self.yt_api = build('youtube', 'v3', developerKey=self.GOOGLE_API_KEY)
        self.sp_api = Spotify(client_credentials_manager=SpotifyClientCredentials())
        self.songs = self.get_top_songs()
        # [
        #     {'number': 1, 'name': 'Mood', 'artist': '24kGoldn ft. iann dior', 'album_name': 'Mood (feat. iann dior)', 'album_cover': 'https://i.scdn.co/image/ab67616d00004851ff8c985ecb3b7c5f847be357', 'song_uri': 'spotify:track:3tjFYV6RSFtuktYl3ZtYcq', 'artist_uri': 'spotify:artist:6fWVd57NKTalqvmjRd2t8Z', 'album_uri': 'spotify:album:4YMnOf4a7obOcN1Gy2QEuM'},
        #     {'number': 2, 'name': 'Positions', 'artist': 'Ariana Grande', 'album_name': 'Positions', 'album_cover': 'https://i.scdn.co/image/ab67616d000048515ef878a782c987d38d82b605', 'song_uri': 'spotify:track:35mvY5S1H3J2QZyna3TFe0', 'artist_uri': 'spotify:artist:66CXWjxzNUsdJxJ2JdwvnR', 'album_uri': 'spotify:album:3euz4vS7ezKGnNSwgyvKcd'},
        #     {'number': 3, 'name': 'Blinding Lights', 'artist': 'The Weeknd', 'album_name': 'After Hours', 'album_cover': 'https://i.scdn.co/image/ab67616d000048518863bc11d2aa12b54f5aeb36', 'song_uri': 'spotify:track:0VjIjW4GlUZAMYd2vXMi3b', 'artist_uri': 'spotify:artist:1Xyo4u8uXC1ZmMpatF05PJ', 'album_uri': 'spotify:album:4yP0hdKOZPNshxUOjY0cZj'},
        #     {'number': 4, 'name': 'Holy', 'artist': 'Justin Bieber ft. Chance The Rapper', 'album_name': 'Holy', 'album_cover': 'https://i.scdn.co/image/ab67616d00004851572c68f79b356c21202e248c', 'song_uri': 'spotify:track:5u1n1kITHCxxp8twBcZxWy', 'artist_uri': 'spotify:artist:1uNFoZAHBGtllmzznpCI3s', 'album_uri': 'spotify:album:4hR7jjsPvRwwcHx8ntJSQS'},
        #     {'number': 5, 'name': 'Dynamite', 'artist': 'BTS', 'album_name': 'BE', 'album_cover': 'https://i.scdn.co/image/ab67616d000048513deb4b0115410a85afe31c29', 'song_uri': 'spotify:track:4saklk6nie3yiGePpBwUoc', 'artist_uri': 'spotify:artist:3Nrfpe0tUJi4K4DXYWgMUX', 'album_uri': 'spotify:album:2qehskW9lYGWfYb0xPZkrS'},
        #     {'number': 6, 'name': 'Go Crazy', 'artist': 'Chris Brown & Young Thug', 'album_name': 'Slime & B', 'album_cover': 'https://i.scdn.co/image/ab67616d0000485163e0ddbb488d0eeec0e738fc', 'song_uri': 'spotify:track:1IIKrJVP1C9N7iPtG6eOsK', 'artist_uri': 'spotify:artist:7bXgB6jMjp9ATFy66eO08Z', 'album_uri': 'spotify:album:7fZKtzZAsfH0kzeTivu5TG'},
        #     {'number': 7, 'name': 'Laugh Now Cry Later', 'artist': 'Drake ft. Lil Durk', 'album_name': 'Laugh Now Cry Later (feat. Lil Durk)', 'album_cover': 'https://i.scdn.co/image/ab67616d0000485152c75ed37313b889447011ef', 'song_uri': 'spotify:track:2SAqBLGA283SUiwJ3xOUVI', 'artist_uri': 'spotify:artist:3TVXtAsR1Inumwj472S9r4', 'album_uri': 'spotify:album:0qGdc7fNq9RNIPEzZufa43'},
        #     {'number': 8, 'name': 'I Hope', 'artist': 'Gabby Barrett ft. Charlie Puth', 'album_name': 'Goldmine', 'album_cover': 'https://i.scdn.co/image/ab67616d000048516c4c8d7e8742204879bff7b3', 'song_uri': 'spotify:track:23T0OX7QOiIUFShSzbJ5Uo', 'artist_uri': 'spotify:artist:6Iz3eq2aQGFf7TbGT2iahL', 'album_uri': 'spotify:album:4Iqfx63CZhFGGIHiAvLxXY'},
        #     {'number': 9, 'name': 'All I Want For Christmas Is You', 'artist': 'Mariah Carey', 'album_name': 'Merry Christmas (Deluxe Anniversary Edition)', 'album_cover': 'https://i.scdn.co/image/ab67616d0000485101c44a2d3c4ae7a6682df677', 'song_uri': 'spotify:track:4I5Hn34v6foGP3ta9Xx0rN', 'artist_uri': 'spotify:artist:4iHNK0tOyZPYnBU7nGAgpQ', 'album_uri': 'spotify:album:0cS9prZ8u3fdbc7lmtCaMV'},
        #     {'number': 10, 'name': 'Levitating', 'artist': 'Dua Lipa ft. DaBaby', 'album_name': 'Levitating (feat. DaBaby)', 'album_cover': 'https://i.scdn.co/image/ab67616d0000485149caa4fc6f962057ba65576a', 'song_uri': 'spotify:track:463CkQjx2Zk1yXoBuierM9', 'artist_uri': 'spotify:artist:6M2wZ9GZgrQXHCFfjv46we', 'album_uri': 'spotify:album:04m06KhJUuwe1Q487puIud'},
        # ]
        self.launcher = 'app'
        self.root = Tk()
        self.root.title('Top Songs')
        # self.root.geometry('1000x1000')
        self.images = {
            'refresh': ImageTk.PhotoImage(Image.open('refresh(24).png')),
            'album_covers': [],
            'youtube': ImageTk.PhotoImage(Image.open('youtube.png').resize((30, 30)))
        }
        self.widgets = {}
        self.create_ui()
        
    def create_ui(self):
        """Create buttons and sections and add them to the GUI."""
        container = LabelFrame(self.root, bd=0)
        top_frame = LabelFrame(container, bd=3, relief=SUNKEN)
        title = Label(top_frame, text='Top Songs', font=self.LARGE_FONT)
        num_songs = Entry(top_frame, width=3, bd=3, font=self.SMALL_FONT)
        refresh_btn = Button(top_frame, bd=3, image=self.images['refresh'], command=self.refresh)
        launcher_btn = Button(top_frame, bd=3, text='Spotify App', font=self.SMALL_FONT, command=self.switch_launcher)
        
        bottom_frame = LabelFrame(self.root, relief=SUNKEN)
        hover_label = Label(bottom_frame, text='', font=self.SMALL_FONT, anchor=W)
        
        container.grid(row=0, column=0)
        top_frame.grid(row=0, column=0, padx=5, pady=5, sticky=W+E)
        title.grid(row=0, column=0, padx=75)
        num_songs.grid(row=0, column=1, padx=0)
        num_songs.insert(0, self.DEFAULT_NUM_SONGS)
        refresh_btn.grid(row=0, column=2, padx=15)
        launcher_btn.grid(row=0, column=3, padx=15)
        
        bottom_frame.grid(row=2, column=0, padx=5, pady=5, sticky=W+E)
        hover_label.grid(row=0, column=0)
        
        self.widgets['top_frame'] = top_frame
        self.widgets['title'] = title
        self.widgets['num_songs'] = num_songs
        self.widgets['refresh_btn'] = refresh_btn
        self.widgets['launcher_btn'] = launcher_btn
        
        self.widgets['bottom_frame'] = bottom_frame
        self.widgets['hover_label'] = hover_label
        self.widgets['song_frames'] = []
        
        self.create_scrollable_frame()
        self.create_song_widgets()
    
    def create_scrollable_frame(self, remove=False):
        if remove:
            self.widgets['middle_frame_outer'].grid_forget()
            self.widgets['canvas'].grid_forget()
            self.widgets['scrollbar'].grid_forget()
            self.widgets['middle_frame_inner'].grid_forget()
            
        middle_frame_outer = LabelFrame(self.root, bd=3, relief=SUNKEN)
    
        canvas = Canvas(middle_frame_outer, height=441)
        scrollbar = ttk.Scrollbar(middle_frame_outer, orient=VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda event: canvas.configure(scrollregion=canvas.bbox('all')))
        middle_frame_inner = Frame(canvas)
        self.root.bind_all('<MouseWheel>', self.scroll)
        canvas.create_window((0, 0), window=middle_frame_inner, anchor=N + W)

        middle_frame_outer.grid(row=1, column=0, padx=5, pady=5, sticky=W + E)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.widgets['middle_frame_outer'] = middle_frame_outer
        self.widgets['canvas'] = canvas
        self.widgets['scrollbar'] = scrollbar
        self.widgets['middle_frame_inner'] = middle_frame_inner
    
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
        middle_frame_inner = self.widgets['middle_frame_inner']
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
            song_frame = LabelFrame(middle_frame_inner, bd=3, relief=RAISED)
            name_btn = Button(song_frame, width=max_name_length, bd=0, text=shortened_name, padx=10, anchor=W, font=self.SMALL_FONT)
            artist_btn = Button(song_frame, width=max_artist_length + 5, bd=0, text=shortened_artist, padx=10, anchor=W, font=self.SMALL_FONT)
            album_btn = Button(song_frame, bd=0, image=self.images['album_covers'][x])
            youtube_btn = Button(song_frame, bd=0, image=self.images['youtube'])
            # Add uri attributes to buttons to be accessed in open_spotify_uri and open_music_video (weird errors with lambda)
            name_btn.uri = song['song_uri']
            artist_btn.uri = song['artist_uri']
            album_btn.uri = song['album_uri']
            youtube_btn.song_name, youtube_btn.artist = song['name'], song['artist']
            # Bind open functions to buttons. Also, cool line length effect.
            name_btn.bind('<Button-1>', self.open_spotify_uri)
            album_btn.bind('<Button-1>', self.open_spotify_uri)
            artist_btn.bind('<Button-1>', self.open_spotify_uri)
            youtube_btn.bind('<Button-1>', self.open_music_video)
            # Add buttons and frame to bottom frame.
            song_frame.grid(row=x, column=0, padx=6, pady=3, sticky=W+E)
            name_btn.grid(row=0, column=0)
            artist_btn.grid(row=0, column=1)
            album_btn.grid(row=0, column=2, padx=10)
            youtube_btn.grid(row=0, column=3, padx=10)
            # Attach hover message to buttons.
            name_btn.message = song['name']
            artist_btn.message = song['artist']
            album_btn.message = song['album_name']
            youtube_btn.message = f'{song["name"]} Music Video'
            # Bind hover event to buttons to display info    .
            name_btn.bind('<Enter>', self.button_hover)
            artist_btn.bind('<Enter>', self.button_hover)
            album_btn.bind('<Enter>', self.button_hover)
            youtube_btn.bind('<Enter>', self.button_hover)
            # Bind leave event to buttons to clear info panel.
            name_btn.bind('<Leave>', self.button_leave)
            artist_btn.bind('<Leave>', self.button_leave)
            album_btn.bind('<Leave>', self.button_leave)
            youtube_btn.bind('<Leave>', self.button_leave)
            
            self.widgets['song_frames'].append(song_frame)
            print('Button created')
    
    def switch_launcher(self):
        button = self.widgets['launcher_btn']
        top_frame = self.widgets['top_frame']
        if self.launcher == 'app':
            self.launcher = 'website'
            btn_text = 'Spotify Website'
        else:
            self.launcher = 'app'
            btn_text = 'Spotify App'
        button.grid_forget()
        button = Button(top_frame, bd=3, text=btn_text, font=self.SMALL_FONT, command=self.switch_launcher)
        button.grid(row=0, column=3, padx=15)
        self.widgets['launcher_btn'] = button

    def scroll(self, event):
        canvas = self.widgets['canvas']
        canvas.yview_scroll(-1 * (event.delta // 30), 'units')
    
    def refresh(self):
        """Set number of songs to number entered, get songs, and re-create song buttons."""
        try:
            self.num_songs = int(self.widgets['num_songs'].get())
        except ValueError:
            self.widgets['num_songs'].delete(0, END)
            self.widgets['num_songs'].insert(0, self.num_songs)
        self.songs = self.get_top_songs()
        self.create_scrollable_frame(remove=True)
        self.create_song_widgets(remove=True)

    def button_hover(self, event):
        """Update hover_label with message."""
        button = event.widget
        hover_label = self.widgets['hover_label']
        hover_label.config(text=button.message)
    
    def button_leave(self, event):
        hover_label = self.widgets['hover_label']
        hover_label.config(text='')
    
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
            artist = song.find('span', class_='chart-element__information__artist').text.replace('Featuring', 'ft.').replace(' x ', ', ').replace(' & ', ', ').replace(' X ', ', ')
            album_name, album_cover, song_uri, artist_uri, album_uri = self.get_spotify_data(name, artist)
            
            songs.append({
                'number': number,
                'name': name,
                'artist': artist,
                'album_name': album_name,
                'album_cover': album_cover,
                'song_uri': song_uri,
                'artist_uri': artist_uri,
                'album_uri': album_uri
            })
        return songs
    
    @staticmethod
    def get_real_artist(artist):
        """Return an artist string with featured artists removed."""
        if ' ft.' in artist:
            return artist[:artist.find(' ft.')]
        return artist
    
    def get_spotify_data(self, song_name, artist):
        """
        Search for a track using the Spotify API and return its
        album name, the smallest version of the album's cover art,
        and the song, artists, and album uris.
        :param song_name: Song Name
        :param artist: Artist
        :return: album_name, album_cover, song_uri, artist uri, album_uri
        """
        real_artist = self.get_real_artist(artist)
        print(song_name + ' ' + real_artist)
        # Send request to Spotify's API and sift through json to find desired data.
        result = self.sp_api.search(q=f'{song_name} {real_artist}', type='track', limit=1)
        album_name = result['tracks']['items'][0]['album']['name']
        album_cover = result['tracks']['items'][0]['album']['images'][-1]['url']
        song_uri = result['tracks']['items'][0]['uri']
        artist_uri = result['tracks']['items'][0]['artists'][0]['uri']
        album_uri = result['tracks']['items'][0]['album']['uri']
        # TODO: more artists
        return album_name, album_cover, song_uri, artist_uri, album_uri
        
    def open_music_video(self, event):
        """
        Search for videos including song name and artist using Youtube API
        and open the top result, which will hopefully be the music video.
        :param event: stores button that was pressed, used to access song name & artist.
        """
        button = event.widget
        song_name = button.song_name
        artist = button.artist
        real_artist = self.get_real_artist(artist)
        # Send a request to Google's API and sift through json to find video url
        result = self.yt_api.search().list(q=f'{song_name} {real_artist}', maxResults=1, part='snippet', type='video').execute()
        video_id = result['items'][0]['id']['videoId']
        channel_title = result['items'][0]['snippet']['channelTitle']
        url = f'https://www.youtube.com/watch?v={video_id}&ab_channel={channel_title}'
        open(url)
    
    def open_spotify_uri(self, event):
        button = event.widget
        uri = button.uri
        uri_type, uri_id = uri.split(':')[1], uri.split(':')[2]
        if self.launcher == 'app':
            os.system(f'spotify --uri={uri}')
        else:
            webbrowser.open(f'https://open.spotify.com/{uri_type}/{uri_id}')
    
    def run(self):
        """Start app."""
        self.root.mainloop()


if __name__ == '__main__':
    TopSongsApp().run()

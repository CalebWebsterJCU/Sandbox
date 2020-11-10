import os
import shutil

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.properties import StringProperty, NumericProperty
from kivy.core.window import Window

GAMES_DIR = r'C:\Users\Caleb Webster\Desktop\Games'
IMAGES_DIR = r'C:\Users\Caleb Webster\Desktop\Images'
COLUMNS = 5
ROW_HEIGHT = 230


class SectionLabel(Label):
    pass


class ButtonBox(AnchorLayout, Button):
    pass


class GameLabel(Label):
    pass


class GamesMenu(App):
    games_box_height = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        os.chdir(GAMES_DIR)

    def build(self):
        Window.size = (1280, 720)
        self.root = Builder.load_file('games_menu_gui.kv')
        self.show_buttons()
        return self.root

    def show_buttons(self):
        self.root.ids.games_box.clear_widgets()
        self.games_box_height = 0
        print(os.listdir('.'))
        for folder in os.listdir('.'):
            images = self.load_images(folder)
            print(os.listdir(folder))
            games = self.get_games(folder)
            games_count = len(games)
            # Create section name label and section grid layout
            section_name = SectionLabel(text=folder, size_hint_y=0.1)
            rows, columns, height = self.calc_section_dimensions(folder)
            section = GridLayout(cols=columns, rows=rows, row_default_height=ROW_HEIGHT, row_force_default=True, size_hint_y=None, height=height, spacing=10)
            print('Section created')
            # Create button for each game in folder
            for x in range(len(games)):
                container = BoxLayout(orientation="vertical")
                image = Image(source=images[0])
                button = ButtonBox()
                name = GameLabel(text=games[x][:-4])
                favourite = Button(text="F", size_hint=(0.2, 0.2), on_release=self.fav_or_unfav)

                image_anchor = AnchorLayout(anchor_x="left", anchor_y="top")
                favourite_anchor = AnchorLayout(anchor_x="right", anchor_y="top")

                button.folder = folder
                button.game = games[x]

                favourite.folder = folder
                favourite.game = games[x]

                image_anchor.add_widget(image)
                favourite_anchor.add_widget(favourite)

                # button.add_widget(image)
                # button.add_widget(favourite)
                button.add_widget(image_anchor)
                button.add_widget(favourite_anchor)

                container.add_widget(button)
                container.add_widget(name)

                section.add_widget(container)
            # Add empty buttons to fill row
            print(f"Games in {folder}: {games_count}")
            while games_count % columns != 0:
                section.add_widget(Label())
                games_count += 1
            self.games_box_height += height + section_name.height
            self.root.ids.games_box.add_widget(section_name)
            self.root.ids.games_box.add_widget(section)
            print('Section added')

    def fav_or_unfav(self, instance):
        """Move game to favorites folder."""
        folder = instance.folder
        filename = instance.game
        if folder != "Favourites":
            os.chdir(GAMES_DIR)
            shutil.copy(rf"{GAMES_DIR}\{folder}\{filename}", rf"{GAMES_DIR}\Favourites\{filename}")
            shutil.copy(rf"{IMAGES_DIR}\{folder}\{filename[:-4]}.png", rf"{IMAGES_DIR}\Favourites\{filename[:-4]}.png")
        else:
            os.remove(rf"{GAMES_DIR}\{folder}\{filename}")
            os.remove(rf"{IMAGES_DIR}\{folder}\{filename[:-4]}.png")
        self.show_buttons()

    @staticmethod
    def load_images(folder):
        """Get images from folder and add them to a list."""
        images = []
        os.chdir(IMAGES_DIR)
        for image in os.listdir(folder):
            images.append(rf"{IMAGES_DIR}\{folder}\{image}")
        return images

    def calc_section_dimensions(self, folder):
        """Set the number of games grid rows to fit all games."""
        columns = COLUMNS
        games = self.get_games(folder)
        if len(games) > columns:
            rows = round(len(games) / columns)
        else:
            rows = 1
        height = rows * (ROW_HEIGHT + 10) - 10
        print(rows, columns, height)
        return rows, columns, height

    @staticmethod
    def run_game(instance):
        """
        Open a game's shortcut when game button is pressed.
        game filename is accessed from instance.game
        :param instance: the button that was pressed
        """
        folder = instance.folder
        filename = instance.game
        os.chdir(GAMES_DIR)
        os.startfile(rf"{folder}\{filename}")

    @staticmethod
    def get_games(folder):
        os.chdir(GAMES_DIR)
        return os.listdir(folder)

    @staticmethod
    def find_lpi(filename):
        """
        Find the index of the last period in a filename,
        indicating the beginning of the file extension
        :param filename: name of file to examine
        :return: integer value of index of last period
        """
        if filename and '.' in filename:
            i = -1
            while filename[i] != '.':
                i -= 1
            return i
        return 0


GamesMenu().run()

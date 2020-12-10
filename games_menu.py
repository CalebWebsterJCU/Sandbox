import os
import math
import shutil

from kivy.config import Config

Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 320)
Config.set('graphics', 'top', 180)

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.properties import StringProperty, NumericProperty
from kivy.core.window import Window

GAMES_DIR = "Games"
IMAGES_DIR = "Images"
STARS = ("star_gold.png", "star_black.png")
COLUMNS = 6
ROW_HEIGHT = 190


class SectionLabel(Label):
    pass


class BoxButton(BoxLayout, Button):
    pass


class AnchorButton(AnchorLayout, Button):
    pass


class GameLabel(Label):
    pass


class GamesMenu(App):
    games_box_height = NumericProperty()
    info_text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.title = "Game Launcher"
        Window.size = (1280, 720)
        self.root = Builder.load_file('games_menu_gui.kv')
        self.info_text = "Welcome to Caleb Webster's Fantastic Game Launcher!"
        self.show_buttons()
        return self.root

    def show_buttons(self):
        self.root.ids.games_box.clear_widgets()
        self.games_box_height = 0
        for folder in os.listdir(GAMES_DIR):

            if folder == "Favourites":
                fav_star = STARS[0]
            else:
                fav_star = STARS[1]

            images = self.load_images(folder)
            games = self.get_games(folder)

            games_count = len(games)
            # Create section name label and section grid layout
            section_name = SectionLabel(text=folder, size_hint_y=0.1)
            rows, columns, height = self.calc_section_dimensions(folder)
            section = GridLayout(cols=columns, rows=rows, row_default_height=ROW_HEIGHT, row_force_default=True, size_hint_y=None, height=height, spacing=10)
            print('Section created')
            # Create button for each game in folder
            for x in range(games_count):
                container = BoxLayout(orientation="vertical")

                button = AnchorButton()

                image_anchor = AnchorLayout(anchor_x="left", anchor_y="top")
                favourite_anchor = AnchorLayout(anchor_x="right", anchor_y="top")

                image = Image(source=images[x])
                fav_img = Image(source=fav_star)
                favourite = BoxButton(size_hint=(0.2, 0.2), on_release=self.fav_or_unfav)
                name = GameLabel(text=games[x][:games[x].rfind('.')])

                button.folder = folder
                button.game = games[x]

                favourite.folder = folder
                favourite.game = games[x]
                favourite.add_widget(fav_img)

                image_anchor.add_widget(image)
                favourite_anchor.add_widget(favourite)

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

    def calc_section_dimensions(self, folder):
        """Set the number of games grid rows to fit all games."""
        columns = COLUMNS
        games = self.get_games(folder)
        if len(games) > columns:
            rows = math.ceil(len(games) / columns)
        else:
            rows = 1
        height = rows * (ROW_HEIGHT + 10) - 10
        print(rows, columns, height)
        return rows, columns, height

    def fav_or_unfav(self, instance):
        """Move game to favorites folder."""
        folder = instance.folder
        filename = instance.game
        if folder != "Favourites":
            print(os.listdir(rf"{GAMES_DIR}\Favourites"))
            if filename not in os.listdir(rf"{GAMES_DIR}\Favourites") or f"{filename[:filename.rfind('.')]}.png" not in os.listdir(rf"{IMAGES_DIR}\Favourites"):
                shutil.copy(rf"{GAMES_DIR}\{folder}\{filename}", rf"{GAMES_DIR}\Favourites\{filename}")
                shutil.copy(rf"{IMAGES_DIR}\{folder}\{filename[:filename.rfind('.')]}.png", rf"{IMAGES_DIR}\Favourites\{filename[:-4]}.png")
                self.info_text = f"{filename[:filename.rfind('.')]} added to favourites!"

            else:
                self.info_text = f"{filename[:filename.rfind('.')]} is already in favourites!"
        else:
            os.remove(rf"{GAMES_DIR}\{folder}\{filename}")
            os.remove(rf"{IMAGES_DIR}\{folder}\{filename[:filename.rfind('.')]}.png")
            self.info_text = f"{filename[:filename.rfind('.')]} removed from favourites!"
        self.show_buttons()

    @staticmethod
    def load_images(folder):
        """Get images from folder and add them to a list."""
        images = []
        for image in os.listdir(rf"{IMAGES_DIR}\{folder}"):
            images.append(rf"{IMAGES_DIR}\{folder}\{image}")
        return images

    @staticmethod
    def run_game(instance):
        """
        Open a game's shortcut when game button is pressed.
        game filename is accessed from instance.game
        :param instance: the button that was pressed
        """
        folder = instance.folder
        filename = instance.game
        os.startfile(rf"{GAMES_DIR}\{folder}\{filename}")

    @staticmethod
    def get_games(folder):
        """
        Return a list of the games in a directory.
        :param folder: directory to search
        :return: list of games
        """
        return os.listdir(rf"{GAMES_DIR}\{folder}")


    @staticmethod
    def rgba_to_percent(rgba):
        """
        Convert rgba values to decimal percentages of 255.
        percentages are rounded to three decimal places.
        rgba values must be passed in as tuple: (R, G, B, A)
        :return: tuple of values as decimal percentages
        """
        values = []
        for value in rgba:
            values.append(round(value / 255, 3))
        print(f"RGBA: {values}")
        return tuple(values)


GamesMenu().run()

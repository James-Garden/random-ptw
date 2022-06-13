import sys
from io import BytesIO
from tkinter import Tk, Label, Entry, StringVar, Button, messagebox
from http.client import HTTPResponse
from random_ptw import get_list_page, get_anime_list, ListEntry
from PIL import ImageTk, Image
from urllib.request import urlopen
from urllib.error import HTTPError


class App(Tk):
    def __init__(self, username: str, list_page: HTTPResponse):
        super().__init__()
        self.title = f"{username}'s Anime List"
        self.anime_list = get_anime_list(list_page)

        # TKINTER GRID CONFIG

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # TKINTER ELEMENTS CREATION

        # Image
        self.image = self.get_anime_image()
        self.anime_image = Label(image=self.image)
        # English Title
        self.anime_title_text = StringVar()
        self.anime_title_text.set("ENG ANIME TITLE")
        self.anime_title_entry = Entry(textvariable=self.anime_title_text, state="readonly", width=105,
                                       justify='center')
        # Japanese Title
        self.anime_title_text_jp = StringVar()
        self.anime_title_text_jp.set("JP ANIME TITLE")
        self.anime_title_jp_entry = Entry(textvariable=self.anime_title_text_jp, state="readonly", width=105,
                                          justify='center')
        # Score
        score_label = Label(text="MAL Rating")
        self.score_text = StringVar()
        self.score_text.set("4.20")
        score_entry = Entry(textvariable=self.score_text, state="readonly", width=4, justify='center')
        # Number of episodes
        num_episodes_label = Label(text="Number of Episodes")
        self.episode_num_text = StringVar()
        self.episode_num_text.set("25")
        num_episodes_entry = Entry(textvariable=self.episode_num_text, state="readonly", width=4, justify='center')
        # Added to PTW on
        added_label = Label(text="Date Added to List")
        self.added_text = StringVar()
        self.added_text.set("04/20/22")
        added_entry = Entry(textvariable=self.added_text, state="readonly", width=8, justify='center')
        # Airing status
        airing_label = Label(text="Airing Status")
        self.airing_text = StringVar()
        self.airing_text.set("Currently Airing")
        airing_entry = Entry(textvariable=self.airing_text, state="readonly", width=16, justify='center')
        # MPAA Rating
        age_label = Label(text="Age Rating")
        self.age_text = StringVar()
        self.age_text.set("PG-13")
        age_entry = Entry(textvariable=self.age_text, state="readonly", width=6, justify='center')
        # Random button
        random_btn = Button(text="Get Random Anime!", command=self.random_entry)

        # TKINTER ELEMENT PLACEMENT

        self.anime_image.grid(column=0, row=0, rowspan=10, padx=5, pady=5)
        self.anime_title_entry.grid(column=1, columnspan=2, row=0, padx=5, pady=5)
        self.anime_title_jp_entry.grid(column=1, columnspan=2, row=1, padx=5, pady=5)
        score_label.grid(column=1, row=2, pady=5, padx=5)
        score_entry.grid(column=2, row=2, pady=5, padx=5)
        num_episodes_label.grid(column=1, row=3, pady=5, padx=5)
        num_episodes_entry.grid(column=2, row=3, pady=5, padx=5)
        added_label.grid(column=1, row=4, pady=5, padx=5)
        added_entry.grid(column=2, row=4, pady=5, padx=5)
        airing_label.grid(column=1, row=5, pady=5, padx=5)
        airing_entry.grid(column=2, row=5, pady=5, padx=5)
        age_label.grid(column=1, row=6, pady=5, padx=5)
        age_entry.grid(column=2, row=6, pady=5, padx=5)
        random_btn.grid(column=1, columnspan=2, row=7, pady=5, padx=5)

        self.after(0, self.random_entry)

    def random_entry(self):
        new_entry = self.anime_list.get_random()
        new_len = max(len(new_entry.anime_title), len(new_entry.anime_title_jp))
        self.anime_title_text.set(new_entry.anime_title)
        self.anime_title_text_jp.set(new_entry.anime_title_jp)
        self.anime_title_entry.config(width=new_len)
        self.anime_title_jp_entry.config(width=new_len)
        self.image = self.get_anime_image(new_entry.image_url)
        self.anime_image.config(image=self.image)
        self.score_text.set(str(new_entry.community_score))
        self.episode_num_text.set(str(new_entry.num_episodes))
        self.added_text.set(new_entry.date_added_to_list.strftime("%d/%m/%y"))
        self.airing_text.set(new_entry.get_airing_status())
        self.age_text.set(new_entry.mpaa_rating)

    @staticmethod
    def get_anime_image(image_url: str = None) -> ImageTk:
        try:
            img_response = urlopen(image_url)
            if img_response.getcode() != 200:
                raise HTTPError
            img_data = img_response.read()
            image = Image.open(BytesIO(img_data))
        except (HTTPError, AttributeError):
            image = Image.open('./image404.png')
        element = ImageTk.PhotoImage(image)
        return element


class UserUI(Tk):
    def __init__(self):
        super().__init__()
        self.response = None
        self.username = None
        self.username_text = StringVar()
        self.title = "Enter Username"
        label = Label(self, text="MAL Username")
        label.pack(padx=5, pady=5)
        entry = Entry(self, textvariable=self.username_text)
        entry.pack(padx=5, pady=5)
        btn = Button(self, text="Get List", command=self.submit)
        btn.pack(padx=5, pady=5)

    def submit(self):
        entry = self.username_text.get()
        user_exists, response = get_list_page(entry)
        if response is None:
            messagebox.showerror(title="Error 404", message=f"User '{entry}' not found.")
        elif response.getcode() == 504:
            messagebox.showerror(title="Error 504",
                                 message=f"https://myanimelist.net appears to be unreachable at the moment")
            self.destroy()
        elif user_exists:
            self.response = response
            self.username = entry
            self.destroy()
        else:
            messagebox.showerror(title=f"Error {response.getcode()}",
                                 message=f"Unexpected error")


def get_list() -> (str, HTTPResponse):
    user_ui = UserUI()
    user_ui.mainloop()
    if user_ui.username is None:
        quit(0)
    return user_ui.username, user_ui.response


def start_app(user_name: str, http_response: HTTPResponse):
    app = App(user_name, http_response)
    app.mainloop()


if __name__ == "__main__":
    user, response = get_list()
    start_app(user, response)


from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from http.client import HTTPResponse
from json import loads
from datetime import datetime
from random import randint


class ListEntry:
    AIRING_STATUS = {1: "Currently Airing", 2: "Finished Airing", 3: "Not Yet Aired"}

    def __init__(self, added_date, anime_title, anime_title_jp, num_episodes, airing_status, community_score, image_url,
                 mpaa_rating, start_date_string, finish_date_string):
        self.date_added_to_list = datetime.fromtimestamp(added_date)
        self.anime_title = anime_title
        self.anime_title_jp = anime_title_jp
        self.num_episodes = num_episodes
        self.airing_status = airing_status
        self.community_score = community_score
        self.image_url = image_url
        self.mpaa_rating = mpaa_rating
        if self.airing_status == 3:
            self.start_date = None
            self.finish_date = None
        else:
            # For some reason dates can be returned in either format.
            # Why.
            # Thanks America!
            try:
                self.start_date = datetime.strptime(start_date_string, "%m-%d-%y")
                if finish_date_string is None:
                    self.finish_date = None
                else:
                    self.finish_date = datetime.strptime(finish_date_string, "%m-%d-%y")
            except ValueError:
                self.start_date = datetime.strptime(start_date_string, "%d-%m-%y")
                if finish_date_string is None:
                    self.finish_date = None
                else:
                    self.finish_date = datetime.strptime(finish_date_string, "%d-%m-%y")

    def __repr__(self):
        return f"<{self.__class__.__name__}>: '{self.anime_title}'"

    def __str__(self):
        return self.anime_title

    def get_airing_status(self) -> str:
        return ListEntry.AIRING_STATUS[self.airing_status]


class AnimeList:
    def __init__(self):
        self.entries = []

    def add(self, entry: ListEntry):
        if not isinstance(entry, ListEntry):
            raise ValueError("May only add ListEntry objects to AnimeList")
        self.entries.append(entry)

    def get_random(self) -> ListEntry:
        if len(self.entries) == 0:
            return self.entries[0]
        return self.entries[randint(0, len(self.entries) - 1)]


def get_list_page(username: str) -> (bool, HTTPResponse):
    """
    Try to get the entered user's anime list:
    returns (True, response) only if the user's list page returned 200 OK,
    returns (False, None) if the user's list page returned 404 NOT FOUND,
    returns (False, response) for any other HTTP status code
    """

    try:
        response = urlopen(f"https://myanimelist.net/animelist/{username}?status=6")
        if response.getcode() == 200:
            return True, response
        if response.getcode() == 504:
            return False, response
        else:
            return False, response
    except HTTPError:
        return False, None


def get_anime_list(response: HTTPResponse) -> AnimeList:
    anime_list = AnimeList()
    soup = BeautifulSoup(response.read().decode(), features="html.parser")

    if soup is None:
        raise ValueError("Invalid HTTPResponse passed")

    table = soup.find("table", {"class": "list-table"})
    list_entries = loads(table.attrs.get("data-items"))
    for entry in list_entries:
        list_entry = ListEntry(entry['created_at'],
                               entry['anime_title_eng'],
                               entry['anime_title'],
                               entry['anime_num_episodes'],
                               entry['anime_airing_status'],
                               entry['anime_score_val'],
                               entry['anime_image_path'],
                               entry['anime_mpaa_rating_string'],
                               entry['anime_start_date_string'],
                               entry['anime_end_date_string'])
        anime_list.add(list_entry)

    return anime_list

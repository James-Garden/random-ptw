# random-ptw
Three scripts for selecting a random anime from a MAL user's 'Plan to Watch' list

***
### random_ptw.py

Two classes and two functions, backend logic for retrieving a MAL user's PTW
* *get_list_page* - takes a MAL username as its only argument, and returns a tuple containing:
    * *bool* - True if the page was retrieved successfully, False otherwise
    * *HTTPResponse* - None if entered user's list page returned 404, HTTPResponse containing the users' PTW page otherwise

* *get_anime_list* - takes a HTTPResponse of a user's anime list as its only argument, returns an AnimeList object of the user's anime list
  * Raises a ValueError if the input HTTPResponse is invalid 
* **ListEntry** - a single entry from a user's anime list, takes 10 constructor arguments
  * *get_airing_status* - returns a string representing the airing status of an entry from: "Currently Airing", "Not Yet Aired", and "Finished Airing"
* **AnimeList** - representation of a user's anime list, takes no constructor arguments
  * *add* - append a **ListEntry** to this object, equivalent to append, but checks if the added object is of type **ListEntry**
  * *get_random* - returns a **ListEntry** at random from this object

***
### random_ptw_gui.py

Main method, two classes and two functions for creating a GUI for presenting a random anime from *random_ptw.py*

* *get_list* - starts GUI for getting username, returns *str* of their username and a *HTTPResponse* of their anime list
* *start_app* - takes *str* of username and *HTTPResponse* of anime list and starts the main GUI
* **UserUI** - Tkinter GUI for getting a user's username, takes no constructor arguments
* **App** - Main Tkinter application for getting random Anime, takes two constructor arguments
  * *str* - of the user's MAL username
  * *HTTPResponse* - of the user's anime list
  * Has the following methods:
    * *random_entry* - replaces the current entry info with a random new one in the GUI
    * *get_anime_image* - takes an image URL as its only argument, returns an ImageTk object produced from that image, or a placeholder image


***
### random_ptw.old.py

Old, unreadable, unfriendly and slow version of this script (don't use this). 

***
### Assets
* *image404.png* - image displayed by *random_ptw_gui.py*'s App if no image is found
# Chronica
This application is a media tracker that allows users to search for movies and TV shows via The Movie Database API (TMDB). Users can leave reviews on items as well as add items to user created lists.

## Distinctiveness and Complexity
This project interacts with an external API (TMDB), as well as an internal API to allow the front-end JavaScript to make changes to the database, specifically to the Media and List models. Prior projects in this course, if they featured an API, were only internal such as the mail project. This created an additional level of complexity because it required handling external requests and understanding the proper authentication to allow the requests to pass through. 

Other projects in this course only had the user interact with one type of item such as an email, auction post, or social network post, but this project had to be developed with multiple interactive items in mind: media items (TV shows and movies), and lists. The level of interaction between these objects is also increased compared to previous projects. For instance, in this application, results are loaded from TMDB and displayed for the user to view, similarly to the commerce project. In the commerce project, users could add certain posts to a watchlist, as well as comment on the posts themselves. However, this project allows users to not only comment on media items via reviews, but also allows users to add media items to more than one list. Through front-end JavaScript code, users can also alter features about the list, such as its title and description, as well as create or delete lists. The complexity required to accomplish this interaction exceeds the complexity of previous projects, as the info from TMDB had to first be converted to a model in the local database (Media model) before being able to interact with it to ensure that the Review and List models would have an appropriate key to reference. Prior projects only have the user generate all the information about a particular Django model themselves.

Conceptually, this project is also distinguished from other projects in this course. Previous projects include a search page front end, a wiki, a commerce website, an email client front-end, and a Twitter-like social media network. This web application is most similar to websites such as IMDB where a user can view details about a movie or TV show and leave reviews, and is therefore distinct from other projects in this course as it does not involve models with similar functions as previous projects nor does it have a similar purpose to any of them.

## Created Files
<ins>tracker</ins>
forms.py
Contains ModelForms for creating reviews and lists.

<ins>static\tracker</ins>
- content.js
    Contains JavaScript to load results from The Movie Database API for a given search query (either for books or movies)
- info.js
    Contains JavaScript to allow users to add a specific media item to a list of their choice. A list can have both TV shows and movies on it.
- list.js
    Contains JavaScript to allow users to edit the title or description of a specific list.
- seasons.js
    Contains JavaScript to display the info for all seasons of a specific TV show.
- styles.css
    Contains style code for the HTML files.

<ins>templates\tracker</ins>
- content.html
    Contains page for viewing search results for both books and movies.
- error.html
    Contains page for when an invalid user and/or list is provided in the url.
- index.html
    Opening page of the web application. Contains currently trending movies and TV shows.
- info.html
    Contains page for viewing the details of a specific movie or TV show.
- layout.html
    Layout page that all other .html files inherit.
- list.html
    Contains page for viewing a list. Includes all items within the list and allows the user to delete the list. The corresponding file list.js allows for the title and description of lists to be edited.
- login.html
    Contains page for allowing a user to log in (sourced from previous projects in this course).
- register.html
    Contains page for allowing a user to register for an account (sourced from previous projects in this course).
- reviewed.html
    Contains page for viewing all media items that the user has already reviewed.
- seasons.html
    Contains page with all buttons for viewing each season. Front-end functionality for actually generating the displays is found in seasons.js.
- user_lists.html
    Contains page with all lists created by a specific user. Allows user to create new lists.

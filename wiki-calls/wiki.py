import random
import requests

import category_lists


def get_random_category(options: list = category_lists.categories) -> tuple[str, list[str]]:
    r_category_name, r_category = random.choice(options)
    return r_category_name, r_category


def get_random_search_title(r_category: list[str]) -> str:
    return random.choice(r_category)


def get_search_parameters(r_search_choice: str) -> dict[str, str | int]:
    search_parameters = {
        "action": "query",              # Fetch data from and about MediaWiki https://en.wikipedia.org/w/api.php?action=help&modules=query
        "titles": r_search_choice,      # exact title search [see "query"]
        "prop": "extracts|pageimages",  # Returns plain-text or limited HTML extracts of the given pages https://en.wikipedia.org/w/api.php?action=help&modules=query%2Bextracts
                                        # Returns information about images on the page, such as thumbnail and presence of photos https://en.wikipedia.org/w/api.php?action=help&modules=query%2Bpageimages
        "piprop": "original",           # URL and dimensions of thumbnail image associated with page, if any [see "pageimages"]
        "explaintext": 1,               # Return extracts as plain text instead of limited HTML. [see "extracts"]
        "redirects": 1,                 # Automatically resolve redirects in query+titles, query+pageids, and query+revids, and in pages returned by query+generator [see "query"] explanation: if title links you to the main article, it follows it automatically(once)
        "format": "json",               # formats as json https://en.wikipedia.org/w/api.php?action=help&modules=json
        "formatversion": 2              # Modern format. [see "json"]
    }
    return search_parameters


def get_response_arguments(search_parameters: dict[str, str | int]) -> tuple:
    wikipedia = "https://en.wikipedia.org/w/api.php"
    params = search_parameters
    header = {"User-Agent": "become_the_mvp_app (become.the.mvp@gmail.com)"}
    return wikipedia, params, header


def get_data_from_wikipedia(response_arguments: tuple[str, dict, dict]) -> dict:
    wikipedia, params, header = response_arguments
    response = requests.get(
        wikipedia,
        params=params,
        headers=header
    )
    response.raise_for_status()  # raises Error if denied (try|except) later
    return response.json() # wiki_data


def provide_backup_picture() -> tuple[str, tuple[int, int]]:
    backup_picture = "https://static.wikia.nocookie.net/antagonisten/images/a/ab/Joker-2008-portrait-b.png/revision/latest?cb=20210107165218&path-prefix=de"
    backup_picture_dimensions_wh = 610, 593 #  future update, fetch automatically from url
    return backup_picture, backup_picture_dimensions_wh


def create_data_parts(wiki_data: dict, backup_picture: tuple[str, tuple[int, int]]) -> tuple:
    wiki_article = wiki_data["query"]["pages"][0]
    try:
        article_picture = wiki_article["original"]["source"]
        picture_dimensions_wh = (wiki_article["original"]["width"], wiki_article["original"]["height"])
    except KeyError:
        backup_picture, backup_picture_dimensions_wh = backup_picture
        article_picture = backup_picture
        picture_dimensions_wh = backup_picture_dimensions_wh
    article_title = wiki_article["title"]
    full_article = wiki_article["extract"].split("\n\n\n== See also")[0]
    article_header = full_article.split("==")[0]
    return article_picture, picture_dimensions_wh, article_title, full_article, article_header  # return as data_parts


def create_article_dict(data_parts: tuple[str]) ->  dict[str, str | tuple[int, int]]:
    article_picture, picture_dimensions_wh, article_title, full_article, article_header = data_parts
    article_dict = {
        "title": article_title,
        "picture_url": article_picture,
        "picture_dimensions": picture_dimensions_wh,
        "header": article_header,
        "full_article": full_article
    }
    return article_dict


def handle_wikipedia():
    r_category_name, r_category = get_random_category()
    r_search_title = get_random_search_title(r_category)

    search_parameters = get_search_parameters(r_search_title)
    response_arguments = get_response_arguments(search_parameters)
    wiki_data = get_data_from_wikipedia(response_arguments)

    backup_picture = provide_backup_picture()
    data_parts = create_data_parts(wiki_data, backup_picture)
    article_dict = create_article_dict(data_parts)
    return article_dict
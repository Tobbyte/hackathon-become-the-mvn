import requests
from datetime import datetime
import random

from wiki_calls import config


def _get_previous_month_with_year() -> tuple[int, int]:
    """Return the previous month and its corresponding year."""
    current_date = datetime.now()

    previous_month = current_date.month - 1
    current_year = current_date.year

    if previous_month == 0:
        previous_month = 12
        current_year -= 1

    return previous_month, current_year


def _create_top_pages_url(year: int, month: int) -> str:
    """Create the Wikimedia URL for the monthly top pages."""
    return (
        "https://wikimedia.org/api/rest_v1/metrics/pageviews/top/"
        f"en.wikipedia.org/all-access/{year}/{month:02d}/all-days"
    )


def _get_top_page_data_from_wikipedia(url: str) -> dict:
    """Request and return the monthly top-page data."""
    headers = {
        "User-Agent": "become_the_mvp_app (become.the.mvp@gmail.com)"
    }
    response = requests.get(
        url,
        headers=headers,
    )
    response.raise_for_status()  # raises Error if denied (try|except) later

    return response.json()


def _get_top_pages(pageviews_data: dict) -> list[str]:
    """Extract the top-page entries from the pageview data."""
    top_pages = pageviews_data["items"][0]["articles"]
    return top_pages


def _filter_top_pages(top_pages: list[dict]) -> list[dict]:
    """Remove non-article pages from the pageview results."""
    excluded_pages = {
        "Main_Page",
    }

    excluded_prefixes = (
        "Special:",
        "Wikipedia:",
        "Portal:",
        "File:",
        "Help:",
        "Event:",
        "List_of_",
    )

    filtered_pages = []

    for page in top_pages:
        article_title = page["article"]

        if (
            article_title not in excluded_pages
            and not article_title.startswith(excluded_prefixes)
        ):
            filtered_pages.append(page)

    return filtered_pages


def _get_top_page_titles(filtered_pages: list[dict]) -> list[str]:
    """Extract the article titles from the filtered page entries."""
    page_titles = []

    for page in filtered_pages:
        article_title = page["article"]
        page_titles.append(article_title)

    return page_titles


def _get_titles_by_difficulty(page_titles: list[str], user_difficulty: str) -> list[str]:
    """Return the article titles for the selected difficulty."""
    for difficulty, start, end in config.DIFFICULTIES_TOP:
        if difficulty == user_difficulty:
            return page_titles[start:end]


def _get_random_title(titles: list[str]) -> str:
    """Return a random title from the given list."""
    r_search_choice = random.choice(titles)
    return r_search_choice


def get_top_wikipedia_title(user_difficulty: str) -> str:
    """Return a random top Wikipedia title for the selected difficulty."""
    month, year = _get_previous_month_with_year()
    url = _create_top_pages_url(year, month)
    pageviews_data = _get_top_page_data_from_wikipedia(url)
    top_pages = _get_top_pages(pageviews_data)
    filtered_pages = _filter_top_pages(top_pages)
    page_titles = _get_top_page_titles(filtered_pages)
    titles = _get_titles_by_difficulty(page_titles, user_difficulty)
    r_search_choice = _get_random_title(titles)
    return r_search_choice
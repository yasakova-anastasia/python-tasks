import typing as tp
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# Directory to save your .json files to
# NB: create this directory if it doesn't exist
SAVED_JSON_DIR = Path(__file__).parent / 'visited_paths'


def distance(source_url: str, target_url: str, passed: tp.Any = {}, count: int = 0) -> int | None:
    """Amount of wiki articles which should be visited to reach the target one
    starting from the source url. Assuming that the next article is choosing
    always as the very first link from the first article paragraph (tag <p>).
    If the article does not have any paragraph tags or any links in the first
    paragraph then the target is considered unreachable and None is returned.
    If the next link is pointing to the already visited article, it should be
    discarded in favor of the second link from this paragraph. And so on
    until the first not visited link will be found or no links left in paragraph.
    NB. The distance between neighbour articles (one is pointing out to the other)
    assumed to be equal to 1.
    :param source_url: the url of source article from wiki
    :param target_url: the url of target article from wiki
    :return: the distance calculated as described above
    """
    if not passed:
        passed = {}

    response = requests.get(source_url, timeout=30)
    html = response.text
    soup = BeautifulSoup(html, features='lxml')
    links = soup.find('div', attrs={"class": "mw-parser-output"})
    links = links.findAll("p", recursive=False)[0].findAll("a")

    if source_url not in passed:
        passed[source_url] = count
        if source_url == target_url:
            return passed[source_url]

        for link in links:
            if 'href' not in link.attrs:
                continue
            if '#' in link['href']:
                continue
            if '.' in link['href']:
                continue

            url = "https://ru.wikipedia.org" + link["href"]
            if url in passed:
                continue

            distance(url, target_url, passed, count + 1)
            break

    if target_url in passed:
        return passed[target_url]
    else:
        return None

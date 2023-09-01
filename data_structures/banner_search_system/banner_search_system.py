import heapq
import string
import typing as tp


def normalize(
        text: str
        ) -> str:
    """
    Removes punctuation and digits and convert to lower case
    :param text: text to normalize
    :return: normalized query
    """
    result = "".join((x for x in text if not x.isdigit()))
    result = result.translate(dict.fromkeys(map(ord, string.punctuation)))
    return result.lower()


def get_words(
        query: str
        ) -> list[str]:
    """
    Split by words and leave only words with letters greater than 3
    :param query: query to split
    :return: filtered and split query by words
    """
    return [q for q in query.split() if len(q) > 3]


def build_index(
        banners: list[str]
        ) -> dict[str, list[int]]:
    """
    Create index from words to banners ids with preserving order and without repetitions
    :param banners: list of banners for indexation
    :return: mapping from word to banners ids
    """
    result: dict[str, list[int]] = {}
    for i, s in enumerate(banners):
        for word in get_words(normalize(s)):
            if word not in result:
                result[word] = []

            if not len(result[word]) or (len(result[word]) and result[word][-1] != i):
                result[word].append(i)

    return result


def get_banner_indices_by_query(
        query: str,
        index: dict[str, list[int]]
        ) -> list[int]:
    """
    Extract banners indices from index, if all words from query contains in indexed banner
    :param query: query to find banners
    :param index: index to search banners
    :return: list of indices of suitable banners
    """
    result = []
    heap: list[tp.Any] = []
    words = get_words(normalize(query))
    idx = 0
    for word in words:
        if index.get(word):
            heapq.heappush(heap, (index[word][0], idx, (index[word], 0)))
            idx += 1

    amount = 0
    val = -1
    while len(heap):
        if val == -1:
            val = heap[0][0]

        if val == heap[0][0]:
            amount += 1
        else:
            amount = 1
            val = heap[0][0]

        if amount == len(words):
            result.append(val)

        edge = heap[0]
        heapq.heappop(heap)

        if len(edge[2][0]) > edge[2][1] + 1:
            heapq.heappush(heap, (edge[2][0][edge[2][1] + 1], idx, (edge[2][0], edge[2][1] + 1)))
            idx += 1

    return result


#########################
# Don't change this code
#########################

def get_banners(
        query: str,
        index: dict[str, list[int]],
        banners: list[str]
        ) -> list[str]:
    """
    Extract banners matched to queries
    :param query: query to match
    :param index: word-banner_ids index
    :param banners: list of banners
    :return: list of matched banners
    """
    indices = get_banner_indices_by_query(query, index)
    return [banners[i] for i in indices]

#########################

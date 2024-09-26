"""
For a given URL, generate a short URL and retrieve the original by the generated one.
Input:
https://www.revolut.com/rewards-personalised-cashback-and-discounts/
Expected output:
https://www.rev.me/<url identifier>

Func req-s:
* in-memory, up to 100 urls
* TODO: consider url_encoded original urls https://www.revolut.com/rewards%33personalised-cashback-and-discounts/
* For a given URL, randomly pick the short URL from a predefined pool.
"""

# python3.12

import unittest, string, random
# use urllib to fetch hash from short_url


class CustomException(Exception):
    def __init__(self):
        self.add_note("first note")
        return super().__init__(self)


class URLShortener:
    MAX_URLS = 100
    MAX_SHORT_URL_LEN = 6
    DOMAIN_SHORT_URL_PATTERN = "https://www.rev.me/"

    def __init__(self, keys: list=None):
        self.keys = keys if keys else []
        self.short_to_url = {}
        self.url_map = {}

    def _generate_hash_collision_possible(self):
        char_set = string.ascii_letters + string.digits
        return ''.join(random.choices(char_set, k=self.MAX_SHORT_URL_LEN))

    def _get_from_keys(self):
        if self.keys:
            return random.choice(self.keys)

        raise ValueError("Keys list is empty")

    def shorten(self, original_url: str) -> str:
        if len(self.short_to_url) >= self.MAX_URLS:
            raise ValueError(f"Limit {self.MAX_URLS} has reached")

        short_url = self._generate_hash_collision_possible()
        while short_url in self.short_to_url:
            short_url = self._generate_hash_collision_possible()

        short_url = self.DOMAIN_SHORT_URL_PATTERN + short_url
        ### locked
        self.short_to_url[short_url] = original_url
        self.url_map[original_url] = short_url
        ### locked

        return short_url

    def retrieve(self, short_url: str) -> str:
        if not short_url in self.short_to_url:
            raise ValueError(f"Not found {short_url}")

        ### locked
        return self.short_to_url[short_url]
        ### locked


# move to tests folder
class TestURLShortener(unittest.TestCase):
    def setUp(self):
        self.shortener = URLShortener()

    def test_shorten(self):
        short_url = self.shortener.shorten("example.com")
        self.assertEqual(len(short_url),
                         self.shortener.MAX_SHORT_URL_LEN + len(self.shortener.DOMAIN_SHORT_URL_PATTERN))
        # pass int to random
        random.seed(101)
        #

    def test_retrieve(self):
        original_url = self.shortener.DOMAIN_SHORT_URL_PATTERN + "exampl"
        short_url = self.shortener.shorten(original_url)
        print(short_url)
        retrieved_url = self.shortener.retrieve(short_url)
        self.assertEqual(original_url, retrieved_url)

    def test_shorten_limit(self):
        for i in range(self.shortener.MAX_URLS):
            self.shortener.shorten(f"example{i}.com")

        with self.assertRaises(ValueError) as exc_info:
            self.shortener.shorten(f"example{i+1}.com")

        self.assertTrue("Limit" in str(exc_info.exception))

    def test_retrieve_not_found(self):
        with self.assertRaises(ValueError) as exc_info:
            self.shortener.retrieve("anydummyurl.com")

        self.assertTrue("Not found" in str(exc_info.exception))


# it ensures that keys are unique by tracking and storing them in memory
# it generates it
class KeyGenerator:
    MAX_POOL_LEN = 10_000

    def __init__(self):
        self.keys = {}
        self.current_idx = 0

    def get_key(self):
        pass


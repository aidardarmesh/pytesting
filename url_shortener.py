"""
System requirements:
*
"""


import unittest, random, string


class UrlShortener:
    def __init__(self, max_urls=100, max_url_len=6):
        self.max_urls = max_urls
        self.max_url_len = max_url_len
        self.url_map = {}
        self.short_to_url = {}

    def _generate_hash(self):
        char_set = string.ascii_letters + string.digits
        return ''.join(random.choices(char_set, k=self.max_url_len))

    def shorten(self, original_url):
        if len(self.url_map) >= self.max_urls:
            raise Exception(f"Limit of urls {self.max_urls} has reached")

        if original_url in self.url_map:
            return self.url_map[original_url]

        url_hash = self._generate_hash()
        while url_hash in self.short_to_url:
            url_hash = self._generate_hash()

        self.url_map[original_url] = url_hash
        self.short_to_url[url_hash] = original_url

        return url_hash

    def retrieve(self, short_url):
        if not short_url in self.short_to_url:
            raise KeyError(f"Short url {short_url} is not found")

        return self.short_to_url[short_url]


class TestUrlShortener(unittest.TestCase):
    def setUp(self):
        self.shortener = UrlShortener()

    def test_shorten(self):
        short_url = self.shortener.shorten("example.com")
        self.assertEqual(len(short_url), self.shortener.max_url_len)

    def test_original_url(self):
        original_url = "example1.com"
        short_url = self.shortener.shorten(original_url)
        retrieved_url = self.shortener.retrieve(short_url)
        self.assertEqual(original_url, retrieved_url)

    def test_url_not_found(self):
        with self.assertRaises(KeyError):
            self.shortener.retrieve("12345")

    def test_unique_urls(self):
        short_url1 = self.shortener.shorten("example1.com")
        short_url2 = self.shortener.shorten("example2.com")
        self.assertNotEqual(short_url1, short_url2)

    def test_max_urls_reached(self):
        for i in range(self.shortener.max_urls):
            self.shortener.shorten(f"example{i}.com")

        with self.assertRaises(Exception) as exc_info:
            self.shortener.shorten("example101.com")

        self.assertTrue("Limit" in str(exc_info.exception))

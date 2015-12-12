import unittest
from netblower import *


class TestPage(unittest.TestCase):

    def testCreate(self):
        url = 'test_url'
        content = '<p>content</p>'
        page = Page(url, content)
        self.assertEqual(url, page.url)
        self.assertEqual(content, page.content)


class TestPageGetter(unittest.TestCase):

    def setUp(self):
        self.url = 'https://github.com/jacob-bennett/netblower'
        self.page_getter = PageGetterMock(self.url)

    def testCreate(self):
        self.assertEqual(self.url, self.page_getter.url)

    def testGetPage(self):
        page = self.page_getter.getPage()
        self.assertIsInstance(page, Page)
        self.assertEqual('<html><body><p>test<a>link</a></p></body</html>', page.content)


class PageGetterMock(PageGetter):
    """Overrides __makeRequest method to return mock data"""
    def _makeRequset(self):
        return "<html><body><p>test<a>link</a></p></body</html>"

if __name__ == '__main__':
    unittest.main()
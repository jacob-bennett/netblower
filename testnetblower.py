import unittest
from unittest.mock import MagicMock
from netblower import *


class TestPage(unittest.TestCase):

    def test_create(self):
        url = 'test_url'
        content = '<p>content</p>'
        page = Page(url, content)
        self.assertEqual(url, page.url)
        self.assertEqual(content, page.content)


class TestPageGetter(unittest.TestCase):

    def setUp(self):
        self.url = 'https://github.com/jacob-bennett/netblower'

    def test_create(self):
        page_getter = PageGetter(self.url, MagicMock)
        self.assertEqual(self.url, page_getter.url)

    def test_get_page(self):
        example_html = "<html><body><p>test<a>link</a></p></body</html>"

        requester_response = MagicMock
        requester_response.read = MagicMock(return_value = example_html)
        requester = MagicMock(request)
        requester.urlopen = MagicMock(return_value = requester_response)

        page_getter = PageGetter(self.url, requester)
        page = page_getter.get_page()

        self.assertIsInstance(page, Page)
        self.assertEqual(example_html, page.content)
        requester.urlopen.assert_called_with(self.url)
        requester_response.read.assert_called_once_with()


class TestLinkExtractor(unittest.TestCase):

    def test_extract_links_from_page(self):
        extractor = LinkExtractor(LinkValidator())
        link1 = "http://test.com"
        link2 = "http://netblower.nb"
        page_content = self._generate_test_html_page(link1, link2)
        page = Page("", page_content)

        returned_links = extractor.extract_links_from_page(page)
        self.assertEquals(2, len(returned_links))
        self.assertIn(link1, returned_links)
        self.assertIn(link2, returned_links)

    def _generate_test_html_page(self, link1, link2):
        empty_link = "http://"
        invalid_link_1 = "http://bleh."
        invalid_link_2 = "http://blah"
        return (
        '<p>test' \
        '<a href="%s">link</a>' \
        '<a href="%s">test</a>' \
        '<a href="%s">I shouldn\'t be extracted</a>' \
        '<a href="%s">Nor should I</a>' \
        '<a href="%s">Nor I</a>' \
        '</p>'
        % (link1, link2, empty_link, invalid_link_1, invalid_link_2)
    )


class TestLinkValidator(unittest.TestCase):

    def test_remove_broken_links(self):
        link_validator = LinkValidator()
        number_of_valid_links = 1
        valid_link = "http://test.com"
        empty_link = "http://"
        broken_link_1 = "http://bleh."
        broken_link_2 = "http://bleh"
        links = [valid_link, empty_link, broken_link_1, broken_link_2]
        returned_links = link_validator.remove_broken_links(links)

        self.assertEqual(len(returned_links), number_of_valid_links)
        self.assertEqual(returned_links[0], valid_link)


if __name__ == '__main__':
    unittest.main()

from urllib import request


class Page:

    def __init__(self, url, content):
        self.url = url
        self.content = content


class PageGetter:

    def __init__(self, url, requester):
        self.url = url
        self.__requester = requester

    def get_page(self):
        content = self.__requester.urlopen(self.url).read()
        return Page(self.url, content)


class LinkValidator:

    def remove_broken_links(self, unvalidated_links):
        working_links = []
        for link in unvalidated_links:
            if self._link_is_valid(link):
                working_links.append(link)

        return working_links

    def _link_is_valid(self, link):
        if self._link_is_correct_length(link) and self._link_has_valid_country_code(link):
            return True

    def _link_is_correct_length(self, link):
        shortest_valid_url = "http://g.cn"
        if len(link) >= len(shortest_valid_url):
            return True

    def _link_has_valid_country_code(self, link):
        if self._country_code_exists(link) and self._country_code_is_in_correct_palce(link):
            return True

    def _country_code_exists(self, link):
        if "." in link:
            return True

    def _country_code_is_in_correct_palce(self, link):
        length_of_link = len(link) - 1
        country_code_position = link.rfind(".")
        if country_code_position > 1 and country_code_position < length_of_link:
            return True


class LinkExtractor:

    def __init__(self, link_validator: LinkValidator):
        self._links = []
        self._content = ""
        self._link_validator = link_validator

    def extract_links_from_page(self, page: Page):
        self._content = page.content
        self._extract_all_links()
        links = self._link_validator.remove_broken_links(self._links)
        return links

    def _extract_all_links(self):
        unextracted_links = self._get_broken_down_content()
        for unextracted_link in unextracted_links:
            self._extract_link(unextracted_link)

    def _get_broken_down_content(self):
        link_prefix = "<a "
        broken_down_content = self._content.split(link_prefix)
        return broken_down_content

    def _extract_link(self, content):
        link = self._find_link_in_content(content)
        self._links.append(link)

    def _find_link_in_content(self, content):
        link_prefix = 'href="'
        start_of_link = content.find(link_prefix) + len(link_prefix)
        end_of_link = content[start_of_link:].find('"') + start_of_link
        link = content[start_of_link:end_of_link]
        return link

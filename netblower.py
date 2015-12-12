from urllib import request


class Page:

    def __init__(self, url, content):
        self.url = url
        self.content = content


class PageGetter:

    def __init__(self, url):
        self.url = url

    def getPage(self):
        content = self._makeRequset()
        return Page(self.url, content)

    def _makeRequset(self):
        response = request.urlopen(self.url)
        return response.read()

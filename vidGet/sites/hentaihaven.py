import re
from bs4 import BeautifulSoup
from selenium import webdriver
from ..vidsite import vidSeries
from ..util import memorize, webpage

bs4 = BeautifulSoup
tags  = ['hh', 'hentaihaven']

class Series(vidSeries):
    siteTemplate   = 'http://hentaihaven.org{}'
    seriesTemplate = siteTemplate.format('/series/{}/?sort=title')

    def __init__(self, series, extras=None, cookie=None):
        self.cookie, self.name = cookie, series
        if extras:
            self.extras = extras.split(',')
            self.runExtras()
        self.br = webdriver.PhantomJS()
        self.br.get(self.url)

    def cleanup(self):
        self.br.close()
        self.br.quit()

    @property
    def pages(self):
        return [self.page(i.a['href'], self) for i in self.soup('div',
            class_='brick-content')]

    def runExtras(self):
        url_search, t = 'http://hentaihaven.org/search/{}', {}
        search = webpage(url_search.format(self.name))
        sel = search.soup('a', class_='series_title')
        for i in sel:
            hold = i.text
            if not hold in t.keys():
                t.update({hold: i['href']})
        final = t.items()
        print('Please select from the following:')
        for n, i in enumerate(final):
            print("{}: {}".format(n, i[0].encode('utf-8')))
        selection = input()
        self.name = final[selection][1].split('/')[-2]

    class page(vidSeries.page):

        @property
        @memorize
        def video(self):
            self.br.get(self.url)
            main = self.soup(class_='download_feed_link')[0]
            qual = main('a')
            return qual[0]['href']

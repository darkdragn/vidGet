import re
from bs4 import BeautifulSoup
from ..vidsite import vidSeries
from ..util import memorize, webpage

bs4 = BeautifulSoup
tags  = ['shm', 'streamhentaimovies']

class Series(vidSeries):
    siteTemplate   = 'http://www.streamhentaimovies.com{}'
    seriesTemplate = siteTemplate.format('/category/{}')

    @property
    def pages(self):
        return [self.page(i.a['href'], self) for i in
                self.soup('li', class_='item-video')[::-1]]

    def runExtras(self):
        url_search = self.siteTemplate.format('?s={}')
        search = webpage(url_search.format(self.name))
        sel = search.soup('a', class_='clip-link')
        print('Please select from the following:')
        t = {}
        for i in sel:
            hold = i['title'].split(u'\u2013')[0]
            if not hold in t.keys():
                t.update({hold: i['href']})
        final = t.items()
        for n, i in enumerate(final):
            print("{}: {}".format(n, i[0].encode('utf-8')))
        selection = input()
        hold = webpage(final[selection][1])
        self.name = hold.soup('div', id='extras')[0].a['href'].split('/')[-2]

    class page(vidSeries.page):

        @property
        def url(self):
            return self.episode
        @property
        def video(self):
            link = self.soup.find('div', id='video').script.text.split('"')[-2]
            return link


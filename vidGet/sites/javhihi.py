import re
from bs4 import BeautifulSoup
from ..vidsite import vidSeries
from ..util import memorize, webpage

bs4 = BeautifulSoup
tags  = ['hihi', 'javhihi']

class Series(vidSeries):
    siteTemplate   = 'http://javhihi.com/{}'
    seriesTemplate = siteTemplate.format('japanese-av/{}.html')

    @property
    def pages(self):
        return [self.page(i.a['href'], self) for i in
                self.soup(class_='video-item')]

    class page(vidSeries.page):

        @property
        def name(self):
            url = self.video
            return ''.join([self.series.title, '/',
                url.split('?')[0].split('/')[-1]])

        @property
        def video(self):
            pref = ['720p', '360p']
            return next(o['src'] for i in pref
                        for o in self.soup('video')[0]('source')
                        if i in o['data-res'])
        @property
        def url(self):
            return self.series.siteTemplate.format(self.episode)

import re

from ..vidsite import vidSeries
from ..util import memorize, webpage

tags  = ['hc', 'hentaicraving']

class Series(vidSeries):
    siteTemplate   = 'http://www.hentai2w.com{}'
    seriesTemplate = siteTemplate.format('/watch/{}')

    @property
    @memorize
    def pages(self):
        return [self.page(i['href'],self) for i in test.soup.main.h3('a')[1:]]

    @property
    def title(self):
        return self.soup.main.h3.a.text.strip().replace(' ', '_')

    class page(vidSeries.page):
        @property
        def name(self):
            return ''.join([self.episode.split('/')[-1], '.mp4'])
        @property
        def url(self):
            return self.episode
        @property
        def video(self):
            pref = ['720p', '360p']
            return next(o['value'] for i in pref 
                        for o in self.soup.findAll('option') 
                        if i in o.text)

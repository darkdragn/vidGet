import re

from ..vidsite import vidSeries
from ..util import memorize, webpage

tags = ['h2w', 'hentai2w']


class Series(vidSeries):
    siteTemplate = 'http://www.hentai2w.com{}'
    seriesTemplate = siteTemplate.format('/watch/{}')

    @property
    @memorize
    def pages(self):
        return [self.page(i['href'], self) for i in self.soup('div',
                class_='block-content remove-padding bg-white')[0]('a')]

    def runExtras(self):
        url_search = 'http://hentai2w.com/search?search={}'
        search = webpage(url_search.format(self.name))
        sel = search.soup.select('div.block-content.row')[0]('a')
        print('Please select from the following:')
        for n, i in enumerate(sel):
            print("{}: {}".format(n, i['data-title'].encode('utf-8')))
        selection = input()
        self.name = sel[selection]['href'].split('/')[-1]
        # sys.exit()

    @property
    def title(self):
        hold = self.soup.main.h3.a.text
        return hold.strip().replace(' ', '_').replace(':', '')

    class page(vidSeries.page):
        @property
        def url(self):
            return self.episode

        @property
        def video(self):
            base_url = 'http://{}/video/{}/{}?st={}&e={}'
            hold = re.search('file: *\'(.*)\',', self.source).group(1)
            s = hold.split('/')
            return base_url.format(s[2], s[6], s[-1], s[4], s[5])

import re
from bs4 import BeautifulSoup
from urlparse import urljoin
from ..vidsite import vidSeries
from ..util import memorize, webpage

bs4 = BeautifulSoup
tags  = ['sp', 'slashpanda']

class Series(vidSeries):
    siteTemplate   = 'https://slashpanda.com{}'
    seriesTemplate = siteTemplate.format('/anime/{}')
    aud = 'sub'

    @property
    def pages(self):
        epi_list = [urljoin(self.url, a['href']) for a in self.soup('a')
                    if 'season' in a['href']][::-1]
        epi_list = [s for s in epi_list if self.aud in s]
        return [self.page(a) for a in epi_list]
    def runExtras(self):
        if 'dub' in self.extras:
            self.aud = 'dub'


    class page(vidSeries.page):

        @property
        def name(self):
            cut_up = self.url.split('/')
            series = cut_up[4]
            sd = cut_up[5].split('-')[-1]
            season = cut_up[5].split('-')[1]
            epi = cut_up[-1].split('-')[-1]

            name_base = '{}/{}_s{:02d}e{:02d}.mp4'
            return name_base.format(series, series, int(season), int(epi))

        @property
        def url(self):
            return self.episode

        @property
        def video(self):
            base = 'https://estream.to/'
            spec = re.search('estream.to\\\\u002F(.*?)"', self.source).group(1)
            embed_url = urljoin(base, spec)
            embed = webpage(embed_url)

            return next(s['src'] for s in embed.soup('source') 
                    if 'mp4' in s['src'])


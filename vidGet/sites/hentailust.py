import re
from bs4 import BeautifulSoup
from ..vidsite import vidSeries
from ..util import memorize, webpage

bs4 = BeautifulSoup
tags  = ['hc', 'hentaicraving']

class Series(vidSeries):
    siteTemplate   = 'http://www.hentailust.tv{}'
    seriesTemplate = siteTemplate.format('/hentai/{}')

    @property
    def pages(self):
        return [self.page(i.a['href'], self) for i in self.soup.find('div',
                class_="td-ss-main-content").findAll('h3')[::-1]]

    class page(vidSeries.page):

        @property
        def url(self):
            return self.episode
        @property
        def video(self):
            s_text = self.soup.find('div', class_="td-post-content").script.text
            h_list = s_text.split('|')[25:31]
            l_temp = "http://www.{}.{}/{}/{}/{}.{}"
            link = l_temp.format(h_list[5], h_list[0], h_list[3], h_list[1],
                                 h_list[2], "mp4")
            return link


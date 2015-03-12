import re

try:
    from vidGet.vidsite import memorize, vidSeries
except ImportError:
    from vidsite import memorize, vidSeries

class kiss(vidSeries):
    siteTemplate = 'http://kissanime.com{}'
    seriesTemplate = siteTemplate.format('/Anime/{}')
    tags  = ['k', 'kiss']
            
    def runExtras(self):
        for i in self.extras:
            if 'car' in i:
                self.siteTemplate = 'http://kisscartoon.me{}'
                self.seriesTemplate = self.siteTemplate.format('/Cartoon/{}')
    @property
    @memorize
    def pages(self):
        return [self.page(self.siteTemplate.format(i['href']), self) 
                          for i in self.soup.find('table').findAll('a')[::-1]]
    
    class page(vidSeries.page):
    
        @property
        @memorize
        def video(self):
            return next(s['value'] for i in ['720p', '480p', '1080p', '360p'] for s in 
                        self.soup.find('select', id="selectQuality").findAll('option') if i in s)
                        
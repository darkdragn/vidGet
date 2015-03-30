import re

try:
    from vidGet.vidsite import memorize, vidSeries
except ImportError:
    from vidsite import memorize, vidSeries

class kiss(vidSeries):
    siteTemplate = 'http://kissanime.com{}'
    seriesTemplate = siteTemplate.format('/Anime/{}')
    tags  = ['k', 'kiss']
    
    formatPage = lambda self, x: self.siteTemplate.format(x['href'])
    pageList   = lambda self: self.soup.find('table').findAll('a')[::-1]
    
    def runExtras(self):
        for i in self.extras:
            if 'car' in i:
                self.siteTemplate = 'http://kisscartoon.me{}'
                self.seriesTemplate = self.siteTemplate.format('/Cartoon/{}')
    
    class page(vidSeries.page)
    
        @property
        @memorize
        def video(self):
            #if 'youtube' in self.source and self.series.cookie:
                #return chromeVid(self)
            qualList = self.soup.find('select', id="selectQuality").findAll('option')
            return next(s['value'] for i in ['720p', '718p', '480p', '1080p', '360p', '352p'] 
                        for s in qualList if i in s)

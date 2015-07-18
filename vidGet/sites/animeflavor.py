import re
try:
    from vidGet.vidsite import vidSeries
    from vidGet.util import memorize, runRepl, unescape, webpage
except ImportError:
    from vidsite import vidSeries
    from util import memorize, runRepl, unescape, webpage

class animeflavor(vidSeries):
    siteTemplate   = 'http://www.animeflavor.com{}'
    seriesTemplate = siteTemplate.format('/cartoon/{}')
    tags  = ['af', 'animeflavor']
    
    @property
    @memorize
    def pages(self):
        return [self.page(i.a['href'], self) for i in self.soup.findAll('ul', class_='menu')[1].findAll('li')]
        
    class page(vidSeries.page):
        vidComp = re.compile('file: \"(?P<vid>[^\"]*)\"')
        @property
        def embed(self):
            return webpage(self.embedLink)
        @property
        def embedLink(self):
            return self.soup.find(src=re.compile('filehoot'))['src']
        @property
        def url(self):
            return self.series.siteTemplate.format(self.episode)
        

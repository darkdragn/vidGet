import re
try:
    from vidGet.vidsite import vidSeries
except ImportError:
    from vidsite import vidSeries

class gogoanime(vidSeries):
    siteTemplate   = 'http://gogoanime.tv{}'
    seriesTemplate = siteTemplate.format('/category/{}')
    tags  = ['gogo', 'gogoanime']
    
    @property
    def pages(self):
        return [self.page(i, self) for i in xrange(1,int(self.soup.find('a', 
                                                   class_='active')['ep_end'])+1)]
        
    class page(vidSeries.page):
        @property
        def video(self):
            pref = ['720p', '360p']
            return next(o['value'] for i in pref 
                        for o in self.soup.findAll('option') 
                        if i in o.text)
        @property
        def url(self):
            return self.series.siteTemplate.format(''.join(['/', self.series.name, 
                                                   '-episode-', str(self.episode)]))

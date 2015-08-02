import re
try:
    from vidGet.vidsite import vidSeries
    from vidGet.util import webpage
except ImportError:
    from vidsite import vidSeries
    from util import webpage

class myhentai(vidSeries):
    siteTemplate   = 'http://myhentai.tv/{}'
    seriesTemplate = siteTemplate.format('/category/{}')
    tags  = ['mh', 'myhentai']
    
    @property
    def pages(self):
        return [self.page(i.a['href'], self) for i in self.soup.findAll('span', 
                                                                 class_='epd')]
        
    class page(vidSeries.page):
        @property
        def name(self):
            return self.video.split('/')[-1]
        @property
        def url(self):
            return self.episode
        @property
        def video(self):
            hold = webpage(self.soup.iframe['src'])
            return re.search('file: \"([^\"]*)\"', hold.source).group(1)
            

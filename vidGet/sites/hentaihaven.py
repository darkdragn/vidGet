import re
try:
    from vidGet.vidsite import vidSeries
except ImportError:
    from vidsite import vidSeries

class hentaihaven(vidSeries):
    siteTemplate   = 'http://hentaihaven.org{}'
    seriesTemplate = siteTemplate.format('/series/{}/?sort=title')
    tags  = ['hh', 'hentaihaven']
    
    @property
    def pages(self):
        return [self.page(i.a['href']) for i in self.soup.findAll('h3') 
                                       if not 'The Blacklist' == i.text]
        
    class page(vidSeries.page):
        @property
        def video(self):
            pref  = ['720p', '360p']
            links = self.soup.find('div', class_='download_feed_link')
            return next(o['href'] for i in pref 
                        for o in links.findAll('a') 
                        if i in o.span.text)

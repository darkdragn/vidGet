import re
try:
    from vidGet.vidsite import vidSeries
except ImportError:
    from vidsite import vidSeries

class watchcartoononline(vidSeries):
    siteTemplate   = 'http://www.hentai2w.com{}'
    seriesTemplate = siteTemplate.format('/anime/{}')
    tags  = ['h2w', 'hentai2w']
    
    @property
    def pages(self):
        return [self.page(i.a['href'], self) for i in self.soup.find('div', 
                              class_='anime_info_episodes').findAll('li')[::-1]]
        
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

import re
try:
    from vidGet.vidsite import vidSeries
    from vidGet.util import webpage
except ImportError:
    from vidsite import vidSeries
    from util import webpage

class hentaicraving(vidSeries):
    siteTemplate   = 'http://www.hentaicraving.com{}'
    seriesTemplate = siteTemplate.format('/hentai-series/{}')
    tags  = ['hc', 'hentaicraving']
    
    @property
    def pages(self):
        return [self.page(i.a['href'], self) for i in self.soup.find('ul', 
                                     class_='eps eps-list').findAll('li')]
        
    class page(vidSeries.page):
        @property
        def embed(self):
            return next(webpage(i['src']) for i in self.soup.findAll('iframe')
                                                  if 'uphentaivid' in i['src'])
        @property
        def url(self):
            return self.episode
        @property
        def video(self):
            scriptText = self.embed.soup.findAll('script')[-2].text
            server = re.search('s/([^\/]*)/r', scriptText).group(1)
            uniq   = re.search('mp4\|([^\|]*)\|files', scriptText).group(1)
            return ''.join(['http://uphentaivid.net/files/', server, '/',
                            uniq, '/video.mp4?start=0'])

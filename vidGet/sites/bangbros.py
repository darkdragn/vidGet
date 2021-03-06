import re

try:
    from vidGet.vidsite import memorize, initMech, vidSeries, webpage
except ImportError:
    from vidsite import memorize, initMech, vidSeries, webpage

class bangbros(vidSeries):
    #siteTemplate = 'http://beta.members.bangbros.com{}'
    #seriesTemplate = siteTemplate.format('/product/1/girl/{}')
    siteTemplate = 'http://members.bangbros.com{}'
    seriesTemplate = siteTemplate.format('/model/{}')
    tags, type_ = ['bb', 'bangbros'], 'Model'
    
    formatPage = lambda self, x: self.siteTemplate.format(x['href'])
    pageList   = lambda self: self.soup.findAll('a', class_='etLnk')
    siteList   = lambda self, url: url.soup.findAll('a', class_='etLnk')

    def __init__(self, series, extras=None, cookie=None):
        self.name = series
        self.br = initMech(self.siteTemplate.format(''), cookie)
        if extras:
            self.extras = extras.split(',')
            self.runExtras()
    def runExtras(self):
        for i in self.extras:
            if 'site' in i:
                self.pageList, self.type_ = self.siteList, 'Site'
                self.seriesTemplate = self.siteTemplate.format('/product/1/site/{}')
                self.pages = self._sitePages
            elif 'title' in i:
                self.title = i.split('=')[-1]
            elif 'search' in i:
                self.seriesTemplate = self.siteTemplate.format('/product/1/search/{}')
                self.pageList, self.title = self.siteList, self.name
            elif 'pref' in i:
                self.pref = i.split('=')[-1]
        
    def sitePageGet(self, cp=1, lp=None):
        pages = []
        url = webpage('/'.join([self.url, 'latest', str(cp)]), self.br)
        if not lp:
            try:
                lp = int(self.soup.findAll('a', class_='echPagi')[-2].text)
            except:
                lp=1
        pages.extend([self.page(self.formatPage(i), self) 
                      for i in self.siteList(url)])
        if not cp == lp:
                pages.extend(self.sitePageGet(cp+1, lp))
        return pages
    @property
    @memorize
    def _sitePages(self):
        return self.sitePageGet()
    @property
    @memorize
    def title(self):
        return self.soup.find('span', class_='mPhed').text.replace(' ', '')
    class page(vidSeries.page):
        
        @property
        @memorize
        def name(self):
            return self.video.split('&')[1].split('=')[1]
        @property
        @memorize
        def video(self):
            pref = ['720', '480']
            if hasattr(self.series, 'pref'):
                for i in pref:
                    if self.series.pref in i:
                        pref.insert(0, pref.pop(pref.index(self.series.pref)))
            btnHolder = self.soup.findAll('div', class_='dropM')
            return next(b['href'] for i in pref
                        for t in btnHolder for b in t.findAll('a') 
                        if i in b['href'] and 'mp4' in b['href'])

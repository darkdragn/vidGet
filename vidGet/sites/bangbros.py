import re

try:
    from vidGet.vidsite import memorize, initMech, vidSeries
except ImportError:
    from vidsite import memorize, initMech, vidSeries

class bangbros(vidSeries):
    siteTemplate = 'http://beta.members.bangbros.com{}'
    seriesTemplate = siteTemplate.format('/product/1/girl/{}')
    tags, type_ = ['bb', 'bangbros'], 'Model'
    
    formatPage = lambda self, x: self.siteTemplate.format(x.a['href'])
    pageList = lambda self: self.soup.findAll('span', class_='echThumbLnk-desc')
    siteList = lambda self: self.soup.findAll('div', 
                            class_='vdoThumbHolder')[-1].findAll('span', 
                            class_='echThumbLnk-desc')
        
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
                self.seriesTemplate = self.siteTemplate
                self.siteLoad()
                self.pages = self._sitePages
            elif 'title' in i:
                self.title = i.split('=')[-1]
            elif 'search' in i:
                self.seriesTemplate = self.siteTemplate.format('/product/1/search/{}')
                self.pageList, self.title = self.siteList, self.name
    def siteLoad(self):
        self.br.open(self.url)
        self.br.click_link(link=self.br.find_link(text_regex=re.compile('Latest.*')))
        self.source = self.br.response().read()
        
    @property
    @memorize
    def title(self):
        return self.soup.h1.text.replace(' ', '')
    class page(vidSeries.page):
        
        @property
        @memorize
        def name(self):
            return self.video.split('&')[1].split('=')[1]
        @property
        @memorize
        def video(self):
            btnHolder = self.soup.findAll('div', class_='wtm-btnHolder clearfix')
            return next(b['href'] for i in ['720', '480']
                        for t in btnHolder for b in t.findAll('a') 
                        if '720' in b['href'] and 'mp4' in b['href'])
